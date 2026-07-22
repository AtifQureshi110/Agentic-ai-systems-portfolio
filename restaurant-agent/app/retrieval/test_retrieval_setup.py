"""
Quick manual test — run directly: python -m app.retrieval.test_retrieval_setup
Confirms Pinecone connection AND Gemini embeddings are working together,
before building ingest.py on top of them.
"""

from app.retrieval.pinecone_client import get_index, create_index
from app.retrieval.embeddings import embed_text
from app.core.config import settings

if __name__ == "__main__":
    print("Step 1: Testing Pinecone connection...")
    create_index()
    index = get_index()
    stats = index.describe_index_stats()
    print("Pinecone connected. Stats:", stats)

    print("\nStep 2: Testing Gemini embeddings...")
    vector = embed_text("What are your opening hours?")
    print("Embedding length:", len(vector))
    assert len(vector) == settings.embedding_dimension, "Dimension mismatch!"
    print("Embedding dimension matches config:", settings.embedding_dimension)

    print("\nStep 3: Testing upsert + query round-trip...")
    index.upsert(vectors=[{"id": "test-1", "values": vector, "metadata": {"text": "test faq"}}])
    result = index.query(vector=vector, top_k=1, include_metadata=True)
    print("Query result:", result)

    print("\nAll checks passed. Pinecone + Embeddings are working together.")
# python -m app.retrieval.test_retrieval_setup