import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from extractor_basic import scrape_article

app = FastAPI()

class URLRequest(BaseModel):
    url: str


@app.post("/summarize")
async def summarize_article(request: URLRequest):
    # Scrape article
    data = scrape_article(request.url)

    if not data or not data.get("text"):
        raise HTTPException(status_code=400, detail="Failed to scrape article")

    article_text = data["text"][:8000]  # smaller chunk for local models

    # Send to Ollama (local llama model)
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",   # change to "phi" or "gemma:2b" if RAM is low
                "prompt": f"Summarize the following article clearly and concisely:\n\n{article_text}",
                "stream": False
            },
            timeout=4800
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ollama request failed")

        summary = response.json()["response"]

        # Return to frontend
        return {
            "title": data["title"],
            "author": data["author"],
            "publication_date": data["publication_date"],
            "summary": summary.strip()
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))