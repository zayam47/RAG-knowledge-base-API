"""
Local, free generation model (no API key required).

Uses google/flan-t5-base, an open, ungated instruction-tuned model from
Hugging Face, run locally via transformers. Given the retrieved context
chunks and the user's question, it produces a grounded natural-language
answer. Downloaded once and cached locally on first run (~1GB).
"""

from functools import lru_cache
from typing import List, Dict

from transformers import pipeline

MODEL_NAME = "google/flan-t5-base"

PROMPT_TEMPLATE = """Answer the question using only the context below.
If the context does not contain the answer, say you don't have enough
information.

Context:
{context}

Question: {question}

Answer:"""


@lru_cache(maxsize=1)
def get_generator():
    """Load and cache the local text2text-generation pipeline."""
    return pipeline("text2text-generation", model=MODEL_NAME, max_new_tokens=256)


def build_context(chunks: List[Dict]) -> str:
    """Join retrieved chunks into a single context block for the prompt."""
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        parts.append(f"[{i}] (source: {chunk['source']})\n{chunk['text']}")
    return "\n\n".join(parts)


def generate_answer(question: str, retrieved_chunks: List[Dict]) -> str:
    """Generate a grounded answer from the question + retrieved context."""
    if not retrieved_chunks:
        return "I don't have enough information in the knowledge base to answer that."

    context = build_context(retrieved_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    generator = get_generator()
    output = generator(prompt, do_sample=False)
    return output[0]["generated_text"].strip()
