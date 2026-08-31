# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

**WordBuddy** — kid-friendly AI word explainer for children ages 8–10 (4th/5th grade), with secondary audience of parents and teachers. Built for the IBM AI Builders Challenge (Wildcard track).

## Stack

- Python 3.11
- Streamlit (UI framework)
- LLM via environment-configured API (structured JSON output required)

## Commands

```bash
# Install
pip install -r requirements.txt

# Run app
streamlit run app.py

# Test (single file)
pytest tests/path/to/test_file.py::test_name

# Lint / format
ruff check .
ruff format .
```

## Module layout

```
app.py          # Streamlit entry point only — wires UI to src/ modules
src/llm.py      # LLM calls; always returns structured JSON
src/prompts.py  # All prompt strings live here, nowhere else
src/fallback.py # Fallback responses when LLM fails or output is unsafe
src/session.py  # st.session_state helpers: learned-words list, token points
```

## Critical rules

- **API keys**: always via `os.environ` / `.env` — never hardcoded, never in source
- **LLM output**: must be structured JSON; parse and validate before use
- **Child-safe content**: short sentences, positive tone, no shame, no adult content, no medical diagnoses
- **Copy standard**: 4th/5th grade reading level throughout — UI labels, error messages, everything
- **UI**: colorful, large text; Streamlit's built-in theming/widgets preferred over custom HTML

## Secrets

- `.env` is already in `.gitignore`
- `.bobignore` must also list `.env` — create it if it doesn't exist
