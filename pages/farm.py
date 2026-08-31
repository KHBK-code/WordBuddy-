"""
pages/farm.py — Word Farm page for WordBuddy.

Every word the child looks up this session plants one animal on the farm.
Purely motivational — session only, no persistence.
"""

import streamlit as st

import src.session as session
from src.farm import GRID_COLS, build_farm

# ---------------------------------------------------------------------------
# Page-scoped CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .farm-header {
        background: #f0fdf4;
        border: 2.5px solid #10b981;
        border-radius: 20px;
        padding: 1rem 1.6rem;
        margin-bottom: 1.2rem;
    }
    .farm-cell {
        background: #f0fdf4;
        border: 2px solid #10b981;
        border-radius: 16px;
        text-align: center;
        padding: 0.7rem 0.4rem 0.4rem;
        font-size: 2.6rem;
        line-height: 1.2;
    }
    .farm-cell-word {
        font-size: 0.75rem;
        font-weight: 600;
        color: #065f46;
        word-break: break-word;
        margin-top: 0.2rem;
    }
    .farm-empty {
        background: #f7f8fa;
        border: 2px dashed #d1d5db;
        border-radius: 16px;
        text-align: center;
        padding: 0.7rem 0.4rem;
        font-size: 2.0rem;
        color: #d1d5db;
        line-height: 1.4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("# 🌾 Word Farm")
st.markdown(
    "#### Every word you learn plants a new animal on your farm!  \n"
    "Look up words on **🌟 Word Buddy** to grow your farm."
)

# ---------------------------------------------------------------------------
# Build farm from session
# ---------------------------------------------------------------------------
words = session.get_learned_words()
farm  = build_farm(words)
count = len(farm)

st.markdown('<div class="farm-header">', unsafe_allow_html=True)
if count == 0:
    st.markdown(
        "🌱 **Your farm is empty right now.**  \n"
        "Go to **🌟 Word Buddy**, look up any tricky word, and your first animal will appear here!"
    )
else:
    plural = "animal" if count == 1 else "animals"
    st.markdown(f"🐾 **You have {count} {plural} on your farm** — keep learning to grow it!")
st.markdown("</div>", unsafe_allow_html=True)

if not farm:
    st.stop()

# ---------------------------------------------------------------------------
# Render grid — GRID_COLS animals per row
# ---------------------------------------------------------------------------
for row_start in range(0, count, GRID_COLS):
    row_items = farm[row_start : row_start + GRID_COLS]
    cols = st.columns(GRID_COLS)
    for col_idx, col in enumerate(cols):
        with col:
            if col_idx < len(row_items):
                animal, word = row_items[col_idx]
                st.markdown(
                    f'<div class="farm-cell">'
                    f"{animal}"
                    f'<div class="farm-cell-word">{word}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
            else:
                # Empty placeholder to keep columns uniform
                st.markdown(
                    '<div class="farm-empty">·</div>',
                    unsafe_allow_html=True,
                )
