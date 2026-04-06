from typing import Dict, List
import re
import math

class Search:
    def __init__(self, index: Dict):
        self.index = index

    def normalize(self, word: str) -> str:
        return word.lower()
    
    def process_query(self, text: str):
        return re.findall(r"\b\w+\b", text.lower())

    def print_word(self, word: str) -> Dict:
        """
        Return inverted index entry for a word.
        """
        word = self.normalize(word)

        if word not in self.index:
            return {}

        return self.index[word]

    def find(self, query: List[str]) -> List[str]:
        """
        Find pages containing ALL words (AND query).
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

    def find_with_ranking(self, query: List[str]) -> List[tuple]:
        pass