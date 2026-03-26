"""
Usage:
    python extractor_pdf.py [PDF_PATH]
"""

import json
import sys
import fitz

DEFAULT_PDF_PATH = "tests/test.pdf"

def extract_title(doc):
    return doc.metadata.get("title", "Unknown Title")

def extract_author(doc):
    return doc.metadata.get("author", "Unknown Author")

def extract_publication_date(doc):
    return doc.metadata.get("creationDate", "Unknown Date")

def extract_links(doc):
    links = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        for link in page.get_links():
            if link.get("uri"):
                links.append(link.get("uri", "No URI"))
    return links

def extract_text(doc):
    extracted_text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        extracted_text += page.get_text()
    return extracted_text

def scrape_article(pdf):
    doc = fitz.open(pdf)

    links = extract_links(doc)
    text = extract_text(doc)

    data = {
        "pdf": pdf,
        "title": extract_title(doc),
        "author": extract_author(doc),
        "publication_date": extract_publication_date(doc),
        "link_count": len(links),
        "text_length": len(text),
        "links": links,
        "text": text,
    }
    
    doc.close()    
    return data


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF_PATH
    result = scrape_article(pdf)
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Scraping failed. Check the URL and your network connection.")