"""
Pinecone client setup — connects to the index using config from core/config.py
"""

from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings

_pc = None
_index = None


def get_client() -> Pinecone:
    """Return a singleton Pinecone client."""
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=settings.pinecone_api_key)
    return _pc


def create_index(dimension: int = 768):
    """Create the configured index if it doesn't already exist."""
    client = get_client()
    existing = [i["name"] for i in client.list_indexes()]
    if settings.pinecone_index_name not in existing:
        client.create_index(
            name=settings.pinecone_index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=settings.pinecone_environment),
        )
        print(f"Created index: {settings.pinecone_index_name}")
    else:
        print(f"Index already exists: {settings.pinecone_index_name}")


def get_index():
    """Return a singleton handle to the configured Pinecone index."""
    global _index
    if _index is None:
        client = get_client()
        _index = client.Index(settings.pinecone_index_name)
    return _index