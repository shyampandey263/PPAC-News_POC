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
import logging

load_dotenv()

# ✅ Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ✅ Telegram Config
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ Missing TELEGRAM_TOKEN or CHAT_ID in .env")

bot = Bot(token=TOKEN)

# ✅ Category keywords
CATEGORIES = {
    "Crude": ["crude", "oil", "brent", "opec", "wti"],
    "Petroleum": ["petrol", "diesel", "refinery", "petroleum", "ppac"],
    "Gas": ["lng", "gas", "lpg", "natural gas"],
}

# ✅ Track sent URLs to avoid duplicates
sent_urls = set()

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
        if len(message) > 3500:
            message = message[:3500] + "..."
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode="HTML"
        )
        logger.info("✅ Telegram message sent")
    except Exception as e:
        logger.error(f"❌ Telegram Error: {e}")

# ✅ Main News Processing — ONLY 1 article per run
async def process_news():
    logger.info("🔄 Fetching & processing news...")

    try:
        news_list = fetch_news()
    except Exception as e:
        logger.error(f"❌ News fetch failed: {e}")
        return

    if not news_list:
        logger.warning("⚠️ No news fetched")
        return

    # ✅ Only 1 article per scheduled run
    for article in news_list[:1]:
        try:
            title = article.get("title", "")
            url = article.get("url", "")

            # ✅ Skip already sent news
            if url in sent_urls:
                logger.info(f"⏭️ Skipping duplicate: {title}")
                continue  # ✅ Fixed: was 'return', now 'continue'

            # ✅ AI Summary
            summary = summarize_news(title)
            summary = summary[:300]

            # ✅ Detect category
            category = detect_category(title)

            # ✅ Save to DB
            save_news(
                title=title,
                summary=summary,
                category=category,
                url=url
            )

            # ✅ Mark as sent
            sent_urls.add(url)

            # ✅ Telegram Message with clickable link
            message = f"""🛢️ <b>PPAC Petroleum Intelligence</b>

📌 <b>Category:</b> {category}

📰 <b>{title}</b>

🤖 <b>AI Summary:</b>
{summary}

🔗 <a href="{url}">Read Full Article</a>"""

            await send_to_telegram(message)
            logger.info(f"✅ Sent: {category} — {title[:50]}")

        except Exception as e:
            logger.error(f"❌ Processing Error: {e}")

# ✅ Scheduler Wrapper
def run_async_job():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_news())
        loop.close()
    except Exception as e:
        logger.error(f"❌ Job runner failed: {e}")

# ✅ 10:00 AM IST = 04:30 UTC
# ✅ 04:45 PM IST = 11:15 UTC  ← updated
schedule.every().day.at("04:30").do(run_async_job)
schedule.every().day.at("11:15").do(run_async_job)  # ← changed from 09:45 to 11:15

logger.info("✅ Scheduler Started — News at 10:00 AM & 4:45 PM IST")
logger.info("⏳ Waiting for scheduled time...")

# ✅ Infinite loop
while True:
    schedule.run_pending()
    time.sleep(60)