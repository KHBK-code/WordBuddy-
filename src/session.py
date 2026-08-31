"""
All st.session_state reads and writes for WordBuddy.
app.py must never access st.session_state directly — use these helpers.
"""

import streamlit as st

_KEY_WORDS = "learned_words"
_KEY_POINTS = "token_points"

# Prize ladder: (threshold, emoji, label)
_PRIZES = [
    (20, "🥇", "Gold Star"),
    (10, "🥈", "Silver Star"),
    (5,  "🥉", "Bronze Star"),
]


def _init() -> None:
    """Initialise state keys if they don't exist yet.
    Safe to call on every Streamlit rerun.
    """
    if _KEY_WORDS not in st.session_state:
        st.session_state[_KEY_WORDS] = []
    if _KEY_POINTS not in st.session_state:
        st.session_state[_KEY_POINTS] = 0


def add_word(word: str) -> None:
    """Append a word to the learned-words list (no duplicates within session)."""
    _init()
    if word not in st.session_state[_KEY_WORDS]:
        st.session_state[_KEY_WORDS].append(word)


def add_points(n: int) -> None:
    """Add n token points to the session total."""
    _init()
    st.session_state[_KEY_POINTS] += n


def get_learned_words() -> list[str]:
    """Return the list of words learned this session, in order."""
    _init()
    return list(st.session_state[_KEY_WORDS])


def get_points() -> int:
    """Return the current token-point total."""
    _init()
    return st.session_state[_KEY_POINTS]


def get_prize(points: int) -> tuple[str, str] | None:
    """Return (emoji, label) for the highest prize earned, or None.

    Pure function — no session state access — so it is easy to unit-test.
    """
    for threshold, emoji, label in _PRIZES:
        if points >= threshold:
            return (emoji, label)
    return None


def next_prize(points: int) -> tuple[int, str, str] | None:
    """Return (tokens_needed, emoji, label) for the next prize, or None if all earned.

    Pure function.
    """
    for threshold, emoji, label in reversed(_PRIZES):
        if points < threshold:
            return (threshold - points, emoji, label)
    return None
