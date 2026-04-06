"""
Inverted Index Builder Module

This module provides an Indexer class that builds an inverted index from
crawled web data. The index maps words to their occurrences across documents,
including frequency counts and positional information.
"""

import json
import re
from typing import Dict, List, Any


class Indexer:
    """
    Builds and manages an inverted index for text search.

    The inverted index structure is:
    {
        "word": {
            "url": {
                "frequency": int,
                "positions": List[int]
            }
        }
    }

    Attributes:
        index (Dict[str, Dict[str, Dict[str, Any]]]): The inverted index data structure.
    """

    def __init__(self) -> None:
        """Initialize an empty inverted index."""
        self.index: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into lowercase words using regex.

        This method extracts word tokens (sequences of word characters)
        and converts them to lowercase for case-insensitive indexing.

        Args:
            text (str): The text to tokenize.

        Returns:
            List[str]: A list of lowercase word tokens.
        """
        return re.findall(r"\b\w+\b", text.lower())

    def add_document(self, url: str, text: str) -> None:
        """
        Add a document's text to the inverted index.

        This method tokenizes the text and updates the index with word
        frequencies and positions for the given URL.

        Args:
            url (str): The URL of the document.
            text (str): The text content of the document.
        """
        words = self.tokenize(text)

        for position, word in enumerate(words):
            if word not in self.index:
                self.index[word] = {}

            if url not in self.index[word]:
                self.index[word][url] = {
                    "frequency": 0,
                    "positions": []
                }

            self.index[word][url]["frequency"] += 1
            self.index[word][url]["positions"].append(position)

    def build_index(self, crawler_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Build the inverted index from crawler data.

        This method processes the output from the Crawler, extracting
        quote text from each page and adding it to the index.

        Args:
            crawler_data (List[Dict[str, Any]]): Data from the Crawler,
                each dict containing "url" and "quotes".

        Returns:
            Dict[str, Dict[str, Dict[str, Any]]]: The complete inverted index.
        """
        for page in crawler_data:
            url = page["url"]

            for quote in page["quotes"]:
                self.add_document(url, quote["text"])

        return self.index

    def save_index(self, filename: str) -> None:
        """
        Save the inverted index to a JSON file.

        This method serializes the index to JSON format with indentation
        for readability and prints status messages.

        Args:
            filename (str): The path to the output file.
        """
        print("\n" + "="*60)
        print("Saving index to file")
        print("="*60)
        with open(filename, "w") as f:
            json_index = {
                word: {
                    url: {
                        "frequency": data["frequency"],
                        "positions": data["positions"]
                    }
                    for url, data in urls.items()
                }
                for word, urls in self.index.items()
            }
            json.dump(json_index, f, indent=2)
        print(f"✓ Index saved to {filename}")