import schedule
import time
import asyncio
import requests
from news_fetcher import fetch_news
from ai_summarizer import summarize_news
from database import save_news
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

# ✅ Telegram Config
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# ✅ Category keywords
CATEGORIES = {
    "Crude": ["crude", "oil", "brent", "opec"],
    "Petroleum": ["petrol", "diesel", "refinery"],
    "Gas": ["lng", "gas", "lpg"],
}


# ✅ Detect Category
def detect_category(title):

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():

        for keyword in keywords:

            if keyword in title_lower:
                return category

    return "General"


# ✅ Async Send Function
async def send_to_telegram(message):

    try:

        # Telegram safe limit
        if len(message) > 3500:
            message = message[:3500] + "..."

        await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print("✅ Telegram message sent")

    except Exception as e:

        print("❌ Telegram Error:", e)


# ✅ Main News Processing
async def process_news():

    print("🔄 Fetching & processing news...")

    news_list = fetch_news()

    if not news_list:

        print("⚠️ No news fetched")

        return

    for article in news_list[:5]:

        try:

            title = article.get("title", "")
            url = article.get("url", "")

            # ✅ AI Summary
            summary = summarize_news(title)

            # ✅ Shorten summary
            summary = summary[:300]

            # ✅ Detect category
            category = detect_category(title)

            # ✅ Save DB
            save_news(
                title=title,
                summary=summary,
                category=category,
                url=url
            )

            # ✅ Telegram Message
            message = f"""
🛢️ PPAC Petroleum Intelligence

📌 Category: {category}

📰 {title}

🤖 AI Summary:
{summary}

🔗 {url}
"""

            # ✅ Send Telegram
            await send_to_telegram(message)

            print(f"✅ Sent: {category}")

            # small delay
            await asyncio.sleep(2)

        except Exception as e:

            print("❌ Processing Error:", e)


# ✅ Scheduler Wrapper
def run_async_job():

    asyncio.run(process_news())


# ✅ Schedule every 5 minutes
schedule.every(5).minutes.do(run_async_job)

print("✅ Scheduler Started...")


# ✅ Run once immediately
run_async_job()


# ✅ Infinite loop
while True:

    schedule.run_pending()

    time.sleep(30)