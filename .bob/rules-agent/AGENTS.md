# AGENTS.md (Agent mode)

This file provides guidance to agents when working with code in this repository.

## Pre-flight

- Create `.bobignore` if it doesn't exist; it must include `.env`.
- Never hardcode API keys — `os.environ` only.

## Module responsibilities (do not blur these boundaries)

| File | Owns |
|---|---|
| `app.py` | Streamlit UI wiring only — no business logic |
| `src/llm.py` | All LLM calls — always returns parsed, validated JSON dict |
| `src/prompts.py` | Every prompt string — no prompt construction elsewhere |
| `src/fallback.py` | Fallback content when LLM errors or output fails validation |
| `src/session.py` | All `st.session_state` reads/writes (learned words, token points) |

## Coding rules

- LLM responses must be validated as structured JSON before any downstream use; on failure, call `src/fallback.py`.
- All user-facing strings must be written at a 4th/5th grade reading level.
- No adult content, medical diagnoses, or shaming language — anywhere, including error messages.
- Token points and learned-word list live exclusively in `src/session.py`; do not access `st.session_state` directly from `app.py` or other modules.
- UI uses large text and color; prefer Streamlit native widgets/theming over injected HTML/CSS.

## Test commands

```bash
pytest tests/path/to/test_file.py::test_name   # single test
pytest tests/                                   # full suite
```
