# AGENTS.md (Plan mode)

This file provides guidance to agents when working with code in this repository.

## Architectural constraints

- **UI framework**: Streamlit — single-process, reruns on every interaction; design with Streamlit's execution model in mind.
- **State**: all session state (learned words, token points) managed in `src/session.py` via `st.session_state`; no external DB or cache planned yet.
- **LLM contract**: `src/llm.py` must always return a validated JSON dict — callers must never handle raw LLM text.
- **Prompt ownership**: `src/prompts.py` is the single source of truth for all prompts; changing tone/reading level means editing only this file.
- **Fallback layer**: `src/fallback.py` is a hard requirement, not optional — every LLM call path must have a fallback.
- **Secrets**: environment variables only; no secret-passing via function arguments or config objects.

## Audience constraints that affect design

- Primary: children 8–10 (4th/5th grade) — vocabulary, UI copy, and error messages must be age-appropriate.
- Secondary: parents and teachers — they may view session history or summaries.
- No medical diagnoses, no adult content, no shaming — these are content policy constraints, not just style.

## Open decisions

- LLM provider / SDK (IBM watsonx, OpenAI, etc.)
- Deployment target
- Whether parents/teachers get a separate view or the same UI
- Test strategy (unit vs integration vs Streamlit AppTest)
