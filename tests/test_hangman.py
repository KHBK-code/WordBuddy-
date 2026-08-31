"""
tests/test_hangman.py — unit tests for src/hangman.py pure functions.
No Streamlit needed.

Run with:  pytest tests/test_hangman.py -v
"""

from __future__ import annotations

import pytest

from src.hangman import (
    MAX_MISSES,
    ROCKET_STAGES,
    is_lost,
    is_won,
    letters_remaining,
    mask_word,
    rocket_art,
)


# ---------------------------------------------------------------------------
# mask_word
# ---------------------------------------------------------------------------
class TestMaskWord:
    def test_no_guesses_all_hidden(self):
        assert mask_word("cat", set()) == "_ _ _"

    def test_correct_guess_reveals_letter(self):
        assert mask_word("cat", {"c"}) == "c _ _"

    def test_all_guessed_reveals_word(self):
        assert mask_word("cat", {"c", "a", "t"}) == "c a t"

    def test_case_insensitive_reveal(self):
        # guessed set uses lowercase; word may have mixed case
        assert mask_word("Cat", {"c", "a", "t"}) == "C a t"

    def test_space_preserved(self):
        result = mask_word("big cat", set())
        assert " " in result  # space not replaced

    def test_non_alpha_chars_preserved(self):
        # hyphens, apostrophes should show as-is
        result = mask_word("photo-synthesis", {"p"})
        assert "-" in result
        assert result.startswith("p")

    def test_already_guessed_wrong_letter_still_hidden(self):
        result = mask_word("cat", {"z"})
        assert result == "_ _ _"

    def test_long_word(self):
        word = "photosynthesis"
        guessed = set("photsyne")
        result = mask_word(word, guessed)
        # 'i' not in guessed → should be underscore
        assert "_" in result
        # all guessed letters should appear
        for ch in guessed:
            if ch in word:
                assert ch in result


# ---------------------------------------------------------------------------
# is_won
# ---------------------------------------------------------------------------
class TestIsWon:
    def test_not_won_with_no_guesses(self):
        assert not is_won("cat", set())

    def test_not_won_partially_guessed(self):
        assert not is_won("cat", {"c", "a"})

    def test_won_exactly(self):
        assert is_won("cat", {"c", "a", "t"})

    def test_won_with_extra_guesses(self):
        assert is_won("cat", {"c", "a", "t", "z", "x"})

    def test_case_insensitive(self):
        assert is_won("Cat", {"c", "a", "t"})

    def test_single_letter_word(self):
        assert is_won("a", {"a"})
        assert not is_won("a", set())

    def test_phrase_with_space(self):
        # space is not alpha, so it is not required in guessed
        assert is_won("big cat", {"b", "i", "g", "c", "a", "t"})


# ---------------------------------------------------------------------------
# is_lost
# ---------------------------------------------------------------------------
class TestIsLost:
    def test_not_lost_at_zero(self):
        assert not is_lost(0)

    def test_not_lost_below_max(self):
        for i in range(MAX_MISSES):
            assert not is_lost(i)

    def test_lost_at_max(self):
        assert is_lost(MAX_MISSES)

    def test_lost_above_max(self):
        assert is_lost(MAX_MISSES + 1)
        assert is_lost(MAX_MISSES + 99)

    def test_max_misses_is_6(self):
        assert MAX_MISSES == 6


# ---------------------------------------------------------------------------
# letters_remaining
# ---------------------------------------------------------------------------
class TestLettersRemaining:
    def test_all_letters_at_start(self):
        remaining = letters_remaining(set())
        assert remaining == list("abcdefghijklmnopqrstuvwxyz")

    def test_guessed_letters_removed(self):
        remaining = letters_remaining({"a", "b", "c"})
        assert "a" not in remaining
        assert "b" not in remaining
        assert "c" not in remaining
        assert "d" in remaining

    def test_all_guessed_empty_list(self):
        all_letters = set("abcdefghijklmnopqrstuvwxyz")
        assert letters_remaining(all_letters) == []

    def test_result_is_sorted(self):
        remaining = letters_remaining({"m", "z"})
        assert remaining == sorted(remaining)

    def test_only_lowercase_returned(self):
        remaining = letters_remaining(set())
        assert all(c.islower() for c in remaining)


# ---------------------------------------------------------------------------
# rocket_art
# ---------------------------------------------------------------------------
class TestRocketArt:
    def test_returns_string(self):
        for i in range(MAX_MISSES + 1):
            assert isinstance(rocket_art(i), str)

    def test_zero_misses_is_first_stage(self):
        assert rocket_art(0) == ROCKET_STAGES[0]

    def test_max_misses_is_last_stage(self):
        assert rocket_art(MAX_MISSES) == ROCKET_STAGES[-1]

    def test_clamps_below_zero(self):
        assert rocket_art(-1) == ROCKET_STAGES[0]

    def test_clamps_above_max(self):
        assert rocket_art(MAX_MISSES + 5) == ROCKET_STAGES[-1]

    def test_stage_count_matches_max_plus_one(self):
        # One stage per miss state: 0, 1, 2, 3, 4, 5, 6
        assert len(ROCKET_STAGES) == MAX_MISSES + 1

    def test_each_stage_is_non_empty(self):
        for i, stage in enumerate(ROCKET_STAGES):
            assert stage.strip(), f"Stage {i} is empty"
