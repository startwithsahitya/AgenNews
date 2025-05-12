# scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def extract_metadata(soup):
    # Title
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"] if title_tag else "Untitled"  # :contentReference[oaicite:5]{index=5}

    # Published Date
    date_tag = soup.find("meta", property="article:published_time")
    date = date_tag["content"] if date_tag else None

    # Author
    author_tag = soup.find("meta", {"name": "byl"})
    author = author_tag["content"] if author_tag else "BBC News Staff"

    return title, date, author

def fetch_news(limit=10):
    res  = requests.get("https://www.bbc.com/news")  # :contentReference[oaicite:6]{index=6}
    soup = BeautifulSoup(res.text, "html.parser")

    links   = soup.select("a[href^='/news/']")
    seen, articles = set(), []

    for link in links:
        path = link['href']
        if path in seen or len(articles) >= limit:
            continue
        seen.add(path)
        url = "https://www.bbc.com" + path

        try:
            art_res = requests.get(url)
            art_soup = BeautifulSoup(art_res.text, "html.parser")
            paragraphs = art_soup.find_all("p")
            body = " ".join(p.get_text() for p in paragraphs[:10] if len(p.get_text()) > 30)
            if len(body) < 100: 
                continue

            title, date, author = extract_metadata(art_soup)
            articles.append({
                "url": url,
                "title": title,
                "body": body,
                "published_date": date,
                "author": author,
                "source": "BBC News",
                "scraped_at": datetime.utcnow().isoformat()
            })
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Save raw data
    with open("data/raw_news.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)
    return articles
