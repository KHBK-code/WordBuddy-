"""
WordBuddy — Streamlit entry point and shared shell.

Responsibilities of this file:
1. set_page_config (must be first)
2. Register navigation pages via st.navigation
3. Inject shared CSS
4. Render the shared sidebar (tokens, prizes, words-of-the-week, word list)
5. Run the active page with _pg.run()

All word-explanation UI lives in pages/word_buddy.py.
All game UI lives in pages/hangman.py.
All LLM calls go through src/llm.explain_word().
"""

import json
import datetime
from pathlib import Path

import streamlit as st

import src.session as session

# ---------------------------------------------------------------------------
# Word-of-the-week helpers (used in sidebar, shared across pages)
# ---------------------------------------------------------------------------
_WOTW_PATH = Path(__file__).parent / "data" / "words_of_the_week.json"


def _load_wotw() -> list[dict]:
    with _WOTW_PATH.open(encoding="utf-8") as f:
        return json.load(f)["weeks"]


def _current_week_entry(weeks: list[dict]) -> dict:
    iso_week = datetime.date.today().isocalendar()[1]
    return weeks[(iso_week - 1) % len(weeks)]


# ---------------------------------------------------------------------------
# Page config — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="WordBuddy",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Navigation — defines the two pages; sidebar nav is rendered automatically
# ---------------------------------------------------------------------------
_pg = st.navigation(
    [
        st.Page("pages/word_buddy.py", title="Word Buddy",    icon="🌟", default=True),
        st.Page("pages/farm.py",       title="Word Farm",     icon="🌾"),
        st.Page("pages/hangman.py",    title="Rocket Launch", icon="🚀"),
    ],
    position="sidebar",
)

# ---------------------------------------------------------------------------
# Global CSS — large font, rounded cards, kid-friendly palette, hide chrome
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Hide the Streamlit top bar and footer */
    #MainMenu, footer, header {visibility: hidden;}

    /* Base font size bump */
    html, body, [class*="css"] {
        font-size: 18px;
    }

    /* Large heading sizes */
    h1 { font-size: 2.6rem !important; }
    h2 { font-size: 2.0rem !important; }
    h3 { font-size: 1.5rem !important; }

    /* Input and button sizing */
    .stTextInput > div > div > input {
        font-size: 1.3rem !important;
        padding: 0.6rem 1rem !important;
        border-radius: 12px !important;
        border: 2px solid #7c5cd8 !important;
    }
    .stButton > button {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.4rem !important;
        border-radius: 14px !important;
        background-color: #7c5cd8 !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #5a3eb5 !important;
    }

    /* Word card container */
    .word-card {
        background: #f0ecff;
        border: 2.5px solid #7c5cd8;
        border-radius: 20px;
        padding: 1.6rem 2rem;
        margin-top: 1rem;
    }

    /* Section labels inside the card */
    .section-label {
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #5a3eb5;
        margin-bottom: 0.2rem;
    }

    /* Pronunciation badge */
    .pron-badge {
        display: inline-block;
        background: #7c5cd8;
        color: white;
        border-radius: 999px;
        padding: 0.25rem 1rem;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    /* Example sentences */
    .example-item {
        background: white;
        border-left: 5px solid #f59e0b;
        border-radius: 0 12px 12px 0;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.05rem;
        color: #1f2328;
    }

    /* Analogy block */
    .analogy-block {
        background: #fef3c7;
        border: 2px solid #f59e0b;
        border-radius: 14px;
        padding: 0.8rem 1.2rem;
        font-size: 1.1rem;
        color: #1f2328;
    }

    /* Encouragement banner */
    .cheer-banner {
        background: #d1fae5;
        border: 2px solid #10b981;
        border-radius: 14px;
        padding: 0.8rem 1.4rem;
        font-size: 1.15rem;
        font-weight: 600;
        color: #065f46;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] {
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session-state initialisation (shared keys used by both pages)
# ---------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "current_word" not in st.session_state:
    st.session_state.current_word = ""
if "answer_accepted" not in st.session_state:
    st.session_state.answer_accepted = False
if "prefill_word" not in st.session_state:
    st.session_state.prefill_word = ""

# ---------------------------------------------------------------------------
# Shared sidebar — rendered once, visible on all pages
# ---------------------------------------------------------------------------
with st.sidebar:
    # Parents & teachers note — top of sidebar so it is easy to find
    st.caption(
        "👋 **Parents & teachers:** WordBuddy helps children build vocabulary "
        "one word at a time. Every lookup, practice answer, and Rocket win "
        "earns tokens. Completely ad-free and child-safe."
    )
    st.divider()

    points = session.get_points()
    st.markdown(f"## ⭐ {points} token{'s' if points != 1 else ''}")
    st.caption("+1 word lookup · +2 practice answer · +3 Rocket win")

    # Prize ladder
    prize = session.get_prize(points)
    if prize:
        emoji, label = prize
        st.markdown(f"### {emoji} {label}!")
    nxt = session.next_prize(points)
    if nxt:
        needed, nxt_emoji, nxt_label = nxt
        st.caption(
            f"{needed} more token{'s' if needed != 1 else ''} "
            f"to earn the {nxt_emoji} {nxt_label}"
        )
    st.divider()

    # Word of the week (only shown on Word Buddy page to avoid cluttering Hangman)
    if _pg.title == "Word Buddy":
        try:
            _weeks = _load_wotw()
            _entry = _current_week_entry(_weeks)
            st.markdown(f"### 📅 Week {_entry['week']}: {_entry['theme']}")
            for item in _entry["words"]:
                col_w, col_b = st.columns([3, 2])
                with col_w:
                    st.markdown(f"**{item['word']}**")
                    st.caption(item["hint"])
                with col_b:
                    if st.button(
                        "Try it ✨",
                        key=f"wotw_{item['word']}",
                        use_container_width=True,
                    ):
                        st.session_state.prefill_word = item["word"]
                        st.rerun()
        except Exception:
            pass
        st.divider()

    learned = session.get_learned_words()
    st.markdown("### 📚 Words I've Learned")
    if learned:
        for w in learned:
            st.markdown(f"• **{w}**")
    else:
        st.caption("No words yet — look one up!")

# ---------------------------------------------------------------------------
# Run the active page
# ---------------------------------------------------------------------------
_pg.run()
