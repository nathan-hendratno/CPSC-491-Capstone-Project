"""
Run extractor_pdf.py against a set of test PDFs.

Usage:
    python tests/test_extractor_pdf.py

Note:
    Add any test PDFs to the tests/ folder and reference them in TEST_PDFS.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from extractor_pdf import scrape_article

TESTS_DIR = os.path.dirname(__file__)

TEST_PDFS = [
    ("VR Health Games Review", os.path.join(TESTS_DIR, "test.pdf")),
]

OUTPUT_FILE = os.path.join(TESTS_DIR, "test_outputs_pdf.json")


if __name__ == "__main__":
    results = []
    for name, path in TEST_PDFS:
        result = scrape_article(path)
        results.append({
            "name": name,
            "data": result,
        })
        print(f"Done: {name}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nAll results written to {OUTPUT_FILE}")
