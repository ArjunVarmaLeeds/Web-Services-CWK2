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
        pass

    def find_with_ranking(self, query: List[str]) -> List[tuple]:
        pass