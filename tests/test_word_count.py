"""Tests for the word count Spark job."""

import pytest
from jobs.word_count import word_count, filter_by_min_count


class TestWordCount:
    """Tests for word_count function."""

    def test_basic_word_count(self, spark):
        """Test basic word counting functionality."""
        text_data = ["hello world", "hello spark"]

        result = word_count(spark, text_data)

        assert result["hello"] == 2
        assert result["world"] == 1
        assert result["spark"] == 1

    def test_empty_input(self, spark):
        """Test with empty input."""
        result = word_count(spark, [])

        assert result == {}

    def test_case_insensitivity(self, spark):
        """Test that word counting is case insensitive."""
        text_data = ["Hello HELLO hello"]

        result = word_count(spark, text_data)

        assert result["hello"] == 3

    def test_multiple_spaces(self, spark):
        """Test handling of multiple spaces."""
        text_data = ["hello    world"]

        result = word_count(spark, text_data)

        assert result["hello"] == 1
        assert result["world"] == 1


class TestFilterByMinCount:
    """Tests for filter_by_min_count function."""

    def test_filter_words(self):
        """Test filtering words by minimum count."""
        word_counts = {"hello": 5, "world": 2, "spark": 1}

        result = filter_by_min_count(word_counts, 2)

        assert result == {"hello": 5, "world": 2}

    def test_filter_all(self):
        """Test when all words are filtered out."""
        word_counts = {"hello": 1, "world": 1}

        result = filter_by_min_count(word_counts, 5)

        assert result == {}

    def test_filter_none(self):
        """Test when no words are filtered out."""
        word_counts = {"hello": 5, "world": 5}

        result = filter_by_min_count(word_counts, 1)

        assert result == {"hello": 5, "world": 5}
