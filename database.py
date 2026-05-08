import sqlite3
import os
from datetime import datetime

# ✅ Absolute DB Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "news.db")

# ✅ Connect DB
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


# ✅ Create Table
def create_table():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        summary TEXT,
        category TEXT,
        url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    print("✅ news table created successfully")


# ✅ Save News
def save_news(title, summary, category, url):

    try:
        cursor.execute("""
        INSERT INTO news (title, summary, category, url)
        VALUES (?, ?, ?, ?)
        """, (
            title,
            summary,
            category,
            url
        ))

        conn.commit()

        print("✅ News saved:", title)

        return True

    except sqlite3.IntegrityError:

        print("⚠️ Duplicate news skipped")

        return False

    except Exception as e:

        print("❌ DB Insert Error:", e)

        return False


# ✅ Fetch Latest News
def get_latest_news(limit=10):

    try:
        cursor.execute("""
        SELECT category, summary, url, created_at
        FROM news
        ORDER BY created_at DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

        return rows

    except Exception as e:

        print("❌ Fetch Error:", e)

        return []


# ✅ Initialize Table
create_table()