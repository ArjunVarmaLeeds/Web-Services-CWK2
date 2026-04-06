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
        for page in crawler_data:
            url = page["url"]

            for quote in page["quotes"]:
                self.add_document(url, quote["text"])

        return self.index
    
    def save_index(self, filename):
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