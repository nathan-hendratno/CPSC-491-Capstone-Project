import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from extractor_basic import scrape_article
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class URLRequest(BaseModel):
    url: str


@app.post("/summarize")
async def summarize_article(request: URLRequest):
    
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
  "topics": ["topic1", "topic2", "topic3"]
}}

Rules:
- key_points must have 3 to 5 items
- topics must have 2 to 5 items
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

        return {
            "title": data.get("title"),
            "author": data.get("author"),
            "publication_date": data.get("publication_date"),
            "summary": analysis.get("summary"),
            "key_points": analysis.get("key_points", []),
            "tone": analysis.get("tone"),
            "bias": analysis.get("bias"),
            "topics": analysis.get("topics", [])
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))