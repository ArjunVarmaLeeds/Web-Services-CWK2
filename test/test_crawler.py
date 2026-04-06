import pytest
from unittest.mock import patch, Mock
from requests import RequestException
import os
from bs4 import BeautifulSoup as bs
from src.crawler import Crawler


# -------------------------
# Helper: load saved HTML
# -------------------------
def load_html(filename: str) -> str:
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "data", filename)

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------
# Test fetch_page (success)
# -------------------------
@patch("src.crawler.requests.get")
def test_fetch_page_success(mock_get):
    html = load_html("page1.html")

    mock_response = Mock()
    mock_response.text = html
    mock_response.raise_for_status = Mock()

    mock_get.return_value = mock_response

    crawler = Crawler()
    soup = crawler.fetch_page("http://fake-url")

    assert soup is not None
    assert isinstance(soup, bs)

# -------------------------
# Test fetch_page (failure)
# -------------------------
@patch("src.crawler.requests.get")
def test_fetch_page_failure(mock_get):
    mock_get.side_effect = RequestException("Network error")

    crawler = Crawler()
    soup = crawler.fetch_page("http://fake-url")

    assert soup is None

# -------------------------
# Test extract_quotes
# -------------------------
def test_extract_quotes():
    crawler = Crawler()

    html = load_html("page1.html")
    soup = bs(html, "html.parser")

    quotes = crawler.extract_quotes(soup)

    assert len(quotes) > 0
    assert "text" in quotes[0]
    assert "author" in quotes[0]

    # Optional stronger check
    assert isinstance(quotes[0]["text"], str)
    assert isinstance(quotes[0]["author"], str)

# -------------------------
# Test get_next_page (exists)
# -------------------------
def test_get_next_page_exists():
    crawler = Crawler()

    html = load_html("page1.html")  # should contain next link
    soup = bs(html, "html.parser")

    next_url = crawler.get_next_page(soup)

    assert next_url is not None
    assert next_url.endswith("/page/2/")

# -------------------------
# Test get_next_page (none)
# -------------------------
def test_get_next_page_none():
    crawler = Crawler()

    html = load_html("page2.html")  # last page
    soup = bs(html, "html.parser")

    next_url = crawler.get_next_page(soup)

    assert next_url is None

# -------------------------
# Test crawl (integration)
# -------------------------
@patch("src.crawler.time.sleep", return_value=None)  # remove delay
@patch("src.crawler.Crawler.fetch_page")
def test_crawl(mock_fetch, mock_sleep):
    html1 = load_html("page1.html")
    html2 = load_html("page2.html")

    soup1 = bs(html1, "html.parser")
    soup2 = bs(html2, "html.parser")

    # simulate 2 pages
    mock_fetch.side_effect = [soup1, soup2]

    crawler = Crawler()
    data = crawler.crawl()

    assert len(data) == 2

    # structure checks
    assert "url" in data[0]
    assert "quotes" in data[0]

    # content checks
    assert isinstance(data[0]["quotes"], list)
    assert len(data[0]["quotes"]) > 0

    assert "text" in data[0]["quotes"][0]
    assert "author" in data[0]["quotes"][0]

def test_extract_quotes_empty_html():
    crawler = Crawler()
    soup = bs("<html></html>", "html.parser")

    quotes = crawler.extract_quotes(soup)

    assert quotes == []

def test_get_next_page_invalid_structure():
    crawler = Crawler()
    soup = bs("<html></html>", "html.parser")

    assert crawler.get_next_page(soup) is None

@patch("src.crawler.requests.get")
def test_fetch_called_with_correct_url(mock_get):
    from unittest.mock import Mock
    mock_response = Mock()
    mock_response.text = "<html><body>Test</body></html>"
    mock_get.return_value = mock_response
    
    crawler = Crawler()
    crawler.fetch_page("http://test.com")

    mock_get.assert_called_once_with("http://test.com", timeout=10)