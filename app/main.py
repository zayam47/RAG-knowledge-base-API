"""
FastAPI application exposing the RAG pipeline as a REST API.

Endpoints:
  GET  /health          - basic health check
  POST /ingest           - upload a .txt/.md file into the knowledge base
  POST /ingest/text      - ingest raw text directly (source name provided)
  POST /query             - ask a question, get a grounded answer + sources
  GET  /stats             - number of chunks currently stored
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from app.rag import ingest_document, answer_question, get_store

app = FastAPI(
    title="RAG Knowledge Base API",
    description="A retrieval-augmented generation service over Python/FastAPI docs.",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    question: str
    top_k: int = 4


class IngestTextRequest(BaseModel):
    text: str
    source: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def stats():
    return {"chunks_stored": get_store().count()}


@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".txt", ".md")):
        raise HTTPException(400, "Only .txt and .md files are supported")

    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore")

    if not text.strip():
        raise HTTPException(400, "File is empty")

    num_chunks = ingest_document(text, source=file.filename)
    return {"filename": file.filename, "chunks_added": num_chunks}


@app.post("/ingest/text")
def ingest_text(req: IngestTextRequest):
    if not req.text.strip():
        raise HTTPException(400, "Text is empty")

    num_chunks = ingest_document(req.text, source=req.source)
    return {"source": req.source, "chunks_added": num_chunks}


@app.post("/query")
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(400, "Question is empty")

    if get_store().count() == 0:
        raise HTTPException(400, "Knowledge base is empty. Ingest documents first.")

    return answer_question(req.question, top_k=req.top_k)
