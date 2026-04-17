import os
import json
import tempfile
import requests

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from extractor_basic import scrape_article
from extractor_pdf import scrape_article as scrape_pdf
from openai import OpenAI
from score_sorcery import Credibility

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class URLRequest(BaseModel):
    url: str


def search_related_articles(query):
    url = "https://api.crossref.org/v1/works"
    params = {
        "query": query,
        "rows": 5,
        "select": "title,URL,author,published-print,published-online"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    items = response.json()["message"]["items"]

    results = []
    for item in items:
        title_list = item.get("title", [])
        title = title_list[0] if title_list else "No title"

        results.append({
            "title": title,
            "url": item.get("URL", "#")
        })

    return results


@app.get("/")
async def root():
    return {"message": "Credible Sorcerer backend is running"}


# NEW: shared processing function for BOTH web URLs and PDFs
def analyze_extracted_data(data):
    if not data or not data.get("text"):
        raise HTTPException(status_code=400, detail="Failed to extract article content")

    article_text = data["text"][:12000]

    # Build article payload for scoring system
    article_for_score = {
        "title": data.get("title"),
        "author": data.get("author"),
        "publish_date": data.get("publication_date"),
        "link_count": data.get("link_count", 0),
        "article_text": data.get("text", "")
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful writing assistant that analyzes research articles. Always respond with valid JSON only, no markdown or extra text."
            },
            {
                "role": "user",
                "content": f"""Analyze the following article and return a JSON object with exactly these fields:
{{
  "summary": "A concise 2-3 sentence summary of the article",
  "key_points": ["point 1", "point 2", "point 3"],
  "tone": "one of: informational, opinion, investigative, promotional, satirical, emotional",
  "bias": "one of: neutral, slight left, slight right, strong left, strong right, unclear",
  "topics": ["topic1", "topic2", "topic3"],
  "search_queries": ["query 1", "query 2"]
}}

Rules:
- key_points must have 3 to 5 items
- topics must have 2 to 5 items
- search_queries must have 1 to 2 items
- Each search query should be short and scholarly, suitable for finding related academic or research articles
- Do not include quotation marks inside the query text unless necessary
- Return only the JSON object, no explanation

Article:
{article_text}"""
            }
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    analysis = json.loads(raw)

    # Run scoring system
    cred = Credibility(article=article_for_score)
    score = cred.calculate_score()
    explanation = cred.get_explanation()
    score_breakdown = cred.get_score_breakdown()

    related_articles = []

    queries = analysis.get("search_queries", [])
    if queries:
        try:
            related_articles = search_related_articles(queries[0])
        except Exception:
            related_articles = []

    return {
        "title": data.get("title"),
        "author": data.get("author"),
        "publication_date": data.get("publication_date"),
        "summary": analysis.get("summary"),
        "key_points": analysis.get("key_points", []),
        "tone": analysis.get("tone"),
        "bias": analysis.get("bias"),
        "topics": analysis.get("topics", []),
        "links": data.get("links", []),
        "text_preview": data.get("text", "")[:2500],
        "search_queries": analysis.get("search_queries", []),
        "related_articles": related_articles,
        "score": score,
        "explanation": explanation,
        "score_breakdown": score_breakdown
    }


@app.post("/summarize")
async def summarize_article(request: URLRequest):
    try:
        data = scrape_article(request.url)
        return analyze_extracted_data(data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# NEW: PDF upload endpoint
@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        data = scrape_pdf(temp_path)
        return analyze_extracted_data(data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)