import os
import requests
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")


def classify_news(content: str) -> str:

    url = "https://api.sarvam.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sarvam-m",
        "messages": [
            {
                "role": "system",
                "content": """
Classify petroleum news into one category:
Crude / Petroleum / Gas / Policy

Return ONLY the category name.
"""
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        category = data["choices"][0]["message"]["content"].strip()

        if category not in ["Crude", "Petroleum", "Gas", "Policy"]:
            return "Petroleum"

        return category

    except Exception as e:
        print("Classification Error:", e)
        return "Petroleum"