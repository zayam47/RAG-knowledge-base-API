# RAG Knowledge Base API

A Retrieval-Augmented Generation (RAG) system built with **FastAPI**, exposing
a REST API that lets you ingest documents and ask natural-language questions
answered using only the retrieved, relevant content — grounded, not
hallucinated.

Built as a hands-on project to apply FastAPI + RAG concepts end-to-end:
chunking, embeddings, vector search, and local LLM generation, wired
together behind a clean API.

## Architecture

```
                ┌─────────────┐
   Document  →  │  Chunking   │  (overlapping word-based chunks)
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  Embedding  │  sentence-transformers
                │   Model     │  (all-MiniLM-L6-v2)
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   ChromaDB  │  persistent local vector store
                └──────┬──────┘
                       │  (on query: cosine similarity search)
                       ▼
   Question  →  ┌─────────────┐
                │  Retrieval  │  top-k relevant chunks
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  Local LLM  │  google/flan-t5-base
                │ Generation  │  (runs on CPU, no API key)
                └──────┬──────┘
                       │
                       ▼
                  Grounded Answer + Sources
```

**Stack:** FastAPI · sentence-transformers · ChromaDB · Hugging Face
transformers (flan-t5-base) · Pydantic

No paid API keys required — embeddings and generation both run locally.

## Setup

Requires Python 3.10+ and ~2GB free disk space for model downloads
(one-time, cached after first run).

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Ingest the sample knowledge base (FastAPI, Python async, RAG concepts)
python scripts/ingest_docs.py

# 4. Start the API server
uvicorn app.main:app --reload
```

The API will be live at `http://127.0.0.1:8000`. Interactive docs (Swagger
UI) are auto-generated at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Endpoint       | Description                                  |
|--------|----------------|-----------------------------------------------|
| GET    | `/health`      | Health check                                   |
| GET    | `/stats`       | Number of chunks currently stored              |
| POST   | `/ingest`      | Upload a `.txt`/`.md` file into the KB         |
| POST   | `/ingest/text` | Ingest raw text with a source name             |
| POST   | `/query`       | Ask a question, get a grounded answer + sources|

### Example: ask a question

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is dependency injection in FastAPI?", "top_k": 3}'
```

Response:
```json
{
  "question": "What is dependency injection in FastAPI?",
  "answer": "...",
  "sources": [
    {"source": "fastapi_basics.md", "similarity": 0.81},
    {"source": "rag_concepts.md", "similarity": 0.42}
  ]
}
```

### Example: ingest your own document

```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -F "file=@my_notes.md"
```

## Adding your own knowledge base

Drop `.md` or `.txt` files into `data/sample_docs/` and re-run
`python scripts/ingest_docs.py`, or use the `/ingest` endpoint to upload
files at runtime without restarting the server.

## Design notes

- **Chunking with overlap**: documents are split into ~500-word chunks with
  80-word overlap so context isn't lost at chunk boundaries.
- **Cosine similarity** is used for vector search (set on the ChromaDB
  collection), which works well with normalized sentence-transformer
  embeddings.
- **Grounded generation**: the LLM prompt explicitly instructs the model to
  answer only from the provided context and to say so if the answer isn't
  present, reducing hallucination.
- **Persistent storage**: ChromaDB persists to disk (`chroma_store/`), so
  the knowledge base survives server restarts — no need to re-ingest every
  time.

## Possible extensions

- Swap `flan-t5-base` for a larger local model (e.g. via `llama-cpp-python`)
  or a hosted API for higher-quality answers
- Add re-ranking of retrieved chunks before generation
- Add streaming responses for the `/query` endpoint
- Add authentication for multi-user knowledge bases
