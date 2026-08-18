"""
Vector store wrapper around ChromaDB.

Stores chunked document text + embeddings on disk (persistent, no external
server required) and supports similarity search at query time.
"""

from typing import List, Dict
import chromadb
from chromadb.config import Settings

from app.embeddings import embed_texts, embed_query

PERSIST_DIR = "chroma_store"
COLLECTION_NAME = "fastapi_python_docs"


class VectorStore:
    def __init__(self, persist_dir: str = PERSIST_DIR):
        self.client = chromadb.PersistentClient(
            path=persist_dir, settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: List[str], sources: List[str]) -> int:
        """Embed and store a batch of text chunks with their source filenames."""
        if not chunks:
            return 0

        embeddings = embed_texts(chunks)
        start_id = self.collection.count()
        ids = [f"chunk_{start_id + i}" for i in range(len(chunks))]
        metadatas = [{"source": src} for src in sources]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        return len(chunks)

    def query(self, question: str, top_k: int = 4) -> List[Dict]:
        """Retrieve the top_k most relevant chunks for a question."""
        query_vector = embed_query(question)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
        )

        hits = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(docs, metas, dists):
            hits.append(
                {
                    "text": doc,
                    "source": meta.get("source", "unknown"),
                    "similarity": round(1 - dist, 4),
                }
            )
        return hits

    def count(self) -> int:
        return self.collection.count()
