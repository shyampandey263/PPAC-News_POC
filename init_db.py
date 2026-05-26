import sqlite3

# ✅ Connect to database
conn = sqlite3.connect("news.db")

cursor = conn.cursor()

# ✅ Create news table
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    category TEXT,

    summary TEXT,

    url TEXT UNIQUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

conn.close()

print("✅ Database initialized successfully")