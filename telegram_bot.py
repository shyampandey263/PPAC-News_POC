from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os
from dotenv import load_dotenv

from rag_engine import search_similar
from ai_summarizer import summarize_news

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


# =========================================================
# ✅ START COMMAND
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛢️ PPAC Petroleum Intelligence Bot Ready.\n\nAsk any petroleum or energy-related question."
    )


# =========================================================
# ✅ ASK HANDLER
# =========================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    question = update.message.text

    await update.message.reply_text("🔍 Analyzing petroleum intelligence...")

    try:

        # =================================================
        # ✅ RAG SEARCH
        # =================================================

        results = search_similar(question)

        if not results:

            await update.message.reply_text(
                "No relevant intelligence found."
            )

            return

        # =================================================
        # ✅ BUILD CONTEXT
        # =================================================

        context_text = "\n".join(results)

        prompt = f"""
You are a petroleum intelligence analyst for PPAC India.

Answer professionally using the context below.

Mention:
- Market trend
- Strategic impact
- India relevance

Context:
{context_text}

Question:
{question}
"""

        # =================================================
        # ✅ AI ANSWER
        # =================================================

        answer = summarize_news(prompt)

        # =================================================
        # ✅ SEND RESPONSE
        # =================================================

        await update.message.reply_text(answer)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error: {str(e)}"
        )


# =========================================================
# ✅ MAIN
# =========================================================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("✅ Telegram AI Bot Running...")

app.run_polling()