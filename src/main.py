"""
Command-Line Interface for the Quotes Search Engine

This module provides a CLI tool for building an inverted index from web-crawled
quotes data and performing search queries. It integrates the Crawler, Indexer,
and Search components into a user-friendly command-line application.
"""

import json
import os
from typing import Dict, List, Optional, Any

from crawler import Crawler
from indexer import Indexer
from search import Search

INDEX_FILE = "data/index.json"


# -------------------------
# BUILD COMMAND
# -------------------------
def build() -> None:
    """
    Execute the build command: crawl website and create inverted index.

    This function orchestrates the crawling of quotes.toscrape.com,
    builds an inverted index from the collected data, and saves it
    to a JSON file. It ensures the data directory exists.
    """
    print("\n[BUILD] Starting crawl and indexing...")

    crawler = Crawler()
    data = crawler.crawl()

    indexer = Indexer()
    index = indexer.build_index(data)

    # ensure data directory exists
    os.makedirs("data", exist_ok=True)

    indexer.save_index(INDEX_FILE)

    print("[BUILD] Completed successfully.\n")


# -------------------------
# LOAD COMMAND
# -------------------------
def load() -> Optional[Dict[str, Dict[str, Dict[str, Any]]]]:
    """
    Execute the load command: load inverted index from file.

    This function attempts to load the inverted index from the JSON file.
    If the file doesn't exist, it prints an error and returns None.

    Returns:
        Optional[Dict[str, Dict[str, Dict[str, Any]]]]: The loaded index,
            or None if the file doesn't exist.
    """
    if not os.path.exists(INDEX_FILE):
        print("[ERROR] No index file found. Run 'build' first.")
        return None

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    print("[LOAD] Index loaded successfully.\n")
    return index


# -------------------------
# PRINT COMMAND
# -------------------------
def print_word(search: Search, word: str) -> None:
    """
    Execute the print command: display index entry for a word.

    This function looks up a word in the index and prints its frequency
    and position data across all documents.

    Args:
        search (Search): The Search instance with the loaded index.
        word (str): The word to look up.
    """
    result = search.print_word(word)

    if not result:
        print(f"[INFO] Word '{word}' not found.\n")
        return

    print(f"\n[PRINT] Results for '{word}':")
    for url, stats in result.items():
        print(f"- {url}")
        print(f"  frequency: {stats['frequency']}")
        print(f"  positions: {stats['positions']}")
    print()


# -------------------------
# FIND COMMAND (Uses TF-IDF page ranking)
# -------------------------
def find_words(search: Search, words: List[str]) -> None:
    """
    Execute the find command: search for words with TF-IDF ranking.

    This function performs a ranked search for the given words and
    displays the results sorted by relevance score.

    Args:
        search (Search): The Search instance with the loaded index.
        words (List[str]): The list of words to search for.
    """
    results = search.find_with_ranking(words)

    if not results:
        print(f"[INFO] No results found for {words}\n")
        return

    print(f"\n[FIND] Pages containing {words} (ranked):")

    for url, score in results:
        print(f"- {url} (score={score:.2f})")

    print()


# -------------------------
# OPTIONAL: RANKED FIND
# -------------------------
def find_ranked(search: Search, words: List[str]) -> None:
    """
    Alternative find command with different output format.

    This function is similar to find_words but uses a different
    output format. It may be used for debugging or alternative
    display preferences.

    Args:
        search (Search): The Search instance with the loaded index.
        words (List[str]): The list of words to search for.
    """
    results = search.find_with_ranking(words)

    if not results:
        print(f"[INFO] No results found for {words}\n")
        return

    print(f"\n[FIND - RANKED] Pages containing {words}:")
    for url, score in results:
        print(f"- {url} (score={score})")
    print()


# -------------------------
# CLI LOOP
# -------------------------
def main() -> None:
    """
    Main CLI loop for the search engine tool.

    This function provides an interactive command-line interface
    that allows users to build/load the index and perform searches.
    Available commands: build, load, print <word>, find <words>, exit.
    """
    index: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None
    search: Optional[Search] = None

    print("========================================")
    print(" Simple Search Engine Tool ")
    print("========================================")
    print("Commands:")
    print("  build")
    print("  load")
    print("  print <word>")
    print("  find <word1> <word2> ...")
    print("  exit")
    print("========================================")

    while True:
        command = input("> ").strip()

        if command == "build":
            build()

        elif command == "load":
            index = load()
            if index is not None:
                search = Search(index)

        elif command.startswith("print "):
            if search is None:
                print("[ERROR] Load or build index first.\n")
                continue

            word = command.split(" ", 1)[1]
            print_word(search, word)

        elif command.startswith("find "):
            if search is None:
                print("[ERROR] Load or build index first.\n")
                continue

            words = command.split()[1:]
            find_words(search, words)

        elif command == "exit":
            print("Exiting...")
            break

        else:
            print("[ERROR] Unknown command.\n")


if __name__ == "__main__":
    main()