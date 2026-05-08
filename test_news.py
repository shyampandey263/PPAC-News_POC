from news_fetcher import fetch_news

news = fetch_news()

for n in news:
    print("\nTITLE:", n["title"])