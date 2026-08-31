"""
pages/hangman.py — Rocket Launch word-guessing game for WordBuddy.

Rules:
- The word comes from the child's "Words I've Learned" list for this session.
- Child guesses one letter at a time by pressing a letter button.
- Max 6 wrong guesses before the rocket launches without them.
- No hanging-person graphics — a rocket builds and launches instead.
- Wrong guess = rocket loses a stage. Win = confetti + token reward.
"""

import streamlit as st

import src.session as session
from src.hangman import (
    MAX_MISSES,
    is_lost,
    is_won,
    letters_remaining,
    mask_word,
    rocket_art,
)

# ---------------------------------------------------------------------------
# Page CSS (scoped additions — base CSS is injected by app.py)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .rocket-box {
        background: #0f172a;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        font-family: monospace;
        font-size: 1.3rem;
        line-height: 1.5;
        color: #f8fafc;
        white-space: pre;
        text-align: center;
        min-height: 9rem;
    }
    .word-display {
        font-size: 2.2rem;
        letter-spacing: 0.25em;
        font-weight: 700;
        color: #1f2328;
        text-align: center;
        padding: 0.6rem 0;
    }
    .miss-counter {
        font-size: 1rem;
        color: #b45309;
        font-weight: 600;
        text-align: center;
    }
    .letter-btn > button {
        font-size: 1.1rem !important;
        padding: 0.3rem 0.5rem !important;
        border-radius: 8px !important;
        min-width: 2.6rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session-state keys (namespaced to avoid clashing with word-buddy keys)
# ---------------------------------------------------------------------------
_K_WORD    = "hm_word"
_K_GUESSED = "hm_guessed"
_K_MISSES  = "hm_misses"
_K_OVER    = "hm_over"
_K_REWARDED = "hm_rewarded"


def _init_game(word: str) -> None:
    st.session_state[_K_WORD]     = word.lower()
    st.session_state[_K_GUESSED]  = set()
    st.session_state[_K_MISSES]   = 0
    st.session_state[_K_OVER]     = False
    st.session_state[_K_REWARDED] = False


def _game_active() -> bool:
    return _K_WORD in st.session_state and not st.session_state.get(_K_OVER, True)


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.markdown("# 🚀 Rocket Launch")
st.markdown("#### Guess the letters before the rocket launches without you!")

# ---------------------------------------------------------------------------
# Word-picker — uses learned words from this session
# ---------------------------------------------------------------------------
learned = session.get_learned_words()

if not learned:
    st.info(
        "📖 You have not learned any words yet this session!  \n"
        "Go to **🌟 Word Buddy** and look up a few words first, "
        "then come back here to play.",
        icon="💡",
    )
    st.stop()

# Sidebar: word selector + new game button
with st.sidebar:
    st.markdown("### 🚀 Pick a word to guess")
    chosen = st.selectbox(
        "Choose a word",
        options=learned,
        label_visibility="collapsed",
        key="hm_pick",
    )
    if st.button("New game ▶", use_container_width=True, key="hm_new"):
        _init_game(chosen)
        st.rerun()

# Auto-start a game if none is running or the word changed
current_hm_word = st.session_state.get(_K_WORD, "")
if not _game_active() or (
    chosen
    and chosen.lower() != current_hm_word
    and not st.session_state.get(_K_OVER, False)
):
    _init_game(chosen)

# ---------------------------------------------------------------------------
# Read game state
# ---------------------------------------------------------------------------
word     = st.session_state[_K_WORD]
guessed  = st.session_state[_K_GUESSED]
misses   = st.session_state[_K_MISSES]
over     = st.session_state[_K_OVER]

masked   = mask_word(word, guessed)
won      = is_won(word, guessed)
lost     = is_lost(misses)

# ---------------------------------------------------------------------------
# Layout: rocket | word display
# ---------------------------------------------------------------------------
col_rocket, col_game = st.columns([1, 2], gap="large")

with col_rocket:
    st.markdown(
        f'<div class="rocket-box">{rocket_art(misses)}</div>',
        unsafe_allow_html=True,
    )
    lives_left = MAX_MISSES - misses
    if not over:
        st.markdown(
            f'<p class="miss-counter">'
            f'{"❤️" * lives_left}{"🖤" * misses}'
            f"</p>",
            unsafe_allow_html=True,
        )

with col_game:
    # Word display
    st.markdown(
        f'<div class="word-display">{masked}</div>',
        unsafe_allow_html=True,
    )

    # Wrong-letter list
    wrong = sorted(ch for ch in guessed if ch not in word)
    if wrong:
        st.caption(f"Letters that were not in the word: {' '.join(wrong)}")

    st.markdown("<br>", unsafe_allow_html=True)

    # — Game-over states —
    if won:
        # Fire balloons exactly once: _K_REWARDED flips True on the same rerun
        # that sets _K_OVER, so subsequent reruns skip both.
        if not st.session_state.get(_K_REWARDED):
            st.balloons()
            session.add_points(3)
            st.session_state[_K_REWARDED] = True
            st.session_state[_K_OVER] = True
            st.rerun()
        st.markdown(
            '<div class="cheer-banner">🎉 You guessed it! Amazing work! +3 tokens 🚀</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Press **New game ▶** in the sidebar to play again.")

    elif lost:
        st.markdown(
            f'<div style="background:#fef9c3;border:2px solid #f59e0b;'
            f'border-radius:14px;padding:0.8rem 1.2rem;font-size:1.1rem">'
            f"The rocket launched without you this time! 🚀<br>"
            f"The word was: <strong>{word}</strong><br>"
            f"Now you know it — you can do it next time! 💪"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.session_state[_K_OVER] = True
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Press **New game ▶** in the sidebar to try again.")

    # — Letter buttons (only shown while game is in progress) —
    else:
        remaining = letters_remaining(guessed)
        # Split into first-half (a–m) and second-half (n–z) for two clean rows
        first_half  = [c for c in remaining if c <= "m"]
        second_half = [c for c in remaining if c > "m"]

        for row in (first_half, second_half):
            if not row:
                continue
            cols = st.columns(len(row))
            for col, letter in zip(cols, row):
                with col:
                    if st.button(
                        letter.upper(),
                        key=f"hm_letter_{letter}",
                        use_container_width=True,
                    ):
                        guessed.add(letter)
                        if letter not in word:
                            st.session_state[_K_MISSES] += 1
                        st.session_state[_K_GUESSED] = guessed
                        st.rerun()
