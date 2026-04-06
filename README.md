# 🚀 **Search Engine Tool (COMP3011 Coursework 2)**

## 📌 Overview

This project implements a **mini search engine pipeline** over the website:
👉 [https://quotes.toscrape.com/](https://quotes.toscrape.com/)

It demonstrates core information retrieval concepts including:

* Web crawling
* Inverted indexing
* Query processing
* Relevance ranking (TF-IDF)

The system crawls web pages, extracts textual data (quotes), builds an efficient **inverted index**, and supports fast keyword-based search via a command-line interface.

---

## 🧠 Key Features

* 🔍 **Inverted Index** with frequency and positional data
* ⚡ **Efficient Lookup** using hash-based structures (Python dictionaries)
* 🔎 **Multi-word AND Queries**
* 📊 **TF-IDF Ranking** for improved search relevance
* 🧹 **Regex-based Tokenization** (handles punctuation correctly)
* 🧪 **Comprehensive Test Suite** with mocking and real HTML parsing
* 💾 Persistent storage using JSON

---

## 🏗️ Architecture Overview

The system follows a **modular pipeline design**:

```text
           +-------------+
           |  Crawler    |
           +-------------+
                  |
                  v
           +-------------+
           |  Indexer    |
           +-------------+
                  |
                  v
           +-------------+
           |   Search    |
           +-------------+
                  |
                  v
           +-------------+
           |     CLI     |
           +-------------+
```

### Components

#### 1. Crawler (`crawler.py`)

* Traverses all pages using pagination
* Extracts quotes and authors
* Implements politeness delay between requests
* Handles network errors gracefully

#### 2. Indexer (`indexer.py`)

* Builds an **inverted index**:

  ```
  word → {document → {frequency, positions}}
  ```
* Uses regex tokenization for normalization
* Stores positional data for extensibility (e.g., phrase search)

#### 3. Search (`search.py`)

* Supports:

  * Word lookup (`print`)
  * Multi-word AND queries (`find`)
* Implements **TF-IDF ranking**:

  * Rewards rare, informative terms
  * Improves relevance over simple frequency scoring

#### 4. CLI Interface (`main.py`)

* Provides user interaction
* Implements required commands:

  * `build`, `load`, `print`, `find`

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/ArjunVarmaLeeds/Web-Services-CWK2.git
cd Web-Services-CWK2
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests beautifulsoup4 pytest
```

---

## 🚀 Usage

Run the application:

```bash
python src/main.py
```

---

## 💻 Command Examples

### 🔨 Build Index

```bash
> build
```

Crawls all pages and builds the inverted index.

---

### 📂 Load Index

```bash
> load
```

Loads previously saved index from `data/index.json`.

---

### 🔍 Print Word

```bash
> print life
```

**Example Output:**

```
[PRINT] Results for 'life':
- https://quotes.toscrape.com/page/1/
  frequency: 2
  positions: [3, 10]
```

---

### 🔎 Find (Ranked Search)

```bash
> find good friends
```

**Example Output:**

```
[FIND] Pages containing ['good', 'friends']:
- https://quotes.toscrape.com/page/1/ (score=3.42)
- https://quotes.toscrape.com/page/2/ (score=1.87)
```

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

### Test Coverage Includes:

* Crawler:

  * HTML parsing
  * Pagination handling
  * Error handling (mocked requests)

* Indexer:

  * Tokenization
  * Index structure correctness
  * Frequency and positional tracking

* Search:

  * Query processing
  * Multi-word intersection logic
  * TF-IDF ranking

**Current test coverage:**
```
================================================== tests coverage ===================================================
_________________________________ coverage: platform darwin, python 3.12.10-final-0 _________________________________

Name             Stmts   Miss  Cover
------------------------------------
src/crawler.py      57      8    86%
src/indexer.py      30      0   100%
src/main.py         91     91     0%
src/search.py       43      2    95%
------------------------------------
TOTAL              221    101    54%
================================================ 32 passed in 1.10s =================================================

```

### Testing Strategy

* ✅ Unit tests for each module
* ✅ Mocking external dependencies (network calls)
* ✅ Real HTML files for realistic parsing
* ✅ Edge case handling

---

## 📦 Dependencies

| Library          | Purpose           |
| ---------------- | ----------------- |
| `requests`       | HTTP requests     |
| `beautifulsoup4` | HTML parsing      |
| `pytest`         | Testing framework |
| `re` (built-in)  | Tokenization      |

---

## 🧠 Design Rationale

### Why Inverted Index?

* Enables **O(1) average lookup** per word
* Avoids scanning documents at query time
* Scales efficiently for large datasets

---

### Why TF-IDF Ranking?

* Simple frequency-based ranking treats all words equally
* TF-IDF improves relevance by:

  * Boosting rare terms (high IDF)
  * Penalising common terms

This aligns with real-world search engine behaviour.

---

### Why Regex Tokenization?

* Handles punctuation consistently
* Ensures:

  ```
  "life." == "life"
  ```
* Prevents mismatches between indexing and querying

---

### Why Modular Design?

* Separation of concerns:

  * Crawling
  * Indexing
  * Searching
* Improves:

  * Maintainability
  * Testability
  * Extensibility

---

## 📈 Complexity Overview

| Operation          | Complexity     |
| ------------------ | -------------- |
| Crawling           | O(n) pages     |
| Indexing           | O(total words) |
| Search (AND query) | O(k × d)       |
| Ranking (TF-IDF)   | O(results)     |

Where:

* `k` = number of query terms
* `d` = documents per term

---

## 📌 Limitations & Future Work

* No phrase search (can be added using positions)
* No stemming or lemmatization
* Ranking can be improved using:

  * TF-IDF normalization
  * cosine similarity

---

## 🎯 Summary

This project implements a **complete search engine pipeline**:

> Crawling → Indexing → Retrieval → Ranking

It demonstrates key principles used in real-world systems such as:

* inverted indexing
* query processing
* relevance ranking

---

## 👤 Author

Arjun Varma
University of Leeds – Computer Science

---
