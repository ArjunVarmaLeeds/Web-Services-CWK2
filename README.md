# Search Engine Tool (COMP3011 Coursework 2)

## 📌 Project Overview and Purpose

This project implements a simple search engine tool for the website:
https://quotes.toscrape.com/

The system demonstrates core search engine concepts including: - Web
crawling - Inverted indexing - Query processing and retrieval

The tool crawls web pages, extracts textual data (quotes), builds an
inverted index storing word statistics (frequency and positions), and
allows users to search for words or phrases efficiently using the TF-IDF page ranking algorithm via a
command-line interface.

------------------------------------------------------------------------

## ⚙️ Installation / Setup Instructions

### 1. Clone the repository

``` bash
git clone https://github.com/ArjunVarmaLeeds/Web-Services-CWK2.git
cd Web-Services-CWK2
```

### 2. Install dependencies

``` bash
pip install -r requirements.txt
```

Or manually:

``` bash
pip install requests beautifulsoup4 pytest
```

### 3. Project Structure

    src/
      main.py
      crawler.py
      indexer.py
      search.py

    tests/
      test_crawler.py
      test_indexer.py
      test_search.py

    data/

------------------------------------------------------------------------

## 🚀 Usage Instructions

Run the program from the project root:

```bash
python src/main.py
```

---

## 💻 Command Examples

Below are examples demonstrating all four required commands.

---

### 🔨 1. Build Index

Crawls the website and builds the inverted index.

```bash
> build
```

**Example Output:**

```
[BUILD] Starting crawl and indexing...
[INFO] Crawling: https://quotes.toscrape.com/page/1/
[INFO] Crawling complete. Pages visited: 10
============================================================
Saving index to file
============================================================
✓ Index saved to data/index.json
[BUILD] Completed successfully.
```

---

### 📂 2. Load Index

Loads a previously saved index from disk.

```bash
> load
```

**Example Output:**

```
[LOAD] Index loaded successfully.
```

---

### 🔍 3. Print Word

Displays index details for a specific word.

```bash
> print life
```

**Example Output:**

```
[PRINT] Results for 'life':
- https://quotes.toscrape.com/page/1/
  frequency: 2
  positions: [3, 10]
- https://quotes.toscrape.com/page/2/
  frequency: 1
  positions: [5]
```

---

### 🔎 4. Find Words

Searches for pages containing ALL query terms, uses TF-IDF ranking.

```bash
> find good friends
```

**Example Output:**

```
[FIND] Pages containing ['good', 'friends']:
- https://quotes.toscrape.com/page/1/
```

---

### ⚠️ Edge Case Example

```bash
> find unknownword
```

**Output:**

```
[INFO] No results found for ['unknownword']
```

---

## 🧪 Testing Instructions

Run all tests using:

``` bash
pytest
```

### What is tested:

-   Crawler (HTML parsing, pagination, error handling)
-   Indexer (tokenization, indexing logic, file saving)
-   Search (query processing, retrieval, ranking)

Tests use: - Mocking (for network calls) - Saved HTML files (realistic
parsing) - Edge case validation

------------------------------------------------------------------------

## 📦 Dependencies

-   requests → HTTP requests
-   beautifulsoup4 → HTML parsing
-   pytest → testing framework
-   re (built-in) → tokenization

Install all dependencies with:

``` bash
pip install requests beautifulsoup4 pytest
```

------------------------------------------------------------------------

## 🧠 Key Features

-   Inverted index with frequency and positional data
-   Case-insensitive search
-   Regex-based tokenization (handles punctuation correctly)
-   Multi-word AND queries
-   Optional ranking (term frequency based)

------------------------------------------------------------------------

## 📌 Notes

-   The crawler respects a politeness delay between requests
-   The index is stored as a JSON file in the `data/` directory
-   Ensure internet connection is available when running `build`

------------------------------------------------------------------------

## 🎯 Summary

This project demonstrates a simplified but realistic search engine
pipeline: Crawling → Indexing → Searching

It highlights core concepts used in real-world search systems such as
Google, including efficient retrieval using inverted indices.
