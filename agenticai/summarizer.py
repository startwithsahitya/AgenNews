# summarizer.py
import os
import requests

ASI_URL = "https://api.asi1.ai/v1/chat/completions"
ASI_KEY = os.getenv("ASI_KEY")

def summarize(text: str) -> str:
    payload = {
        "model": "asi1-mini",
        "messages": [
            {"role": "system", "content": "Summarize the following news article in 2–3 concise sentences."},
            {"role": "user",   "content": text}
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
        # Non-JSON response
        print("⚠️ Non-JSON response from ASI API:", resp.text)
        return text

    # Handle HTTP errors
    if not resp.ok:
        print(f"⚠️ ASI API returned status {resp.status_code}: {data}")
        return text

    # Handle API-level errors
    if "error" in data:
        print("⚠️ ASI API error:", data["error"])
        return text

    # Finally, safely extract the summary
    choices = data.get("choices")
    if not choices or not isinstance(choices, list):
        print("⚠️ Unexpected ASI response format:", data)
        return text

    # Everything looks good
    summary = choices[0].get("message", {}).get("content")
    return summary.strip() if summary else text
