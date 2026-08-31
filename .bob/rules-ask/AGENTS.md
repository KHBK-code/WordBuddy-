# AGENTS.md (Ask mode)

This file provides guidance to agents when working with code in this repository.

## Project context

**WordBuddy** — Streamlit + Python 3.11 app that uses an LLM to explain difficult words to children ages 8–10. Secondary audience: parents and teachers. IBM AI Builders Challenge (Wildcard).

## Module map (for answering "where does X live?")

| Module | Responsibility |
|---|---|
| `app.py` | Streamlit entry point; UI only |
| `src/llm.py` | LLM calls; returns structured JSON |
| `src/prompts.py` | All prompts |
| `src/fallback.py` | Safe fallback responses |
| `src/session.py` | `st.session_state`: learned words + token points |

## Non-obvious context

- The app does **not** have a database; persistence is in-session via `st.session_state`.
- LLM output is always JSON — questions about "parsing the response" apply to JSON, not raw text.
- Child-safe content rules apply to **all** user-facing strings, including error messages.
- No source files exist yet — the project is in the planning/scaffolding stage.
