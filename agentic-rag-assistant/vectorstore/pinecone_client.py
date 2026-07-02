import os
import hashlib
import logging
from pinecone import Pinecone
from dotenv import load_dotenv
from data_pipeline.embedder import get_embeddings

# ---------------- INIT ----------------
load_dotenv()

logger = logging.getLogger(__name__)

INDEX_NAME = "agentic-rag-orchestrator"

api_key = os.getenv("PINECONE_API_KEY")

if not api_key:
    raise ValueError("PINECONE_API_KEY not found in .env")

pc = Pinecone(api_key=api_key)
index = pc.Index(INDEX_NAME)

# ---------------- VECTOR ID ----------------
def build_vector_id(source: str, chunk_id: int) -> str:
    raw = f"{source}_{chunk_id}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

# ---------------- UPSERT ----------------
def upsert_vectors(vectors, doc):

    if not vectors:
        return 0

    payload = []

    for item in vectors:
        try:
            payload.append({
                "id": build_vector_id(
                    doc["source"],
                    item["chunk_id"]
                ),
                "values": item["embedding"],
                "metadata": {
                    "doc_id": doc["source"],
                    "source": doc["source"],
                    "type": doc["type"],
                    "chunk_id": item["chunk_id"],
                    "text": item["text"][:6000]
                    # "text": item["text"][:2000]
                }
            })

        except Exception as e:
            logger.error(f"Vector build failed: {e}")

    if not payload:
        return 0

    try:
        index.upsert(vectors=payload)
        logger.info(f"Inserted {len(payload)} vectors")
        return len(payload)

    except Exception as e:
        logger.error(f"Pinecone upsert failed: {e}")
        return 0

def query_vectors(question: str, top_k: int = 4):

    # Guard: empty question
    if not question or not question.strip():
        logger.warning("query_vectors called with empty question")
        return []

    try:
        # Guard: embedding returned empty list
        embeddings = get_embeddings([question])

        if not embeddings:
            logger.error(f"Embedding returned empty for question: {question}")
            return []

        query_embedding = embeddings[0].get("embedding")

        # Guard: embedding key missing
        if not query_embedding:
            logger.error(f"Embedding key missing for question: {question}")
            return []

        result = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Guard: no matches returned
        if not result or not result.matches:
            logger.warning(f"No matches found for question: {question}")
            return []

        docs = []

        for match in result.matches:
            docs.append({
                "id": match.id,
                "score": float(match.score),
                "metadata": (match.metadata or {})
            })

        return docs

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return []

# ---------------- STATS (DEBUG ONLY) ----------------
def get_index_stats():
    try:
        return index.describe_index_stats()

    except Exception as e:
        logger.error(f"Stats failed: {e}")
        return None

def rerank_chunks(question, chunks):

    q_words = set(question.lower().split())

    def score(chunk):
        text = chunk["metadata"]["text"].lower()
        return sum(1 for w in q_words if w in text)

    return sorted(chunks, key=score, reverse=True)

def delete_all_vectors():
    index.delete(delete_all=True)
    return "All vectors deleted"

def delete_by_source(source: str):
    """
    Deletes only one document (all its chunks)
    """
    index.delete(
        filter={
            "source": {"$eq": source}
        }
    )

def get_all_sources():
    """
    Returns unique document sources from Pinecone metadata.
    """

    stats = index.describe_index_stats()

    # NOTE: Pinecone does not directly return all metadata,
    # so we must query a sample OR use namespace strategy.

    query_result = index.query(
        vector=[0] * 3072,  # dummy vector (match your embedding dim)
        top_k=1000,
        include_metadata=True
    )

    sources = set()

    for match in query_result["matches"]:
        meta = match.get("metadata", {})
        if "source" in meta:
            sources.add(meta["source"])

    return list(sources)