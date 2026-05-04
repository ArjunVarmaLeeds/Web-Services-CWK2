import json
import time
from src.search import Search


def load_index():
    with open("data/index.json", "r") as f:
        return json.load(f)


def benchmark_queries(search):
    queries = [
        ["life"],
        ["good", "friends"],
        ["life", "love", "truth"],
        ["if", "you", "understand"]
    ]

    print("\n--- Query Benchmark ---\n")

    for q in queries:
        # basic find
        start = time.time()
        search.find(q)
        basic_time = time.time() - start

        # tf-idf find
        start = time.time()
        search.find_with_ranking(q)
        tfidf_time = time.time() - start

        print(f"Query: {q}")
        print(f"  Basic find: {basic_time:.6f}s")
        print(f"  TF-IDF find: {tfidf_time:.6f}s")
        print()


if __name__ == "__main__":
    index = load_index()
    search = Search(index)

    benchmark_queries(search)