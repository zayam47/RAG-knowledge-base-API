"""
Embedding model wrapper.

Uses sentence-transformers (all-MiniLM-L6-v2) to convert text chunks into
dense vector embeddings for semantic similarity search. This model is small
(~80MB), runs fully on CPU, and is downloaded once from Hugging Face on
first run (then cached locally).
"""

from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load and cache the embedding model (loaded once per process)."""
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of text chunks into vectors."""
    model = get_embedding_model()
    vectors = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Embed a single user query into a vector."""
    model = get_embedding_model()
    vector = model.encode([query], show_progress_bar=False, normalize_embeddings=True)
    return vector[0].tolist()
