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

conn = pymssql.connect(
    server = os.getenv("SERVER"),
    database = os.getenv("DB_NAME"),
    as_dict = True
)
print(get_log_tables(conn))

