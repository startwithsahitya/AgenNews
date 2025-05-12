# cleaner.py
import json
from summarizer import summarize
from extractor import extract_keywords
from image_fetcher import fetch_image

def clean_and_format(raw_articles: list[dict]) -> list[dict]:
    formatted = []
    for art in raw_articles:
        # Use the original description if present, else fallback to body
        description = art.get("description") or art.get("body", "")

        # Generate a short summary for image search
        short_summary = summarize(art.get("body", ""))
        # Extract keywords for image search from the short summary
        kws = extract_keywords(short_summary)
        img = art.get("image") or fetch_image(kws)

        formatted.append({
            "image":       img,
            "title":       art["title"],
            "description": description,
            "genre":       "General",
            "date":        (art.get("published_date") or art["scraped_at"])[:10],
            "source":      art["source"]
        })
    with open("data/final_news.json", "w", encoding="utf-8") as f:
        json.dump(formatted, f, indent=2, ensure_ascii=False)
    return formatted
