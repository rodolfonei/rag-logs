import chromadb
from sentence_transformers import SentenceTransformer
import ollama

def query(question: str, table: str = None):
    chroma = chromadb.PersistentClient(path="./chroma_db")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    q_embedding = model.encode([question])[0].tolist()

    # Query one table or all collections
    collections = [chroma.get_collection(table.lower())] if table \
        else chroma.list_collections()

    chunks = []
    for col in collections:
        results = col.query(query_embeddings=[q_embedding], n_results=5)
        chunks.extend(results["documents"][0])
    context = "\n\n".join(chunks)
    prompt = f"""You are analyzing application log from a MSSQL database.

Relevant log entries:
{context}

Question: {question}

Provide a clear, concise analysis based only on the log entries above."""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    print(response["message"]["content"])

if __name__ == "__main__":
    query("What errors occurred most frequently through the whole database?")