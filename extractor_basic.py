# ── extractor_basic.py ────────────────────────────────────────
"""
extractor_basic.py - Basic article data extractor for Credible Sorcerer.

Fetches a web page and extracts the title, links, and visible text
using requests + BeautifulSoup.

Usage:
    python extractor_basic.py [URL]

Note: 
    Only tested on Wikipedia & BBC articles so far.
"""
# ─────────────────────────────────────────────────────────────

import json
import sys
import requests
from bs4 import BeautifulSoup


# ── Configuration ───────────────────────────────────────────────
# Default URL used when no argument is provided.
DEFAULT_URL = "https://en.wikipedia.org/wiki/Web_scraping"
# ────────────────────────────────────────────────────────────────


def fetch_html(url):
    """Download the page HTML. Returns the text content or None on failure."""
    try:
        headers = {"User-Agent": "CredibleSorcerer/1.0 (student project)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # raises an error for 4xx/5xx status codes
        return response.text
    except requests.RequestException as err:
        print(f"Error fetching URL: {err}")
        return None


def extract_title(soup):
    """Return the text inside the <title> tag, or a fallback message."""
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        return title_tag.string.strip()
    return "(no title found)"

def extract_author(soup):
    """Return the author of the article if available."""
    author_meta = soup.find("meta", attrs={"name": "author"})
    if author_meta and author_meta.get("content"):
        return author_meta["content"].strip()
    return "(no author found)"

def extract_links(soup):
    """Return a list of all href values from <a> tags."""
    links = []
    for tag in soup.find_all("a", href=True):
        if tag["href"].startswith("http"):
            links.append(tag["href"])
    return links


def extract_visible_text(soup):
    """Return the visible text from the article body with extra whitespace collapsed."""
    # Try to find the main content area. Falls back to the full page if none found.
    body = (
        soup.find("article")
        or soup.find("div", id="mw-content-text")  # Wikipedia-specific
        or soup.find("div", {"role": "main"})
        or soup
    )

    # Remove script and style elements so their contents don't leak into the text.
    for hidden in body(["script", "style"]):
        hidden.decompose()

    raw_text = body.get_text(separator=" ")

    # Collapse runs of whitespace into single spaces and strip leading/trailing.
    cleaned = " ".join(raw_text.split())
    return cleaned


def scrape_article(url):
    """Main function: fetch, parse, and return extracted data as a dict."""
    html = fetch_html(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, "html.parser")

    data = {
        "url": url,
        "title": extract_title(soup),
        "author": extract_author(soup),
        "links": [],
        "link_count": 0,
        "visible_text_preview": "",
        "visible_text_length": 0,
    }

    links = extract_links(soup)
    data["links"] = links
    data["link_count"] = len(links)

    text = extract_visible_text(soup)
    # Store only the first 4000 characters as a preview to keep output readable.
    data["visible_text_preview"] = text[:4000]
    data["visible_text_length"] = len(text)
    
    return data


# ── Run ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    result = scrape_article(url)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Scraping failed. Check the URL and your network connection.")

# ───────────────────────────────────────────────────────────────




# ── TODO's ─────────────────────────────────────────────────────────

# TODO: Extract author and publication date if available
#       Look for common meta tags like name = "author" and HTML structures

# TODO: Add Visible Text Preview (Article Text Data) to Dict
#       Return the full Article Text in Dict if needed for testing 
#       Clean Up Visible Text Extraction

# TODO: Add Links to Dict for Article Data
#       Count Links and Add Link Count to Dict

# TODO: Handle different site structures
#       Not every site uses <article> or has the same layout
#       Use library to auto detect article body if possible

# TODO: Turn file into module with functions for reuse
#       Refactor code into functions that can be imported and reused

# TODO: Output into JSON format
#       Format the final output as JSON for easy consumption
# ───────────────────────────────────────────────────────────────