"""
Run extractor_pdf.py against a set of test PDFs.

Usage:
    python tests/test_extractor_pdf.py

Note:
    Add any test PDFs to the tests/pdfs/ folder and reference them in TEST_PDFS.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from extractor_pdf import scrape_article

TESTS_DIR = os.path.dirname(__file__)
PDFS_DIR = os.path.join(TESTS_DIR, "pdfs")

TEST_PDFS = [
    ("VR Health Games",          os.path.join(PDFS_DIR, "t0_vr_health_games.pdf")),
    ("ACS NMR Spectroscopy",     os.path.join(PDFS_DIR, "t1_acs_nmr_spectroscopy.pdf")),
    ("CDC Health Report",        os.path.join(PDFS_DIR, "t2_cdc_health_report.pdf")),
    ("ProPublica White Paper",   os.path.join(PDFS_DIR, "t3_propublica_white_paper.pdf")),
    ("News Article (OCR)",       os.path.join(PDFS_DIR, "t4_news_article_ocr.pdf")),
    ("China Reconstructs (OCR)", os.path.join(PDFS_DIR, "t5_china_reconstructs_ocr.pdf")),
    ("Govt Report (OCR)",        os.path.join(PDFS_DIR, "t6_govt_report_ocr.pdf")),
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
