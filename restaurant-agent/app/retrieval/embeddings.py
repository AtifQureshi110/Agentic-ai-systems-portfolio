from functools import lru_cache
from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings


@lru_cache
def get_embedder() -> GoogleGenerativeAIEmbeddings:
    """
    Returns a single shared Gemini embeddings client, built once per process.
    retrieval/ingest.py and any query-time retrieval should import `embedder`
    from here rather than instantiating their own.
    """
    return GoogleGenerativeAIEmbeddings(
        model=settings.gemini_embed_model,
        google_api_key=settings.gemini_api_key,
        output_dimensionality=settings.embedding_dimension,
    )


# Shared instance — import directly: `from app.retrieval.embeddings import embedder`
embedder = get_embedder()


def embed_text(text: str) -> List[float]:
    """Embed a single piece of text (e.g. a query at retrieval time)."""
    return embedder.embed_query(text)


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Embed multiple chunks at once (used during ingestion)."""
    return embedder.embed_documents(texts)