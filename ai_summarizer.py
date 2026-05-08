import requests
import os
from dotenv import load_dotenv

# ✅ Load ENV
load_dotenv()

# ✅ Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =========================================================
# ✅ AI SUMMARIZER FUNCTION
# =========================================================

def summarize_news(news_text):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a petroleum intelligence analyst for PPAC India.

Summarize the following news in EXACTLY 50 words.

Requirements:
- Professional tone
- Mention market impact
- Mention India relevance if applicable
- NO reasoning
- NO thinking process
- NO bullet points
- ONLY final summary

News:
{news_text}
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 120
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        result = response.json()

        summary = result["choices"][0]["message"]["content"]

        # ✅ Remove thinking traces if any
        if "<think>" in summary:

            if "</think>" in summary:
                summary = summary.split("</think>")[-1]

        return summary.strip()

    except Exception as e:

        print("❌ AI Summary Error:", e)

        return "AI summary unavailable."