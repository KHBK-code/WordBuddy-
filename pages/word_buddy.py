"""
pages/word_buddy.py — Word explanation page.
Rendered by app.py via st.navigation / _pg.run().
"""

import streamlit as st

import src.session as session
from src.llm import explain_word

# ---------------------------------------------------------------------------
# Session-state initialisation (keys owned by this page)
# ---------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "current_word" not in st.session_state:
    st.session_state.current_word = ""
if "answer_accepted" not in st.session_state:
    st.session_state.answer_accepted = False
if "prefill_word" not in st.session_state:
    st.session_state.prefill_word = ""
# One-shot flag: balloons fired for the current accepted answer
if "balloons_fired" not in st.session_state:
    st.session_state.balloons_fired = False
# One-shot flag: token toast shown for the current lookup (+1)
if "lookup_toast_shown" not in st.session_state:
    st.session_state.lookup_toast_shown = False

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("# 🌟 WordBuddy")
st.markdown(
    "#### Your kind reading helper — type any tricky word and "
    "I will explain it just for you!"
)

# ---------------------------------------------------------------------------
# Input row  (wider button column so it does not squeeze on small screens)
# ---------------------------------------------------------------------------
col_input, col_btn = st.columns([4, 1], vertical_alignment="bottom")

# Consume any pending pre-fill from the Word-of-the-Week button
_prefill = st.session_state.pop("prefill_word", "") or ""

with col_input:
    word_input = st.text_input(
        label="Word to explain",
        placeholder='Try a tricky word like "enormous" …',
        max_chars=80,
        label_visibility="collapsed",
        key="word_input",
        value=_prefill,
    )

with col_btn:
    explain_clicked = st.button(
        "Explain it! ✨",
        use_container_width=True,
        type="primary",
    )

# ---------------------------------------------------------------------------
# Handle button click — call LLM once, store result, then rerun.
# Double-wrapped: explain_word() already guarantees no raises, but the outer
# try/except ensures no traceback ever reaches the UI.
# ---------------------------------------------------------------------------
if explain_clicked:
    word = word_input.strip()
    try:
        with st.spinner("Looking that up for you …"):
            result = explain_word(word)
    except Exception:  # noqa: BLE001 — absolute last line of defence
        from src.llm import _BRAVE_FALLBACK
        result = _BRAVE_FALLBACK
    st.session_state.result = result
    st.session_state.current_word = word
    st.session_state.answer_accepted = False
    st.session_state.balloons_fired = False
    st.session_state.lookup_toast_shown = False
    if result.get("syllables") != "?":
        session.add_word(word)
        session.add_points(1)
        # Re-fill the input with the same word so the child can see what they typed
        st.session_state.prefill_word = word
    st.rerun()

# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------
result = st.session_state.result
word   = st.session_state.current_word

if result is None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        '💡 **Type a tricky word above**, then press **Explain it!**  \n'
        'Try something like *photosynthesis*, *metamorphosis*, or *circumference*.',
        icon="📖",
    )
    st.stop()

# ---------------------------------------------------------------------------
# +1 token toast — shown once per new lookup
# ---------------------------------------------------------------------------
if not st.session_state.lookup_toast_shown and result.get("syllables") != "?":
    st.toast("⭐ +1 token for looking up a word!", icon="🌟")
    st.session_state.lookup_toast_shown = True

# ---------------------------------------------------------------------------
# Word card
# ---------------------------------------------------------------------------
st.markdown('<div class="word-card">', unsafe_allow_html=True)

# — Syllables & pronunciation —
st.markdown(f"## {result['syllables']}")
st.markdown(
    f'<span class="pron-badge">👄 {result["pronunciation_hint"]}</span>',
    unsafe_allow_html=True,
)

st.markdown("---")

# — Definition —
st.markdown('<p class="section-label">📖 What it means</p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:1.15rem'>{result['definition']}</p>", unsafe_allow_html=True)

st.markdown("---")

# — Examples —
st.markdown('<p class="section-label">💬 See it in a sentence</p>', unsafe_allow_html=True)
for ex in result["examples"]:
    st.markdown(f'<div class="example-item">{ex}</div>', unsafe_allow_html=True)

st.markdown("---")

# — Analogy —
st.markdown('<p class="section-label">🧠 Imagine it like this …</p>', unsafe_allow_html=True)
st.markdown(f'<div class="analogy-block">{result["analogy"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# — Encouragement —
st.markdown(
    f'<div class="cheer-banner">💪 {result["encouragement"]}</div>',
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)  # close .word-card

# ---------------------------------------------------------------------------
# Practice question
# ---------------------------------------------------------------------------
if result.get("syllables") != "?":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### ❓ {result['practice_question']}")

    if not st.session_state.answer_accepted:
        st.markdown(
            '<p style="font-size:1rem;font-weight:600;color:#5a3eb5;margin-bottom:0.2rem">'
            "Write your answer below — even one word counts! ✏️"
            "</p>",
            unsafe_allow_html=True,
        )
        answer = st.text_input(
            label="Your answer",
            placeholder="Type your answer here …",
            key=f"answer_{word}",
            label_visibility="collapsed",
        )
        if st.button("📬 Submit my answer!", key=f"submit_{word}"):
            if answer.strip():
                session.add_points(2)
                st.session_state.answer_accepted = True
                st.session_state.balloons_fired = False
                st.rerun()
            else:
                st.info("Write something — even one word counts! ✏️", icon="💡")
    else:
        # Fire balloons exactly once per accepted answer
        if not st.session_state.balloons_fired:
            st.balloons()
            st.session_state.balloons_fired = True

        st.markdown(
            '<div class="cheer-banner">🎉 Nice thinking! You earned 2 bonus tokens!</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            "🔤 Want to try another word? Type it in the box above and press **Explain it!**",
            icon="💡",
        )
