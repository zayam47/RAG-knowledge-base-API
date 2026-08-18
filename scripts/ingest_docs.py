"""
Bulk-ingest all .md/.txt files from data/sample_docs into the vector store.

Run this once before starting the API server:
    python scripts/ingest_docs.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag import ingest_document

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sample_docs")


def main():
    if not os.path.isdir(DOCS_DIR):
        print(f"No docs directory found at {DOCS_DIR}")
        return

    total_chunks = 0
    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith((".md", ".txt")):
            continue

        path = os.path.join(DOCS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        num_chunks = ingest_document(text, source=filename)
        total_chunks += num_chunks
        print(f"Ingested {filename}: {num_chunks} chunks")

    print(f"\nDone. Total chunks stored: {total_chunks}")


if __name__ == "__main__":
    main()
