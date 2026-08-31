# WordBuddy — MVP Implementation Plan

---

## 1. One-Sentence Pitch

WordBuddy is a kid-friendly AI companion that turns intimidating big words into clear, encouraging, bite-sized explanations so children who struggle with reading can feel confident and keep going.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────┐
│              app.py                     │
│   Streamlit UI — input, display, state  │
│   wires everything together; no logic   │
└────────────┬────────────────────────────┘
             │ calls
     ┌───────▼────────┐     ┌─────────────────┐
     │  src/llm.py    │────▶│  LLM API (env)  │
     │  send prompt   │     └─────────────────┘
     │  parse + valid │
     └───────┬────────┘
             │ on failure
     ┌───────▼──────────┐
     │ src/fallback.py  │
     │ 50-word offline  │
     │ dictionary       │
     └──────────────────┘

     ┌──────────────────┐
     │ src/prompts.py   │  ◀── single source of truth for all prompt text
     └──────────────────┘

     ┌──────────────────┐
     │ src/session.py   │  ◀── all st.session_state reads/writes
     │ learned words    │
     │ token points     │
     └──────────────────┘
```

**Key architectural decisions:**
- Streamlit reruns the entire script on every user interaction — all state must live in `st.session_state` via `src/session.py`, never in module-level variables.
- `src/llm.py` is the only module allowed to call the LLM. It always returns a validated Python dict. Callers never handle raw text or catch JSON errors.
- Every LLM call path must have a corresponding fallback in `src/fallback.py`. The fallback is a hard requirement, not a nice-to-have.

---

## 3. Exact File List

8 tracked files (`.env` is gitignored and never committed):

```
WordBuddy/
├── app.py                    # Streamlit entry point; UI only, no business logic
├── requirements.txt          # streamlit, python-dotenv, requests (or SDK), pytest, ruff
├── .bobignore                # blocks .env and secrets from Bob
├── src/
│   ├── llm.py                # LLM call → validated JSON dict; raises on unrecoverable error
│   ├── prompts.py            # system prompt + user prompt templates; reading level lives here
│   ├── fallback.py           # offline dict of ~50 hard words; used when llm.py fails
│   └── session.py            # get/set helpers for st.session_state (words, points)
├── tests/
│   └── test_wordbuddy.py     # all unit tests: llm, fallback, session, prompts
└── docs/
    └── PLAN.md               # this file
```

> Note: `src/__init__.py` is not needed — Python 3.11 supports namespace packages without it.

---

## 4. LLM Response Schema

Every call to `src/llm.py` must return a dict matching this exact structure. Any response that fails validation triggers the fallback.

```json
{
  "syllables": "in·tim·i·dat·ing",
  "pronunciation_hint": "in-TIM-ih-day-ting",
  "definition": "When something feels really scary or makes you feel small.",
  "examples": [
    "The big dog was intimidating, but it was actually friendly.",
    "Mia felt intimidated before her first piano recital."
  ],
  "analogy": "It's like when you see a really tall slide and your tummy does a flip.",
  "encouragement": "You just learned a HUGE word. You're amazing!",
  "practice_question": "Can you think of a time something felt intimidating but turned out okay?"
}
```

Validation rules (enforced in `src/llm.py`):
- All 7 keys present and non-empty strings/lists
- `examples` is a list of exactly 2 strings
- No string longer than 200 characters (prevents runaway output)
- No content matching a blocklist of adult/medical terms (child-safe gate)

---

## 5. Data Flow

```
User types word → app.py
  → session.py: validate input (non-empty, ≤ 60 chars)
  → prompts.py: build system_prompt + user_prompt
  → llm.py: call API, parse JSON, validate schema
      ├── success → return dict to app.py
      └── failure → fallback.py: look up word in offline dict
                        ├── found  → return fallback dict
                        └── not found → return generic "We'll look that up later!" dict

app.py receives dict →
  → display 7 fields in colorful large-text UI
  → session.py: add_word(word), add_points(1)
  → show practice question
      → child answers → session.py: add_points(2)
  → sidebar: session.py.get_learned_words(), get_points()
```

---

## 6. Prompting Strategy

### System prompt (lives in `src/prompts.py`)

Goals:
- Lock reading level to 2nd–3rd grade vocabulary in all outputs
- Enforce the 7-field JSON schema unconditionally
- Forbid adult content, medical diagnoses, frightening examples, and shaming language
- Instruct the model to be warm, encouraging, and use concrete everyday analogies

Key constraints to state explicitly in the system prompt:
1. "Always respond with valid JSON only. No extra text before or after the JSON."
2. "Use words a 7-year-old would understand."
3. "Never mention illness, death, violence, or anything scary."
4. "Always end with an encouraging message."
5. "The analogy must use something from a child's everyday life (toys, food, school, pets)."

### User prompt template (lives in `src/prompts.py`)

```
Explain the word or phrase: "{word}"

Return JSON with exactly these keys:
syllables, pronunciation_hint, definition, examples (list of 2),
analogy, encouragement, practice_question
```

### Why structured JSON output?

- Streamlit renders each field independently — no string splitting needed
- Validation is deterministic — if a key is missing, fallback fires immediately
- Makes unit testing `src/llm.py` straightforward (no text parsing)

---

## 7. Session State Design

Managed exclusively through `src/session.py`. `app.py` never accesses `st.session_state` directly.

| Key | Type | Description |
|---|---|---|
| `learned_words` | `list[str]` | Words explained this session, in order |
| `token_points` | `int` | Cumulative points (default 0) |

Point rules:
- `+1` when a word is successfully explained (LLM or fallback)
- `+2` when the child submits a non-empty answer to the practice question

---

## 8. Error Handling Strategy

| Scenario | Handling |
|---|---|
| Empty input | Blocked in UI before API call; friendly message ("Type a word first!") |
| Input > 60 chars | Truncated with notice, or friendly rejection |
| LLM API timeout / 5xx | `src/llm.py` raises; `app.py` calls fallback |
| JSON parse failure | `src/llm.py` raises; `app.py` calls fallback |
| Schema validation failure | `src/llm.py` raises; `app.py` calls fallback |
| Word not in fallback dict | Generic warm response: "That's a tricky one! Ask a grown-up too." |
| Missing API key env var | `src/llm.py` raises `EnvironmentError` at startup; Streamlit shows setup instructions |

All error messages shown to the child must be at 2nd–3rd grade reading level and must not shame or alarm.

---

## 9. Offline Fallback Dictionary (`src/fallback.py`)

Approximately 50 words selected to cover the most common "hard words" encountered by children ages 8–10. Examples:

`enormous`, `peculiar`, `sufficient`, `ancient`, `generate`, `ferocious`, `transparent`, `exhausted`, `terrific`, `collaborate`, `elaborate`, `consequence`, `demonstrate`, `environment`, `exaggerate`, `frustrated`, `hesitate`, `illuminate`, `magnificent`, `necessary`, `obvious`, `persistent`, `question`, `reluctant`, `suspicious`, `tremendous`, `unfamiliar`, `vocabulary`, `wonderful`, `yesterday`

Each entry in the dict uses the same 7-key schema as the LLM response, pre-filled with child-safe, hand-written content. This guarantees the app works in demo conditions with no internet or API key.

---

## 10. UI Design

Streamlit layout — no custom HTML/CSS required:

```
┌─────────────────────────────────┐  ┌──────────────────┐
│  🌟 WordBuddy                   │  │  SIDEBAR         │
│                                 │  │                  │
│  [Type a big word here...]  [→] │  │  ⭐ 7 points     │
│                                 │  │                  │
│  ┌─────────────────────────┐    │  │  Words I Learned │
│  │ in·tim·i·dat·ing        │    │  │  • enormous      │
│  │ (in-TIM-ih-day-ting)    │    │  │  • peculiar      │
│  │                         │    │  │  • intimidating  │
│  │ What it means:          │    │  └──────────────────┘
│  │ [definition]            │    │
│  │                         │    │
│  │ 📖 Examples             │    │
│  │ [example 1]             │    │
│  │ [example 2]             │    │
│  │                         │    │
│  │ 🧠 Think of it like...  │    │
│  │ [analogy]               │    │
│  │                         │    │
│  │ 💪 [encouragement]      │    │
│  │                         │    │
│  │ ❓ Practice question    │    │
│  │ [question]              │    │
│  │ [Answer box]   [Submit] │    │
│  └─────────────────────────┘    │
└─────────────────────────────────┘
```

UI constraints:
- Font size: use `st.markdown` with `##`/`###` headings for large text; no `st.write` for primary content
- Color: use `st.success`, `st.info`, `st.balloons` for positive feedback; avoid `st.error` for child-facing messages
- Sidebar always visible; points and word list update on every rerun

---

## 11. Five-Day Implementation Order

### Day 1 — Foundation
**Intent:** Get the skeleton running end-to-end with no LLM.

- [ ] Create `.bobignore`, `requirements.txt`
- [ ] Implement `src/session.py` (add_word, add_points, get_learned_words, get_points)
- [ ] Implement `src/fallback.py` with all ~50 words and schema-compliant dicts
- [ ] Smoke test: `pytest tests/test_wordbuddy.py`

### Day 2 — Prompts + LLM plumbing
**Intent:** Wire up the LLM call with full validation; app still uses fallback for most words.

- [ ] Implement `src/prompts.py` (system prompt + user prompt template)
- [ ] Implement `src/llm.py` (API call, JSON parse, schema validation, raises on failure)
- [ ] Unit tests in `tests/test_wordbuddy.py`: valid response, malformed JSON, missing keys, content blocklist
- [ ] Smoke test: `pytest tests/test_wordbuddy.py`

### Day 3 — Streamlit UI
**Intent:** Build the full UI wired to real modules; all 7 fields displayed.

- [ ] Implement `app.py`: input box, display card (7 fields), sidebar (points + word list)
- [ ] Wire input validation (empty, >60 chars) through `src/session.py`
- [ ] Wire LLM → fallback flow; never show raw errors to child
- [ ] Manual walkthrough: explain 3 words, verify UI, verify session state updates

### Day 4 — Practice question + points
**Intent:** Complete the gamification loop.

- [ ] Add answer input + Submit button to the word card in `app.py`
- [ ] Wire `+2` points through `src/session.py` on non-empty answer submission
- [ ] Add `st.balloons()` or `st.success` celebration on answer submission
- [ ] Test full flow: word explained (+1), answer submitted (+2), sidebar updates

### Day 5 — Polish + demo prep
**Intent:** Demo-ready hardening; nothing new added.

- [ ] Run full test suite; fix any failures
- [ ] Test offline mode: disable API key, verify fallback fires for known and unknown words
- [ ] Verify all acceptance criteria (section 13 below)
- [ ] Write one-paragraph demo script in `docs/DEMO.md`

---

## 12. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM returns unsafe content for a child-submitted word | Medium | High | System prompt blocklist + schema content validation in `src/llm.py`; fallback fires on any blocked content |
| API cost overrun during demo | Low | Medium | Add a per-session call counter; warn (don't block) after 20 calls |
| Empty or nonsense input reaching the API | High | Low | Block in UI before any API call; validate in `src/session.py` |
| LLM ignores JSON schema, returns prose | Medium | Medium | `src/llm.py` always wraps parse+validate; fallback fires immediately — user never sees raw LLM output |
| API key missing in demo environment | Low | High | `src/llm.py` checks env var at startup; shows a clear setup message, not a Python traceback |
| Fallback word not in offline dict | Medium | Low | Generic warm "Ask a grown-up!" response; never an error |

---

## 13. Acceptance Criteria (Demo)

The MVP is demo-ready when all of the following pass:

- [ ] A child can type a word and receive all 7 fields displayed in the UI within 5 seconds
- [ ] Points increment by +1 after a word is explained; sidebar updates immediately
- [ ] Points increment by +2 after the child submits a non-empty practice answer
- [ ] The "Words I've Learned" sidebar list grows with each explained word
- [ ] Disabling the API key causes the fallback to fire silently — the child sees a valid explanation, not an error
- [ ] Typing a word not in the fallback dict with no API key shows the generic "Ask a grown-up!" message, not a Python traceback
- [ ] Empty input is blocked before any API call with a friendly message
- [ ] All UI copy (labels, messages, errors) is readable by a 2nd–3rd grader
- [ ] No adult content, medical language, or shaming language appears in any output
- [ ] `pytest tests/` passes with no failures

