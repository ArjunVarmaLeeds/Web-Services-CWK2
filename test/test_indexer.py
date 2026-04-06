import os
import json
import pytest

from src.indexer import Indexer


# -------------------------
# Test tokenize
# -------------------------
def test_tokenize_basic():
    indexer = Indexer()

    text = "Hello World"
    tokens = indexer.tokenize(text)

    assert tokens == ["hello", "world"]


# -------------------------
# Test add_document (single word)
# -------------------------
def test_add_document_single_word():
    indexer = Indexer()

    indexer.add_document("page1", "hello")

    assert "hello" in indexer.index
    assert "page1" in indexer.index["hello"]
    assert indexer.index["hello"]["page1"]["frequency"] == 1
    assert indexer.index["hello"]["page1"]["positions"] == [0]


# -------------------------
# Test add_document (multiple words + positions)
# -------------------------
def test_add_document_multiple_words():
    indexer = Indexer()

    indexer.add_document("page1", "good good friends")

    assert indexer.index["good"]["page1"]["frequency"] == 2
    assert indexer.index["good"]["page1"]["positions"] == [0, 1]

    assert indexer.index["friends"]["page1"]["frequency"] == 1
    assert indexer.index["friends"]["page1"]["positions"] == [2]


# -------------------------
# Test multiple documents
# -------------------------
def test_add_multiple_documents():
    indexer = Indexer()

    indexer.add_document("page1", "good friends")
    indexer.add_document("page2", "good people")

    assert "good" in indexer.index
    assert "page1" in indexer.index["good"]
    assert "page2" in indexer.index["good"]

    assert indexer.index["good"]["page1"]["frequency"] == 1
    assert indexer.index["good"]["page2"]["frequency"] == 1


# -------------------------
# Test build_index
# -------------------------
def test_build_index():
    indexer = Indexer()

    crawler_data = [
        {
            "url": "page1",
            "quotes": [{"text": "good friends"}]
        },
        {
            "url": "page2",
            "quotes": [{"text": "good people"}]
        }
    ]

    index = indexer.build_index(crawler_data)

    assert "good" in index
    assert "friends" in index
    assert "people" in index

    assert "page1" in index["good"]
    assert "page2" in index["good"]


# -------------------------
# Test empty input
# -------------------------
def test_build_index_empty():
    indexer = Indexer()

    index = indexer.build_index([])

    assert index == {}


# -------------------------
# Test save_index
# -------------------------
def test_save_index(tmp_path):
    indexer = Indexer()

    # Build simple index
    indexer.add_document("page1", "hello world")

    file_path = tmp_path / "test_index.json"

    indexer.save_index(file_path)

    # Check file exists
    assert os.path.exists(file_path)

    # Load and verify content
    with open(file_path, "r") as f:
        data = json.load(f)

    assert "hello" in data
    assert "page1" in data["hello"]
    assert data["hello"]["page1"]["frequency"] == 1


# -------------------------
# Test case insensitivity
# -------------------------
def test_case_insensitivity():
    indexer = Indexer()

    indexer.add_document("page1", "Good good GOOD")

    assert "good" in indexer.index
    assert indexer.index["good"]["page1"]["frequency"] == 3


# -------------------------
# Test positions correctness
# -------------------------
def test_positions_correct():
    indexer = Indexer()

    indexer.add_document("page1", "a b a")

    assert indexer.index["a"]["page1"]["positions"] == [0, 2]