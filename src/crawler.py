
import requests
from bs4 import BeautifulSoup as bs
import time
from typing import List, Dict

class Crawler:
    def __init__(self, base_url: str = "https://quotes.toscrape.com"):
        pass

    def fetch_page(self, url: str) -> bs:
        pass

    def extract_quotes(self, soup: bs) -> List[Dict]:
        pass

    def get_next_page(self, soup: bs) -> str:
        pass

    def crawl(self) -> List[Dict]:
        pass

