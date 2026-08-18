# Retrieval-Augmented Generation (RAG) Concepts

Retrieval-Augmented Generation combines a search step with a language
model's generation step. Instead of relying only on what a language model
memorized during training, the system first retrieves relevant text
passages from an external knowledge base, then feeds those passages to the
model as context so its answer is grounded in real, up-to-date source
material.

Text is usually split into smaller chunks before being stored, because
embedding models and retrieval work better on focused passages than on
entire documents. Chunk size is a tradeoff: chunks that are too small lose
context, while chunks that are too large dilute the similarity signal and
make retrieval less precise. Overlapping chunks help avoid losing meaning
at chunk boundaries.

An embedding model converts text into a dense numeric vector such that
semantically similar pieces of text end up close together in vector space.
Sentence-transformer models are commonly used for this because they are
trained specifically to produce useful sentence and paragraph level
embeddings, unlike raw word embeddings.

A vector database stores these embeddings alongside the original text and
supports fast nearest-neighbor search, so that given a new query vector it
can quickly return the most similar stored chunks. Popular options include
Chroma, FAISS, Pinecone, and Weaviate, each with different tradeoffs
around scale, hosting, and ease of local development.

The final generation step takes the retrieved chunks and the user's
question, combines them into a single prompt, and asks a language model to
answer using only that provided context. This reduces hallucination
compared to asking the model the question directly, because the model has
relevant facts in front of it rather than relying purely on memorized
training data.
