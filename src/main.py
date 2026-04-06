from crawler import Crawler
from indexer import Indexer
import json


def run_build():
    """
    Runs crawler + indexer and saves index to file.
    """
    print("[INFO] Starting crawl...")

    crawler = Crawler()
    crawler_data = crawler.crawl()

    print("[INFO] Building index...")

    indexer = Indexer()
    index = indexer.build_index(crawler_data)

    # Save index
    with open("data/index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print("[INFO] Index saved to data/index.json")

    return index


def run_load():
    """
    Loads index from file.
    """
    try:
        with open("data/index.json", "r", encoding="utf-8") as f:
            index = json.load(f)

        print("[INFO] Index loaded successfully")
        return index

    except FileNotFoundError:
        print("[ERROR] No index file found. Run 'build' first.")
        return None


def print_word(index, word):
    """
    Print index entry for a word.
    """
    word = word.lower()

    if word not in index:
        print(f"[INFO] Word '{word}' not found in index")
        return

    print(f"\n[INFO] Results for '{word}':")

    for url, stats in index[word].items():
        print(f"- {url}")
        print(f"  frequency: {stats['frequency']}")
        print(f"  positions: {stats['positions']}")


def find_words(index, words):
    """
    Find pages containing ALL words.
    """
    words = [w.lower() for w in words]

    result_sets = []

    for word in words:
        if word not in index:
            print(f"[INFO] Word '{word}' not found")
            return []

        result_sets.append(set(index[word].keys()))

    # intersection of all sets
    results = set.intersection(*result_sets)

    print(f"\n[INFO] Pages containing {words}:")

    for r in results:
        print(f"- {r}")

    return list(results)


def main():
    index = None

    print("Simple Search Engine CLI")
    print("Commands: build | load | print <word> | find <words> | exit")

    while True:
        command = input("> ").strip()

        if command == "build":
            index = run_build()

        elif command == "load":
            index = run_load()

        elif command.startswith("print "):
            if index is None:
                print("[ERROR] Load or build index first")
                continue

            word = command.split(" ", 1)[1]
            print_word(index, word)

        elif command.startswith("find "):
            if index is None:
                print("[ERROR] Load or build index first")
                continue

            words = command.split()[1:]
            find_words(index, words)

        elif command == "exit":
            print("Exiting...")
            break

        else:
            print("[ERROR] Unknown command")


if __name__ == "__main__":
    main()