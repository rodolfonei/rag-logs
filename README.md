# RAG Logs

A Retrieval-Augmented Generation (RAG) system for analyzing MSSQL database logs. It ingests log tables into a vector database and uses an LLM to answer questions about the logs.

## Features

- Ingests MSSQL log tables into ChromaDB vector database
- Uses sentence-transformers for embeddings (all-MiniLM-L6-v2)
- Uses Ollama with llama3.2 for natural language queries
- Supports querying specific tables or all log tables at once

## Prerequisites

1. **Python 3.8+**
2. **MSSQL Server** with database containing tables ending in "Log"
3. **Ollama** installed with llama3.2 model:
   ```bash
   ollama pull llama3.2
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-logs
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   # or: source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:
   ```
   SERVER=your_mssql_host
   DB_NAME=your_database_name
   ```

## Usage

### Ingest Logs

To ingest log tables from MSSQL into ChromaDB:

```bash
python ingest.py
```

This will:
- Find all tables ending in "Log" in the configured database
- Extract TOP 5 rows from each table
- Embed and store them in ChromaDB (persistent storage in `chroma_db/`)

### Query Logs

To ask questions about the logs using natural language:

```bash
python query.py
```

This runs the default question: *"What errors occurred most frequently through the whole database?"*

#### Custom Questions

Import and use the `query` function in Python:

```python
from query import query

# Query all log tables
query("What are the most recent errors in the system?")

# Query a specific table
query("Show me recent login failures", table="LoginLog")
```

## Project Structure

```
rag-logs/
├── .env              # Environment variables (MSSQL connection)
├── .gitignore        # Git ignore rules
├── .venv/            # Virtual environment
├── chroma_db/        # Persistent ChromaDB storage (auto-created)
├── CLAUDE.md         # Claude Code instructions
├── ingest.py         # Script to ingest logs to vector DB
├── query.py          # Script to query logs using RAG
└── requirements.txt  # Python dependencies
```

## Architecture

- **ingest.py**: Connects to MSSQL, finds tables ending in "Log", embeds TOP 5 rows per table using sentence-transformers (all-MiniLM-L6-v2), stores in ChromaDB
- **query.py**: Embeds user question, retrieves relevant log chunks from ChromaDB, sends context + question to Ollama (llama3.2) for analysis

## License

MIT