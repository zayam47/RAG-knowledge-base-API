"""
Core RAG orchestration: chunking + retrieve-then-generate pipeline.
"""

from typing import List, Dict
import re

from app.vectorstore import VectorStore
from app.generator import generate_answer

_store: VectorStore | None = None


def get_store() -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore()
    return _store


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> List[str]:
    """
    Split text into overlapping word-based chunks.

    Overlap keeps context from being cut off mid-idea at chunk boundaries,
    which improves retrieval quality for questions that span two sentences.
    """
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split(" ")

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def ingest_document(text: str, source: str) -> int:
    """Chunk a document and store it in the vector database."""
    chunks = chunk_text(text)
    store = get_store()
    return store.add_chunks(chunks, sources=[source] * len(chunks))


def answer_question(question: str, top_k: int = 4) -> Dict:
    """Full RAG flow: retrieve relevant chunks, then generate a grounded answer."""
    store = get_store()
    retrieved = store.query(question, top_k=top_k)
    answer = generate_answer(question, retrieved)

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {"source": r["source"], "similarity": r["similarity"]} for r in retrieved
        ],
    }
