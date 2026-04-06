import json
import re

class Indexer:
    def __init__(self):
        self.index = {}

    def tokenize(self, text: str):
        return re.findall(r"\b\w+\b", text.lower())    
    
    def add_document(self, url: str, text: str):
        """
        Indexing format
        {
        "word": {
                "page_url": {
                    "frequency": int,
                    "positions": [int, int]
                }
            }
        }
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

    def build_index(self, crawler_data):
        pass
    
    def save_index(self, filename):
        pass