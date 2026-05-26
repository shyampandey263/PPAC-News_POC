from fastapi import FastAPI
import sqlite3
import os
from datetime import datetime

# 🔹 RAG imports
from rag_engine import search_similar

# 🔹 AI summarizer
from ai_summarizer import summarize_news

app = FastAPI(title="PPAC Petroleum Intelligence API")

# ✅ Absolute DB Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "news.db")


# ✅ Database Connection
def get_db_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ✅ Root Endpoint
@app.get("/")
def root():

    return {
        "message": "PPAC Petroleum Intelligence API is running 🚀",
        "timestamp": datetime.now()
    }


# ✅ Get All News
@app.get("/news")
def get_all_news(limit: int = 10):

    try:

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, summary, url, created_at
            FROM news
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

        conn.close()

        return {
            "count": len(rows),
            "news": [
                {
                    "category": row["category"],
                    "summary": row["summary"],
                    "url": row["url"],
                    "time": row["created_at"]
                }
                for row in rows
            ]
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ✅ Get Category-wise News
@app.get("/news/{category}")
def get_news_by_category(category: str, limit: int = 5):

    try:

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT summary, url, created_at
            FROM news
            WHERE category = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (category.capitalize(), limit))

        rows = cursor.fetchall()

        conn.close()

        return {
            "category": category,
            "count": len(rows),
            "news": [
                {
                    "summary": row["summary"],
                    "url": row["url"],
                    "time": row["created_at"]
                }
                for row in rows
            ]
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ✅ Search News
@app.get("/search")
def search_news(query: str, limit: int = 5):

    try:

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, summary, url, created_at
            FROM news
            WHERE summary LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (f"%{query}%", limit))

        rows = cursor.fetchall()

        conn.close()

        return {
            "query": query,
            "count": len(rows),
            "results": [
                {
                    "category": row["category"],
                    "summary": row["summary"],
                    "url": row["url"],
                    "time": row["created_at"]
                }
                for row in rows
            ]
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ✅ AI RAG Question Answering
@app.post("/ask")
def ask_question(question: str):

    try:

        # 🔍 Retrieve relevant news chunks
        results = search_similar(question)

        # ✅ No result found
        if not results:

            return {
                "question": question,
                "answer": "No relevant information found."
            }

        # ✅ Take top 3 relevant results only
        top_results = results[:3]

        # ✅ Build context
        context = "\n\n".join(top_results)

        # ✅ AI Prompt
        prompt = f"""
You are a petroleum intelligence analyst.

Answer ONLY using the context below.

Provide:
1. Key insight
2. Market impact
3. India relevance

Context:
{context}

Question:
{question}
"""

        # 🤖 Generate AI Answer
        answer = summarize_news(prompt)

        # ✅ Better formatting
        formatted_answer = (
            answer.replace(
                "Key insight:",
                "🔍 Key Insight:\n"
            )
            .replace(
                "Market impact:",
                "\n\n📈 Market Impact:\n"
            )
            .replace(
                "India relevance:",
                "\n\n🇮🇳 India Relevance:\n"
            )
        )

        return {
            "question": question,
            "sources_used": len(top_results),
            "answer": formatted_answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }