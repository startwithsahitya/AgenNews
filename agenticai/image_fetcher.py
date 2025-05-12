# image_fetcher.py
import time
from duckduckgo_search import DDGS

def fetch_image(keywords: list[str]) -> str | None:
    """Return the first DuckDuckGo image URL matching any of the keywords, with rate limit handling."""
    with DDGS() as ddgs:
        for kw in keywords:
            try:
                results = ddgs.images(kw, max_results=1)
                if results:
                    return results[0]["image"]
                time.sleep(1)  # Add delay to avoid rate limit
            except Exception as e:
                print(f"DuckDuckGo image search error for '{kw}': {e}")
                time.sleep(2)  # Wait a bit longer on error
    return None

