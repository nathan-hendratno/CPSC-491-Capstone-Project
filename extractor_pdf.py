"""
Usage:
    python extractor_pdf.py [PDF_PATH]

Example:
    python extractor_pdf.py tests/pdfs/t0_vr_health_games.pdf
"""

import json
import sys
import fitz

DEFAULT_PDF_PATH = "tests/pdfs/t0_vr_health_games.pdf"

def extract_title(doc):
    return doc.metadata.get("title", "(no title found)")

def extract_author(doc):
    return doc.metadata.get("author", "(no author found)").strip()

def extract_publication_date(doc):
    raw = doc.metadata.get("creationDate", "")
    if not raw:
        return "(no publication date found)"

    if raw.startswith("D:"):
        date = raw[2:10]  # grab just YYYYMMDD
        return f"{date[:4]}-{date[4:6]}-{date[6:8]}"

    return raw

def extract_links(doc):
    seen = set()
    links = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        for link in page.get_links():
            uri = link.get("uri")
            if uri and uri not in seen:
                seen.add(uri)
                links.append(uri)
    return links

def extract_text(doc):
    extracted_text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        extracted_text += page.get_text()
    cleaned = " ".join(extracted_text.split())
    return cleaned

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