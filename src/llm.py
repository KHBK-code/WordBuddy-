"""
LLM interface for WordBuddy.
This is the ONLY module that calls the LLM.
It always returns a validated 7-key dict the UI can render directly.
Callers never handle raw text, JSON errors, or provider exceptions.

Provider selection (via environment variables):
  LLM_PROVIDER=groq    → Groq OpenAI-compatible chat API
  LLM_PROVIDER=watsonx → IBM watsonx Granite
  (anything else)      → offline fallback only

API keys are read from the environment; they are never logged.
"""

from __future__ import annotations

import json
import logging
import os
import re

import requests

from src.fallback import FALLBACK_DICT, lookup as fallback_lookup
from src.prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# LLMError — defined first so all functions below can reference it (fix 2b)
# ---------------------------------------------------------------------------
class LLMError(Exception):
    """Raised when the LLM call or validation fails unrecoverably."""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_REQUIRED_KEYS = frozenset({
    "syllables",
    "pronunciation_hint",
    "definition",
    "examples",
    "analogy",
    "encouragement",
    "practice_question",
})

# Word-boundary regex for content blocking — avoids false positives on
# substrings like "deadline", "sextant", "Essex" (fix 2d).
_BLOCKLIST_TERMS = (
    "death", "died", "dead", "kill", "murder", "blood",
    "cancer", "disease", "surgery", "diagnosis",
    "drugs", "alcohol", "sex", "violence", "weapon",
)
_BLOCKLIST_RE = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in _BLOCKLIST_TERMS) + r")\b",
    re.IGNORECASE,
)

# Injection-detection pattern — catches common jailbreak/override phrases (fix 1a).
_INJECTION_RE = re.compile(
    r"\b(ignore|forget|disregard|pretend|you are now|act as|jailbreak|"
    r"new instruction|override|system prompt|bypass|disable)\b",
    re.IGNORECASE,
)

_REQUEST_TIMEOUT = 15  # seconds

# Returned when the LLM is unavailable and the word is not in the fallback dict.
_OFFLINE_DEFAULT: dict = {
    "syllables": "?",
    "pronunciation_hint": "ask a grown-up to help",
    "definition": "We could not look that up right now. Try again in a little while!",
    "examples": [
        "Sometimes the internet takes a little break.",
        "Ask a teacher or grown-up to help you with this word today.",
    ],
    "analogy": "It is like when the library is closed — the books are still there, just not right now.",
    "encouragement": "You are so brave for looking up new words. Keep it up!",
    "practice_question": "Can you ask a grown-up what this word means?",
}

# Last-resort fallback — returned when something truly unexpected happens
# (e.g. an unhandled exception type). Never shows a stack trace.
_BRAVE_FALLBACK: dict = {
    "syllables": "?",
    "pronunciation_hint": "?",
    "definition": "Something went wrong on our end, but that is okay!",
    "examples": [
        "Even the best helpers need a moment to think sometimes.",
        "Try the word again in a little while — we will get it next time!",
    ],
    "analogy": "It is like when a library book is being re-shelved — it will be back soon!",
    "encouragement": "You still did a brave thing by trying. That counts for a lot!",
    "practice_question": "While you wait, can you think of another big word you would like to learn?",
}


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------
def _clean_input(word: str) -> str:
    """Strip whitespace and validate the input.

    Returns the cleaned string.
    Raises ValueError with a reason code on bad input:
      "empty"     — nothing typed
      "too_long"  — more than 80 characters
      "no_letters"— no alphabet characters at all
      "injection" — input looks like a prompt-injection attempt (fix 1a)
    """
    if not word:
        raise ValueError("empty")
    cleaned = word.strip()
    if not cleaned:
        raise ValueError("empty")
    if len(cleaned) > 80:
        raise ValueError("too_long")
    if not re.search(r"[a-zA-Z]", cleaned):
        raise ValueError("no_letters")
    # Reject instruction-like input before it reaches the LLM (fix 1a)
    if _INJECTION_RE.search(cleaned):
        raise ValueError("injection")
    return cleaned


# ---------------------------------------------------------------------------
# JSON parsing (robust — uses raw_decode to handle nested braces correctly)
# ---------------------------------------------------------------------------
def _parse_json(text: str) -> dict:
    """Parse the first valid JSON object from an LLM text response.

    Handles:
    1. Response wrapped in ```json ... ``` or ``` ... ``` fences
    2. Leading/trailing prose around the JSON object
    3. Nested braces inside the JSON (fix 2a — replaces greedy regex)

    Raises LLMError if no valid JSON object can be found.
    """
    text = text.strip()

    # Strip code fences first so raw_decode sees clean JSON
    fence_match = re.search(r"```(?:json)?\s*(\{.*)\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    # Walk the string and stop at the first position that successfully
    # decodes a JSON object — correctly handles nested braces (fix 2a).
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch == "{":
            try:
                data, _ = decoder.raw_decode(text, i)
                if not isinstance(data, dict):
                    raise LLMError(
                        f"Expected a JSON object, got {type(data).__name__}"
                    )
                return data
            except json.JSONDecodeError:
                continue  # not a valid start; keep scanning

    raise LLMError("No valid JSON object found in LLM response")


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------
def _validate(data: dict) -> dict:
    """Validate a parsed response dict against the 7-key schema.

    Raises LLMError on structural or content violations.
    Returns a dict containing ONLY the 7 required keys (extra keys are
    discarded — fix 2c).
    """
    missing = _REQUIRED_KEYS - data.keys()
    if missing:
        raise LLMError(f"Response missing keys: {missing}")

    for key in _REQUIRED_KEYS:
        value = data[key]
        if key == "examples":
            if not isinstance(value, list) or len(value) != 2:
                raise LLMError("'examples' must be a list of exactly 2 strings")
            for item in value:
                if not isinstance(item, str) or not item.strip():
                    raise LLMError("Each example must be a non-empty string")
                if len(item) > 300:
                    raise LLMError(f"Example too long ({len(item)} chars)")
        else:
            if not isinstance(value, str) or not value.strip():
                raise LLMError(f"Key '{key}' must be a non-empty string")
            if len(value) > 300:
                raise LLMError(f"Value for '{key}' too long ({len(value)} chars)")

    # Child-safety content gate — all 7 fields, word-boundary matching (fix 2d).
    all_values = [data[k] for k in _REQUIRED_KEYS if k != "examples"] + data["examples"]
    check_text = " ".join(all_values)
    if _BLOCKLIST_RE.search(check_text):
        raise LLMError("Blocked content detected in response")

    # Discard any extra keys the model may have added (fix 2c)
    return {k: data[k] for k in _REQUIRED_KEYS}


# ---------------------------------------------------------------------------
# Provider: Groq (OpenAI-compatible)
# ---------------------------------------------------------------------------
def _call_groq(word: str) -> dict:
    """Call the Groq chat completion API and return a parsed, validated dict.

    Required env vars:
      GROQ_API_KEY  — your Groq API key
    Optional:
      GROQ_MODEL    — defaults to "llama3-8b-8192"
    """
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise LLMError("GROQ_API_KEY is not set")

    model = os.environ.get("GROQ_MODEL", "llama3-8b-8192")
    url = "https://api.groq.com/openai/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(word)},
        ],
        "temperature": 0.4,
        "max_tokens": 512,
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=_REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.Timeout:
        raise LLMError("Groq request timed out")
    except requests.HTTPError as exc:
        raise LLMError(f"Groq HTTP error: {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise LLMError(f"Groq request failed: {type(exc).__name__}") from exc

    try:
        content = resp.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as exc:
        raise LLMError(f"Unexpected Groq response shape: {exc}") from exc

    return _validate(_parse_json(content))


# ---------------------------------------------------------------------------
# Provider: IBM watsonx
# ---------------------------------------------------------------------------
def _call_watsonx(word: str) -> dict:
    """Call IBM watsonx text generation API and return a parsed, validated dict.

    Required env vars:
      WATSONX_API_KEY   — IBM Cloud API key
      WATSONX_PROJECT_ID — watsonx project ID
    Optional:
      WATSONX_URL       — defaults to Dallas endpoint
      WATSONX_MODEL     — defaults to "ibm/granite-13b-chat-v2"
    """
    api_key = os.environ.get("WATSONX_API_KEY", "")
    project_id = os.environ.get("WATSONX_PROJECT_ID", "")
    if not api_key or not project_id:
        raise LLMError("WATSONX_API_KEY and WATSONX_PROJECT_ID must both be set")

    base_url = os.environ.get(
        "WATSONX_URL",
        "https://us-south.ml.cloud.ibm.com",
    )
    model = os.environ.get("WATSONX_MODEL", "ibm/granite-13b-chat-v2")

    # Step 1: obtain an IAM bearer token
    try:
        token_resp = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": api_key,
            },
            timeout=_REQUEST_TIMEOUT,
        )
        token_resp.raise_for_status()
        bearer = token_resp.json()["access_token"]
    except requests.RequestException as exc:
        raise LLMError(f"watsonx IAM token request failed: {type(exc).__name__}") from exc
    except (KeyError, ValueError) as exc:
        raise LLMError(f"watsonx IAM response unexpected: {exc}") from exc

    # Step 2: call the generation endpoint
    # Strip Granite turn-delimiter tokens from the word so they cannot
    # break out of the <|user|> block (fix 1c).
    sanitised_word = re.sub(r"<\|[^|]*\|>", "", word)
    prompt_text = (
        f"<|system|>\n{SYSTEM_PROMPT}\n"
        f"<|user|>\n{build_user_prompt(sanitised_word)}\n"
        "<|assistant|>\n"
    )
    payload = {
        "model_id": model,
        "input": prompt_text,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 512,
            "temperature": 0.4,
        },
        "project_id": project_id,
    }

    try:
        gen_resp = requests.post(
            f"{base_url}/ml/v1/text/generation?version=2023-05-29",
            json=payload,
            headers={
                "Authorization": f"Bearer {bearer}",
                "Content-Type": "application/json",
            },
            timeout=_REQUEST_TIMEOUT,
        )
        gen_resp.raise_for_status()
    except requests.Timeout:
        raise LLMError("watsonx request timed out")
    except requests.HTTPError as exc:
        raise LLMError(f"watsonx HTTP error: {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise LLMError(f"watsonx request failed: {type(exc).__name__}") from exc

    try:
        content = gen_resp.json()["results"][0]["generated_text"]
    except (KeyError, IndexError, ValueError) as exc:
        raise LLMError(f"Unexpected watsonx response shape: {exc}") from exc

    return _validate(_parse_json(content))


# ---------------------------------------------------------------------------
# Provider dispatch
# ---------------------------------------------------------------------------
def _call_provider(word: str) -> dict:
    """Route to the configured LLM provider and return a validated dict.

    Raises LLMError on any provider failure.
    """
    provider = os.environ.get("LLM_PROVIDER", "").lower().strip()
    if provider == "groq":
        return _call_groq(word)
    if provider == "watsonx":
        return _call_watsonx(word)
    raise LLMError(f"No LLM provider configured (LLM_PROVIDER='{provider}')")


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------
# Child-friendly error dicts for each input rejection reason
_INPUT_ERROR_RESPONSES: dict[str, dict] = {
    "empty": {
        "syllables": "?",
        "pronunciation_hint": "?",
        "definition": "You did not type anything yet! Try typing a word first.",
        "examples": [
            "Type a word like 'enormous' or 'peculiar'.",
            "Then press the button and I will explain it!",
        ],
        "analogy": "It is like trying to open a book that has no pages yet.",
        "encouragement": "Go ahead — type any word and I will help you!",
        "practice_question": "What is a big word you have heard lately?",
    },
    "too_long": {
        "syllables": "?",
        "pronunciation_hint": "?",
        "definition": "That is a really long sentence! Try picking one word from it and typing that instead.",  # fix 3a — removed "just"
        "examples": [
            "For example, type the word 'photosynthesis' on its own.",
            "Or try the word 'government' and I will explain it.",
        ],
        "analogy": "It is like trying to fit a whole pizza into one bite — one word at a time works better!",
        "encouragement": "Pick the biggest word from what you wrote and try again!",
        "practice_question": "Which one word from your sentence do you want to learn about?",
    },
    "no_letters": {
        "syllables": "?",
        "pronunciation_hint": "?",
        "definition": "Hmm, I could not find any letters in there! Try typing a word with letters, like 'ancient' or 'enormous'.",  # fix 3b — reframed as curious, not corrective
        "examples": [
            "Type a word like 'ancient' or 'territory'.",
            "Or try 'magnificent' — it is a great one!",
        ],
        "analogy": "Letters are the building blocks of words, just like LEGO bricks build a castle.",
        "encouragement": "You can do it — type a word and I will help you right away!",
        "practice_question": "Can you think of a word with at least three letters?",
    },
    "injection": {
        "syllables": "?",
        "pronunciation_hint": "?",
        "definition": "Hmm, that does not look like a word to explain. Try typing a single word, like 'enormous' or 'hypothesis'.",
        "examples": [
            "Type a word you saw in a book or heard at school.",
            "Any big word you are curious about works great!",
        ],
        "analogy": "WordBuddy is like a dictionary — it works best with one word at a time.",
        "encouragement": "You are doing great — try typing one word and I will explain it for you!",
        "practice_question": "What is a word you have been wondering about lately?",
    },
}


def explain_word(word: str) -> dict:
    """Return a validated 7-key explanation dict for *word*.

    Resolution order:
      1. Input validation  → return friendly error dict on bad input
      2. Fallback dict     → return pre-written entry on exact lowercase match
      3. LLM provider      → call Groq or watsonx based on LLM_PROVIDER env var
      4. Fallback lookup   → use offline dict if LLM fails
      5. Offline default   → safe generic dict if word not in fallback dict
      6. _BRAVE_FALLBACK   → last resort if any unexpected exception escapes

    Never raises. Never logs API keys. Always returns a renderable dict.
    No stack trace ever reaches the caller.
    """
    try:
        # --- 1. Input validation (includes injection detection) ---
        try:
            cleaned = _clean_input(word)
        except ValueError as exc:
            reason = str(exc)
            return _INPUT_ERROR_RESPONSES.get(reason, _INPUT_ERROR_RESPONSES["empty"])

        lower = cleaned.lower()

        # --- 2. Fallback dict (exact lowercase match — fast, no network) ---
        if lower in FALLBACK_DICT:
            return FALLBACK_DICT[lower]

        # --- 3. LLM provider ---
        provider = os.environ.get("LLM_PROVIDER", "").lower().strip()
        if provider in ("groq", "watsonx"):
            try:
                return _call_provider(cleaned)
            except LLMError as exc:
                logger.warning("LLM call failed (%s): %s", provider, exc)
                # fall through to offline fallback below

        # --- 4 + 5. Offline fallback (partial match or generic) ---
        return fallback_lookup(lower)

    except Exception as exc:  # noqa: BLE001 — intentional last-resort catch
        # Log the details for operators (no key material in exc message)
        logger.error("explain_word: unexpected exception for input %r: %s", word, type(exc).__name__)
        return _BRAVE_FALLBACK
