import json
import os

from crawler import Crawler
from indexer import Indexer
from search import Search

INDEX_FILE = "data/index.json"

# -------------------------
# BUILD COMMAND
# -------------------------
def build():
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
def load():
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
def print_word(search: Search, word: str):
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
def find_words(search: Search, words):
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
def find_ranked(search: Search, words):
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
def main():
    index = None
    search = None

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