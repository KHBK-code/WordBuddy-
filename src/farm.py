"""
src/farm.py — Pure helpers for the Word Farm page.

Logic is kept here (not in the page) so it can be unit-tested without Streamlit.
"""

# Ordered list of farm animals assigned round-robin as words are learned.
_ANIMALS = [
    "🐔", "🐄", "🐑", "🐷", "🐴", "🐓", "🐇", "🦆", "🐐", "🐝",
    "🦃", "🐖", "🐈", "🐕", "🦙", "🐎", "🐂", "🦌", "🐿️", "🦔",
]

GRID_COLS = 5  # animals per row


def animal_for_index(index: int) -> str:
    """Return the animal emoji for the nth word (0-based), cycling if > 20 words."""
    return _ANIMALS[index % len(_ANIMALS)]


def build_farm(words: list[str]) -> list[tuple[str, str]]:
    """Return [(animal_emoji, word), ...] for all learned words, in order.

    Pure function — no session state, no Streamlit.
    """
    return [(animal_for_index(i), w) for i, w in enumerate(words)]
