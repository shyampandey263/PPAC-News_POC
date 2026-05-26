import requests
import os
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
print("Loaded GNEWS_API_KEY:", GNEWS_API_KEY)

def fetch_news():
    url = (
        f"https://gnews.io/api/v4/search?"
        f"q=crude oil OR petroleum OR LNG OR OPEC&"
        f"lang=en&"
        f"max=10&"
        f"apikey={GNEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            print("❌ GNews Error:", data)
            return []

        print(f"✅ Fetched {len(articles)} articles")

        for a in articles:
            print(f"🔗 URL: {a.get('url')} | Title: {a.get('title', '')[:50]}")

        return articles

    except Exception as e:
        print("❌ Fetch Error:", e)
        return []