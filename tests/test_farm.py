"""
tests/test_farm.py

Unit tests for src/farm.py pure helpers.
Run with:  pytest tests/test_farm.py -v
"""

from __future__ import annotations

import pytest

from src.farm import GRID_COLS, animal_for_index, build_farm


# ---------------------------------------------------------------------------
# animal_for_index
# ---------------------------------------------------------------------------
class TestAnimalForIndex:
    def test_returns_string(self):
        assert isinstance(animal_for_index(0), str)

    def test_index_zero_is_first_animal(self):
        # First animal must be a non-empty emoji string
        a = animal_for_index(0)
        assert len(a) >= 1

    def test_different_indices_give_different_animals(self):
        animals = [animal_for_index(i) for i in range(10)]
        # All ten should be distinct (roster has 20 unique entries)
        assert len(set(animals)) == 10

    def test_cycles_after_20(self):
        # index 20 should wrap back to index 0
        assert animal_for_index(20) == animal_for_index(0)

    def test_cycles_at_arbitrary_large_index(self):
        assert animal_for_index(105) == animal_for_index(105 % 20)

    def test_never_raises_for_large_index(self):
        for i in range(0, 200, 7):
            animal_for_index(i)  # must not raise


# ---------------------------------------------------------------------------
# build_farm
# ---------------------------------------------------------------------------
class TestBuildFarm:
    def test_empty_words_returns_empty_list(self):
        assert build_farm([]) == []

    def test_single_word_returns_one_pair(self):
        result = build_farm(["cat"])
        assert len(result) == 1
        animal, word = result[0]
        assert word == "cat"
        assert isinstance(animal, str) and len(animal) >= 1

    def test_five_words_returns_five_pairs(self):
        words = ["alpha", "beta", "gamma", "delta", "epsilon"]
        result = build_farm(words)
        assert len(result) == 5

    def test_words_preserved_in_order(self):
        words = ["apple", "banana", "cherry"]
        result = build_farm(words)
        assert [w for _, w in result] == words

    def test_each_pair_is_tuple_of_two_strings(self):
        for animal, word in build_farm(["hello", "world"]):
            assert isinstance(animal, str)
            assert isinstance(word, str)

    def test_animals_are_non_empty(self):
        for animal, _ in build_farm(["x", "y", "z"]):
            assert len(animal) >= 1

    def test_twenty_words_all_distinct_animals(self):
        words = [f"word{i}" for i in range(20)]
        animals = [a for a, _ in build_farm(words)]
        assert len(set(animals)) == 20

    def test_twenty_one_words_wraps_animal(self):
        words = [f"word{i}" for i in range(21)]
        result = build_farm(words)
        # 21st animal (index 20) wraps to same as first (index 0)
        assert result[20][0] == result[0][0]

    def test_duplicate_words_each_get_own_animal(self):
        # build_farm doesn't deduplicate — that's session.add_word's job
        result = build_farm(["same", "same", "same"])
        assert len(result) == 3


# ---------------------------------------------------------------------------
# GRID_COLS constant
# ---------------------------------------------------------------------------
class TestGridCols:
    def test_grid_cols_is_five(self):
        assert GRID_COLS == 5

    def test_grid_cols_is_positive_int(self):
        assert isinstance(GRID_COLS, int)
        assert GRID_COLS > 0
