# extractor.py
import os, requests

ASI_URL = "https://api.asi1.ai/v1/chat/completions"
ASI_KEY = os.getenv("ASI_KEY")

def extract_keywords(text: str) -> list[str]:
    """Extract 1–2 image-search keywords using ASI-1 Mini, or return [] on failure."""
    payload = {
        "model": "asi1-mini",
        "messages": [
            {"role":"system", "content":"Extract 1–2 short keyword phrases for image search."},
            {"role":"user",   "content": text}
        ],
        "temperature": 0.2
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('ASI_KEY')}",
        "Content-Type": "application/json"
    }

    resp = requests.post(ASI_URL, json=payload, headers=headers)
    try:
        data = resp.json()
    except ValueError:
        print("⚠️ Non-JSON response from ASI:", resp.text)
        return []

    if not resp.ok:
        print(f"⚠️ ASI returned {resp.status_code}:", data)
        return []

    if "error" in data:
        print("⚠️ ASI error:", data["error"])
        return []

    choices = data.get("choices")
    if not choices or not isinstance(choices, list):
        print("⚠️ Unexpected ASI format:", data)
        return []

    content = choices[0].get("message", {}).get("content")
    if not content:
        print("⚠️ ASI returned empty content:", data)
        return []

    # Split on commas, trim, drop empty strings
    return [k.strip() for k in content.split(",") if k.strip()]
