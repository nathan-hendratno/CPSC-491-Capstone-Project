import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from extractor_basic import scrape_article
from openai import OpenAI

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class URLRequest(BaseModel):
    url: str


@app.post("/summarize")
async def summarize_article(request: URLRequest):
    # Scrape article
    data = scrape_article(request.url)

    if not data or not data.get("text"):
        raise HTTPException(status_code=400, detail="Failed to scrape article")

    article_text = data["text"][:12000]  

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes news articles clearly and concisely."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following article:\n\n{article_text}"
                }
            ],
            temperature=0.3
        )

        summary = response.choices[0].message.content

        return {
            "title": data["title"],
            "author": data["author"],
            "publication_date": data["publication_date"],
            "summary": summary.strip()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))