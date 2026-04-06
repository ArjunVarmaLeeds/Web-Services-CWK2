"""
Search Engine Module

This module provides a Search class that performs text queries on an inverted index.
It supports exact word lookups, AND queries, and TF-IDF based ranking.
"""

from typing import Dict, List, Tuple, Any
import re
import math


class Search:
    """
    Performs search operations on an inverted index.

    This class provides methods for querying the index, including word lookups,
    boolean AND queries, and ranked searches using TF-IDF scoring.

    Attributes:
        index (Dict[str, Dict[str, Dict[str, Any]]]): The inverted index to search.
    """

    def __init__(self, index: Dict[str, Dict[str, Dict[str, Any]]]) -> None:
        """
        Initialize the Search with an inverted index.

        Args:
            index (Dict[str, Dict[str, Dict[str, Any]]]): The inverted index
                built by the Indexer.
        """
        self.index = index

    def normalize(self, word: str) -> str:
        """
        Normalize a word to lowercase for case-insensitive search.

        Args:
            word (str): The word to normalize.

        Returns:
            str: The normalized (lowercased) word.
        """
        return word.lower()

    def process_query(self, text: str) -> List[str]:
        """
        Process a query string into a list of normalized words.

        This method tokenizes the input text and normalizes each word.

        Args:
            text (str): The query text to process.

        Returns:
            List[str]: A list of normalized word tokens.
        """
        return re.findall(r"\b\w+\b", text.lower())

    def print_word(self, word: str) -> Dict[str, Dict[str, Any]]:
        """
        Return the inverted index entry for a specific word.

        This method retrieves the frequency and position data for a word
        across all documents in the index.

        Args:
            word (str): The word to look up.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary mapping URLs to their
                frequency and position data for the word. Empty if not found.
        """
        word = self.normalize(word)

        if word not in self.index:
            return {}

        return self.index[word]

    def find(self, query: List[str]) -> List[str]:
        """
        Find documents containing ALL query words (AND query).

        This method performs a boolean AND search, returning only documents
        that contain every word in the query.

        Args:
            query (List[str]): List of words to search for.

        Returns:
            List[str]: List of URLs that contain all query words.
                Empty if no matches or if any word is not in the index.
        """
        if not query:
            return []

        words = self.process_query(" ".join(query))

        # collect sets of pages
        page_sets = []

        for word in words:
            if word not in self.index:
                return []  # if any word missing → no result

            page_sets.append(set(self.index[word].keys()))

        # intersection of all sets
        results = set.intersection(*page_sets)

        return list(results)

    def find_with_ranking(self, query: List[str]) -> List[Tuple[str, float]]:
        """
        Find documents containing query words and rank by TF-IDF score.

        This method performs a ranked search using Term Frequency-Inverse
        Document Frequency (TF-IDF) scoring. Documents are ranked by their
        relevance score, with higher scores indicating better matches.

        Args:
            query (List[str]): List of words to search for.

        Returns:
            List[Tuple[str, float]]: List of (URL, score) tuples, sorted
                by score in descending order. Empty if no matches or
                if any word is not in the index.
        """
        if not query:
            return []

        words = self.process_query(" ".join(query))
        N = len({url for word in self.index for url in self.index[word]})

        scores: Dict[str, float] = {}

        for word in words:
            if word not in self.index:
                return []

            df = len(self.index[word])  # document frequency
            idf = math.log((N + 1) / (df + 1)) + 1  # smoothed IDF

            for url, data in self.index[word].items():
                tf = data["frequency"]

                if url not in scores:
                    scores[url] = 0

                scores[url] += tf * idf

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)