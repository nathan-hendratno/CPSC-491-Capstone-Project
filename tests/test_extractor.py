"""
Run extractor_basic.py against a set of test URLs.

Usage:
    python tests/test_extractor.py
"""

import json
import sys
import os

TESTS_DIR = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(TESTS_DIR, ".."))
from extractor_basic import scrape_article

TEST_URLS = [
    # Major News
    ("Fortune", "https://fortune.com/2026/02/09/nancy-guthries-family-faces-6-million-bitcoin-ransom-demand/"),
    ("Reuters (blocked)", "https://www.reuters.com/world/china/china-set-widen-footprint-bangladesh-indias-ties-decline-2026-02-10/"),
    ("NYT (blocked)", "https://www.nytimes.com/2026/02/09/us/politics/trump-nuclear-arms-underground-tests.html"),

    # International News
    ("Al Jazeera", "https://www.aljazeera.com/news/liveblog/2026/2/10/live-israeli-attack-on-gaza-building-kills-four-palestinians"),
    ("The Guardian", "https://www.theguardian.com/us-news/2026/feb/09/judge-california-ice-masks"),

    # Tech / Blog
    ("TechCrunch", "https://techcrunch.com/2026/02/09/mrbeasts-company-buys-gen-z-focused-fintech-app-step/"),
    ("Ars Technica", "https://arstechnica.com/gaming/2026/02/just-look-at-ayaneos-absolute-unit-of-a-windows-gaming-handheld/"),

    # Academic / Reference
    ("Wikipedia", "https://en.wikipedia.org/wiki/Web_scraping"),
    ("Google Scholar (not an article)", "https://scholar.google.com/"),

    # Smaller / Independent
    ("ProPublica", "https://www.propublica.org/article/life-inside-ice-dilley-children"),
    ("Medium (blocked)", "https://medium.com/code-like-a-girl/why-reading-more-books-wasnt-making-me-smarter-5fad5a2cad03"),

    # .edu Sites
    # University news pages
    ("MIT News", "https://news.mit.edu/2026/designing-more-resilient-future-plants-foray-0227"),
    ("Stanford News (blocked)", "https://news.stanford.edu/stories/2026/02/ukrainian-reform-initiatives-fellowship-program"),

    # Research / Academic articles
    ("ACS (blocked)", "https://pubs.acs.org/doi/full/10.1021/acsaenm.6c00121"),
    ("PubMed", "https://pubmed.ncbi.nlm.nih.gov/38421179/"),
    ("arXiv", "https://arxiv.org/abs/2603.01202"),

    # Library / Reference
    ("University of Washington Libraries", "https://guides.lib.uw.edu")
]

OUTPUT_FILE = os.path.join(TESTS_DIR, "test_outputs.json")


if __name__ == "__main__":
    results = []
    for name, url in TEST_URLS:
        result = scrape_article(url)
        results.append({
            "site": name,
            "data": result,
        })
        print(f"Done: {name}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nAll results written to {OUTPUT_FILE}")
