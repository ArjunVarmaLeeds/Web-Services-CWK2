
"""
Web Crawler Module for Quotes Scraper

This module provides a Crawler class that fetches web pages from quotes.toscrape.com,
extracts quotes and their authors, and handles pagination with politeness delays.
"""

import requests
from bs4 import BeautifulSoup as bs
import time
from typing import List, Dict, Optional, Any


class Crawler:
    """
    A web crawler for scraping quotes from quotes.toscrape.com.

    This class handles fetching pages, extracting quote data, and managing
    pagination while respecting website politeness policies through delays
    between requests.

    Attributes:
        base_url (str): The base URL of the website to crawl.
        visited_urls (set): Set of URLs that have already been visited.
        sleep_time (int): Number of seconds to wait between requests.
    """

    def __init__(self, base_url: str = "https://quotes.toscrape.com") -> None:
        """
        Initialize the Crawler with a base URL.

        Args:
            base_url (str): The base URL of the website to crawl.
                Defaults to "https://quotes.toscrape.com".
        """
        self.base_url = base_url
        self.visited_urls: set[str] = set()
        self.sleep_time = 3

    def fetch_page(self, url: str) -> Optional[bs]:
        """
        Fetch a web page and return a BeautifulSoup object.

        This method performs an HTTP GET request with a timeout and basic
        error handling. If the request fails, it prints an error message
        and returns None.

        Args:
            url (str): The URL of the page to fetch.

        Returns:
            Optional[bs]: A BeautifulSoup object if successful, None if failed.

        Raises:
            This method catches all RequestException and returns None.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return bs(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None

    def extract_quotes(self, soup: bs) -> List[Dict[str, str]]:
        """
        Extract all quotes and their authors from a BeautifulSoup object.

        This method parses the HTML to find quote text and author elements
        using CSS selectors, then pairs them together.

        Args:
            soup (bs): A BeautifulSoup object representing the page HTML.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each containing
                'text' and 'author' keys with their respective string values.
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

    def get_next_page(self, soup: bs) -> Optional[str]:
        """
        Extract the URL of the next page if it exists.

        This method looks for a "next" link in the pagination and constructs
        the full URL by appending the href to the base URL.

        Args:
            soup (bs): A BeautifulSoup object representing the page HTML.

        Returns:
            Optional[str]: The full URL of the next page, or None if no next page.
        """
        next_button = soup.select_one(".next a")
        if next_button:
            return self.base_url + next_button["href"]
        return None

    def crawl(self) -> List[Dict[str, Any]]:
        """
        Crawl all pages starting from page 1 and collect quote data.

        This method performs a breadth-first crawl of the website, extracting
        quotes from each page and following pagination links. It includes
        politeness delays between requests and avoids revisiting URLs.

        Returns:
            List[Dict[str, any]]: A list of dictionaries, each containing:
                - "url" (str): The URL of the page.
                - "quotes" (List[Dict[str, str]]): List of quotes from that page.
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
                print(f"[INFO] Sleeping for {self.sleep_time} seconds (politeness policy)...")
                time.sleep(self.sleep_time)

        print(f"[INFO] Crawling complete. Pages visited: {len(all_data)}")
        return all_data


if __name__ == "__main__":
    crawler = Crawler()
    data = crawler.crawl()

    # Simple debug print
    for page in data:
        print(f"\nURL: {page['url']}")
        for quote in page["quotes"]:
            print(f" - {quote}")