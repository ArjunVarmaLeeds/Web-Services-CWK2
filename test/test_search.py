import pytest
from src.search import Search


# -------------------------
# Sample index (fixture)
# -------------------------
@pytest.fixture
def sample_index():
    return {
        "good": {
            "page1": {"frequency": 2, "positions": [0, 1]},
            "page2": {"frequency": 1, "positions": [2]}
        },
        "friends": {
            "page1": {"frequency": 1, "positions": [2]}
        },
        "people": {
            "page2": {"frequency": 1, "positions": [0]}
        }
    }


# -------------------------
# Test print_word (exists)
# -------------------------
def test_print_word_exists(sample_index):
    search = Search(sample_index)

    result = search.print_word("good")

    assert "page1" in result
    assert result["page1"]["frequency"] == 2


# -------------------------
# Test print_word (not found)
# -------------------------
def test_print_word_not_found(sample_index):
    search = Search(sample_index)

    result = search.print_word("unknown")

    assert result == {}


# -------------------------
# Test find (single word)
# -------------------------
def test_find_single_word(sample_index):
    search = Search(sample_index)

    result = search.find(["good"])

    assert set(result) == {"page1", "page2"}


# -------------------------
# Test find (multiple words AND query)
# -------------------------
def test_find_multiple_words(sample_index):
    search = Search(sample_index)

    result = search.find(["good", "friends"])

    assert result == ["page1"] or set(result) == {"page1"}


# -------------------------
# Test find (no match)
# -------------------------
def test_find_no_match(sample_index):
    search = Search(sample_index)

    result = search.find(["friends", "people"])

    assert result == []


# -------------------------
# Test find (word not in index)
# -------------------------
def test_find_word_not_present(sample_index):
    search = Search(sample_index)

    result = search.find(["good", "unknown"])

    assert result == []


# -------------------------
# Test find (empty query)
# -------------------------
def test_find_empty_query(sample_index):
    search = Search(sample_index)

    result = search.find([])

    assert result == []


# -------------------------
# Test case insensitivity
# -------------------------
def test_case_insensitivity(sample_index):
    search = Search(sample_index)

    result = search.find(["GOOD"])

    assert set(result) == {"page1", "page2"}


# -------------------------
# Test find_with_ranking
# -------------------------
def test_find_with_ranking(sample_index):
    search = Search(sample_index)

    result = search.find_with_ranking(["good"])

    # page1 should rank higher (frequency 2 > 1)
    assert result[0][0] == "page1"
    assert result[0][1] >= result[1][1]


# -------------------------
# Test ranking with multiple words
# -------------------------
def test_find_with_ranking_multiple_words(sample_index):
    search = Search(sample_index)

    result = search.find_with_ranking(["good", "friends"])

    # page1 should be highest because it contains both
    assert result[0][0] == "page1"