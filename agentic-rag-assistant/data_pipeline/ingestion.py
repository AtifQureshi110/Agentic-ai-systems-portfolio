from data_pipeline.loader import load_document
from data_pipeline.splitter import split_text
from data_pipeline.embedder import get_embeddings
from vectorstore.pinecone_client import (
    upsert_vectors,
    delete_by_source,
    build_vector_id
)

import re
from urllib.parse import urlparse

def normalize_source(source: str) -> str:
    if not source:
        return source

    source = source.strip().lower()

    if source.startswith("http"):
        parsed = urlparse(source)
        netloc = parsed.netloc.replace("www.", "")
        path = parsed.path.rstrip("/")          # keep the path
        return netloc + path if path else netloc # e.g. "panaversity.org/courses"

    return source.replace("\\", "/").replace("www.", "").strip("/")

# ---------------- INGESTION PIPELINE ----------------
def ingest_document(source: str):
    """
    Production-grade ingestion pipeline:
    - Fully idempotent
    - Dedup-safe (no duplicate vectors)
    - Source canonicalization enforced
    """

    # STEP 0: NORMALIZE SOURCE (SINGLE TRUTH)
    normalized_source = normalize_source(source)

        # FIXED: wrapped in try/except so empty namespace doesn't crash
    try:
        delete_by_source(normalized_source)
    except Exception as e:
        print(f" Delete skipped (namespace may be empty): {e}")

    # STEP 2: LOAD DOCUMENT (RAW INPUT OK HERE)
    doc = load_document(source)

    if not doc or not doc.get("content"):
        return {
            "metadata": doc,
            "chunks": [],
            "vectors": [],
            "inserted": 0
        }

    # FORCE CONSISTENT SOURCE INSIDE DOC
    doc["source"] = normalized_source

    content = doc["content"]

    # STEP 3: SEMANTIC CHUNKING
    chunks = split_text(content)

    if not chunks:
        return {
            "metadata": doc,
            "chunks": [],
            "vectors": [],
            "inserted": 0
        }

    # STEP 4: EMBEDDINGS
    embeddings_output = get_embeddings(chunks)

    if not embeddings_output:
        return {
            "metadata": doc,
            "chunks": [],
            "vectors": [],
            "inserted": 0
        }

    # STEP 5: BUILD VECTOR PAYLOAD
    vectors = []

    for i, emb in enumerate(embeddings_output):
        vectors.append({
            "id": build_vector_id(normalized_source, i),
            "chunk_id": i,
            "text": chunks[i],
            "embedding": emb["embedding"],
            "metadata": {
                "source": normalized_source
            }
        })

    # STEP 6: UPSERT TO PINECONE
    inserted = upsert_vectors(vectors, doc)

    return {
        "metadata": doc,
        "chunks": chunks,
        "vectors": vectors,
        "inserted": inserted
    }
