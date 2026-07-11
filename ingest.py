import os
import pymssql
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

def get_log_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE '%Log'
    """)
    return [row["TABLE_NAME"] for row in cur.fetchall()]

def serialize_row(row):
    return " | ".join(f"{col}={val}" for col, val in row.items() if val is not None)

def ingest():
    conn = pymssql.connect(
        server = os.getenv("SERVER"),
        database = os.getenv("DB_NAME"),
        as_dict = True
    )
    chroma = chromadb.PersistentClient(path="./chroma_db")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    for table in get_log_tables(conn):
        cur = conn.cursor()
        cur.execute(f"SELECT TOP 5 * FROM [{table}]")
        rows = cur.fetchall()

        if not rows:
            print(f"Skipping {table} - no rows found")
            continue

        texts = [serialize_row(row) for row in rows]
        ids = [f"{table}_{i}" for i in range(len(texts))]
        metas = [{"table": table} for _ in texts]

        collection = chroma.get_or_create_collection(name=table.lower())
        embeddings = model.encode(texts).tolist()
        collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metas)
        print(f"Ingested {len(texts)} rows from {table}")

    conn.close()

if __name__ == "__main__":
    ingest()

