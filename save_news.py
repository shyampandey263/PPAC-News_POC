import sqlite3


# ✅ Save fetched news into SQLite
def save_news(articles):

    conn = sqlite3.connect("news.db")

    cursor = conn.cursor()

    inserted_count = 0

    for article in articles:

        summary = article.get("description")

        url = article.get("url")

        title = article.get("title", "")

        # ✅ Skip empty news
        if not summary or not url:
            continue

        # ✅ Auto category tagging
        text = (title + " " + summary).lower()

        if "opec" in text:
            category = "OPEC"

        elif "lng" in text:
            category = "LNG"

        elif "crude" in text:
            category = "Crude Oil"

        else:
            category = "Petroleum"

        try:

            cursor.execute("""
                INSERT INTO news (category, summary, url)
                VALUES (?, ?, ?)
            """, (category, summary, url))

            inserted_count += 1

        except sqlite3.IntegrityError:

            # ✅ Duplicate URL skipped
            pass

    conn.commit()

    conn.close()

    print(f"✅ Inserted {inserted_count} new articles")