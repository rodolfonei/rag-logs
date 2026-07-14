# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG system for analyzing MSSQL database logs. It ingests log tables into a vector database and uses an LLM to answer questions about the logs.

## Commands

```bash
# Ingest logs from MSSQL to ChromaDB
python ingest.py

# Query the logs (uses default question)
python query.py

# Query with custom question (import and call from Python)
```

Requires Ollama running with llama3.2 model installed.

## Architecture

- **ingest.py**: Connects to MSSQL, finds tables ending in "Log", embeds TOP 5 rows per table using sentence-transformers (all-MiniLM-L6-v2), stores in ChromaDB
- **query.py**: Embeds user question, retrieves relevant log chunks from ChromaDB, sends context + question to Ollama (llama3.2) for analysis
- **chroma_db/**: Persistent ChromaDB storage (auto-created)

Environment variables in `.env`: `SERVER` (MSSQL host), `DB_NAME` (database name)