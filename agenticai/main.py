# main.py
from scraper import fetch_news
from deduper import dedupe
from cleaner import clean_and_format
from dotenv import load_dotenv
import json
import os

load_dotenv()

def main():
    print("1. Scraping raw news…")
    raw     = fetch_news(limit=20)

    print("2. Deduplicating…")
    unique  = dedupe(raw)

    print("3. Cleaning & formatting…")
    final   = clean_and_format(unique)

    print(f"✅ Pipeline complete: {len(final)} articles ready in data/final_news.json")

    # Save final_news.json to Flutter assets location using absolute path
    default_image = "https://images.unsplash.com/photo-1465101046530-73398c7f28ca"
    for article in final:
        if not article.get("image") or not str(article["image"]).strip():
            article["image"] = default_image
    flutter_data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../agennews/assets/data/news_data.json")
    )
    with open(flutter_data_path, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"✅ Done")

if __name__ == "__main__":
    main()
