
import requests
from bs4 import BeautifulSoup as bs
import time
from typing import List, Dict

class Crawler:
    def __init__(self, base_url: str = "https://quotes.toscrape.com"):
        self.base_url = base_url
        self.visited_urls = set()

    def fetch_page(self, url: str) -> bs:
        """
        Fetch a page and return bs object.
        Includes basic error handling.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return bs(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None

    def extract_quotes(self, soup: bs) -> List[Dict]:
        """
        Extract all quotes from a page.
        """
        quotes = []
        quote_elements = soup.select(".quote .text")
        author_elements = soup.select(".quote .author")

        for q, a in zip(quote_elements, author_elements):
            text = q.get_text(strip=True)
            author = a.get_text(strip=True)

            quotes.append({
                "text": text,
                "author": author
            })

        return quotes

    def get_next_page(self, soup: bs) -> str:
        pass

    def crawl(self) -> List[Dict]:
        pass

