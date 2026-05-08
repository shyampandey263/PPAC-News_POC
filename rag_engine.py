import sqlite3
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ✅ Absolute DB Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "news.db")

# ✅ Load Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")


# ✅ Fetch News From DB
def fetch_news_from_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, summary
        FROM news
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ✅ Build FAISS Index
def build_index():

    data = fetch_news_from_db()

    if not data:
        return None, None, None

    ids = [row[0] for row in data]
    texts = [row[1] for row in data]

    # 🔹 Generate embeddings
    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    # 🔹 Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, ids, texts


# ✅ Semantic Search
def search_similar(query, top_k=3):

    index, ids, texts = build_index()

    if index is None:
        return []

    # 🔹 Query embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    # 🔍 Search
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:

        if idx < len(texts):
            results.append(texts[idx])

    return results