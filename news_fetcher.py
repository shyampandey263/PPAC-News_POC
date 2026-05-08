import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print("Loaded NEWS_API_KEY:", NEWS_API_KEY)


def fetch_news():

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=crude oil OR petroleum OR LNG OR OPEC&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize=10&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        if data.get("status") != "ok":

            print("❌ News API Error:", data)

            return []

        articles = data.get("articles", [])

        print(f"✅ Fetched {len(articles)} news articles")

        return articles

    except Exception as e:

        print("❌ Fetch Error:", e)

        return []