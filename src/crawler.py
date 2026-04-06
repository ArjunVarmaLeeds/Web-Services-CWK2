
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
        """
        Get next page URL if exists.
        """
        next_button = soup.select_one(".next a")
        if next_button:
            return self.base_url + next_button["href"]
        return None

    def crawl(self) -> List[Dict]:
        """
        Crawl all pages and return collected data.
        Each entry contains:
        {
            "url": page_url,
            "quotes": [list of quotes]
        }
        """
        url = f"{self.base_url}/page/1/"
        all_data = []

        while url:
            if url in self.visited_urls:
                break

            print(f"[INFO] Crawling: {url}")
            soup = self.fetch_page(url)

            if soup is None:
                break

            # Extract quotes
            quotes = self.extract_quotes(soup)

            all_data.append({
                "url": url,
                "quotes": quotes
            })

            self.visited_urls.add(url)

            # Find next page
            url = self.get_next_page(soup)

            # Politeness delay (MANDATORY for coursework)
            if url:
                print("[INFO] Sleeping for 6 seconds (politeness policy)...")
                time.sleep(6)

        print(f"[INFO] Crawling complete. Pages visited: {len(all_data)}")
        return all_data

