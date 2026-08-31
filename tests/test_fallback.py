"""
Unit tests for src/fallback.py.
Run with: pytest tests/test_fallback.py
"""

import pytest

from src.fallback import FALLBACK_DICT, GENERIC_FALLBACK, lookup

# The 7 keys every response must have
REQUIRED_KEYS = {
    "syllables",
    "pronunciation_hint",
    "definition",
    "examples",
    "analogy",
    "encouragement",
    "practice_question",
}


# ---------------------------------------------------------------------------
# Schema compliance
# ---------------------------------------------------------------------------
class TestSchema:
    def test_all_fallback_entries_have_required_keys(self):
        for word, entry in FALLBACK_DICT.items():
            missing = REQUIRED_KEYS - entry.keys()
            assert not missing, f"'{word}' is missing keys: {missing}"

    def test_all_fallback_examples_are_lists_of_two(self):
        for word, entry in FALLBACK_DICT.items():
            examples = entry["examples"]
            assert isinstance(examples, list), f"'{word}': examples is not a list"
            assert len(examples) == 2, f"'{word}': examples must have exactly 2 items"

    def test_all_fallback_strings_are_non_empty(self):
        string_keys = REQUIRED_KEYS - {"examples"}
        for word, entry in FALLBACK_DICT.items():
            for key in string_keys:
                assert isinstance(entry[key], str), f"'{word}': {key} is not a str"
                assert entry[key].strip(), f"'{word}': {key} is empty"

    def test_generic_fallback_has_required_keys(self):
        missing = REQUIRED_KEYS - GENERIC_FALLBACK.keys()
        assert not missing, f"GENERIC_FALLBACK missing keys: {missing}"

    def test_generic_fallback_examples_are_list_of_two(self):
        examples = GENERIC_FALLBACK["examples"]
        assert isinstance(examples, list)
        assert len(examples) == 2


# ---------------------------------------------------------------------------
# Lookup behaviour
# ---------------------------------------------------------------------------
class TestLookup:
    def test_known_word_exact_match(self):
        result = lookup("enormous")
        assert result["syllables"] == "e·nor·mous"

    def test_known_word_case_insensitive(self):
        result = lookup("ENORMOUS")
        assert result["syllables"] == "e·nor·mous"

    def test_known_word_with_leading_trailing_spaces(self):
        result = lookup("  enormous  ")
        # lookup strips on lower match
        assert result["syllables"] == "e·nor·mous"

    def test_unknown_word_returns_generic_fallback(self):
        result = lookup("xyzzy_notaword_12345")
        assert result is GENERIC_FALLBACK

    def test_all_ten_sample_words_are_reachable(self):
        sample_words = [
            "enormous", "peculiar", "ferocious", "transparent", "exhausted",
            "collaborate", "magnificent", "reluctant", "suspicious", "vocabulary",
        ]
        for word in sample_words:
            result = lookup(word)
            assert result is not GENERIC_FALLBACK, f"'{word}' unexpectedly returned generic fallback"

    def test_lookup_result_always_has_required_keys(self):
        for word in ["enormous", "nonexistent_word_xyz"]:
            result = lookup(word)
            missing = REQUIRED_KEYS - result.keys()
            assert not missing, f"lookup('{word}') result missing keys: {missing}"
