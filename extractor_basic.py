"""
extractor_basic.py - Basic article data extractor for Credible Sorcerer.

Fetches a web page and extracts the title, links, and visible text
using requests + BeautifulSoup.

Usage:
    python extractor_basic.py [URL]

Note: 
    Only tested on Wikipedia & BBC articles so far.
"""


import json
import sys
import requests
from bs4 import BeautifulSoup


# Default URL used when no argument is provided.
DEFAULT_URL = "https://en.wikipedia.org/wiki/Web_scraping"


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


def extract_json_ld(soup):
    """Extract JSON-LD structured data from the page if available."""
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string)
            # Some sites wrap it in a list.
            if isinstance(data, list):
                data = data[0]
            # Look for an article type.
            if data.get("@type") in ("NewsArticle", "Article", "BlogPosting", "ReportageNewsArticle"):
                return data
        except (json.JSONDecodeError, TypeError):
            continue
    return None


def extract_title(soup):
    """Return the text inside the <title> tag, or a fallback message."""
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        return title_tag.string.strip()
    return "(no title found)"


def extract_publication_date(soup):
    """Return the publication date of the article if available."""
    # Try JSON-LD structured data first (cleanest source).
    ld = extract_json_ld(soup)
    if ld and ld.get("datePublished"):
        return ld["datePublished"].strip()

    # Try common meta tag patterns.
    candidates = [
        {"property": "article:published_time"},  
        {"name": "publication_date"},
        {"name": "date"},
        {"name": "pubdate"},
        {"name": "DC.date.issued"},
    ]
    for attrs in candidates:
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return tag["content"].strip()

    # Fall back to <time> elements with a datetime attribute.
    time_tag = soup.find("time", attrs={"datetime": True})
    if time_tag:
        return time_tag["datetime"].strip()

    return "(no publication date found)"


def extract_author(soup):
    """Return the author of the article if available."""
    # Try JSON-LD structured data first (cleanest source).
    ld = extract_json_ld(soup)
    if ld and ld.get("author"):
        author = ld["author"]
        # Author can be a dict, a list of dicts, or a string.
        if isinstance(author, list):
            names = []
            for a in author:
                if isinstance(a, dict):
                    names.append(a.get("name", ""))
                else:
                    names.append(a)
            # Filter out empty names and join with commas.
            filtered = []
            for n in names:
                if n:
                    filtered.append(n)
            return ", ".join(filtered)
        if isinstance(author, dict):
            return author.get("name", "(no author found)")
        return str(author)

    # Try common meta tag conventions in order of prevalence.
    candidates = [
        {"property": "article:author"},  # Open Graph
        {"name": "author"},
        {"name": "byl"},
        {"name": "DC.creator"},
    ]
    for attrs in candidates:
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return tag["content"].strip()

    # Fall back to elements with common author/byline class names.
    for class_name in ["author", "byline"]:
        author_el = soup.find(attrs={"class": lambda c: c and class_name in c.lower()})
        if author_el and author_el.get_text(strip=True):
            return author_el.get_text(strip=True)

    return "(no author found)"


def extract_links(soup):
    """Return a list of all href values from <a> tags."""
    links = []
    for tag in soup.find_all("a", href=True):
        if tag["href"].startswith("http"):
            links.append(tag["href"])
    return links


def extract_text(soup):
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
        "publication_date": extract_publication_date(soup),
        "link_count": len(extract_links(soup)),
        "text_length": len(extract_text(soup)),
        "links": [],
        "text_preview": "",
    }

    links = extract_links(soup)
    # Uncomment to show all links
    # data["links"] = links

    text = extract_text(soup)
    # Store only the first 4000 characters as a preview to keep output readable.
    # Uncomment to show preview text
    # data["text_preview"] = text[:4000]
    
    return data


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    result = scrape_article(url)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Scraping failed. Check the URL and your network connection.")



# TODO: Handle different site structures
#       Not every site uses <article> or has the same layout
#       Use library to auto detect article body if possible
