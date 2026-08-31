"""
Pure game-logic helpers for the Hangman page.
No Streamlit imports — fully unit-testable.
"""

from __future__ import annotations

MAX_MISSES = 6

# Rocket launch stages — 0 misses = fully built, 6 = launched (game over)
# Each stage adds one part of the rocket silhouette using text art.
ROCKET_STAGES = [
    # 0 misses — full rocket on the pad, ready to go
    "    🚀\n   /||\\\n  / || \\\n |  ||  |\n  \\ || /\n   \\||/\n ===🔥===",
    # 1 miss — small flame flicker
    "    🚀\n   /||\\\n  / || \\\n |  ||  |\n  \\ || /\n   \\||/\n  ==🔥==",
    # 2 misses — rocket lifts slightly
    "    🚀\n   /||\\\n  / || \\\n |  ||  |\n  \\ || /\n   \\||/",
    # 3 misses — halfway up
    "    🚀\n   /||\\\n  / || \\\n |  ||  |",
    # 4 misses — nose cone only
    "    🚀\n   /||\\\n  / || \\",
    # 5 misses — just the tip
    "    🚀\n   /||\\",
    # 6 misses — rocket has launched! (game over)
    "  🚀💨\n\n(it launched\n without you!)",
]


def mask_word(word: str, guessed: set[str]) -> str:
    """Return the word with unguessed letters replaced by underscores.

    Spaces in the original word are preserved (for phrases).
    """
    return " ".join(
        ch if ch.lower() in guessed or not ch.isalpha() else "_"
        for ch in word
    )


def is_won(word: str, guessed: set[str]) -> bool:
    """Return True when every letter in *word* has been guessed."""
    return all(ch.lower() in guessed for ch in word if ch.isalpha())


def is_lost(misses: int) -> bool:
    """Return True when the miss count has reached the maximum."""
    return misses >= MAX_MISSES


def letters_remaining(guessed: set[str]) -> list[str]:
    """Return the alphabet letters not yet guessed, in order."""
    return [ch for ch in "abcdefghijklmnopqrstuvwxyz" if ch not in guessed]


def rocket_art(misses: int) -> str:
    """Return the rocket stage string for *misses* (clamped to valid range)."""
    idx = max(0, min(misses, len(ROCKET_STAGES) - 1))
    return ROCKET_STAGES[idx]
