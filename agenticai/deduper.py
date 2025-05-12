# deduper.py
import json, os
import hashlib

HISTORY = "data/history.json"

def _load_history() -> list[dict]:
    if not os.path.exists(HISTORY):
        return []
    with open(HISTORY, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_history(hist: list[dict]):
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2)

def dedupe(articles: list[dict]) -> list[dict]:
    history = _load_history()
    seen_titles = {a.get("title", "") for a in history}
    seen_bodies = {a.get("body", "") for a in history}
    unique = []
    for a in articles:
        title = a.get("title", "")
        body = a.get("body", "")
        if title not in seen_titles and body not in seen_bodies:
            unique.append(a)
            seen_titles.add(title)
            seen_bodies.add(body)
    history.extend(unique)
    _save_history(history)
    return unique  # uses hashlib for IDs if desired :contentReference[oaicite:10]{index=10}
