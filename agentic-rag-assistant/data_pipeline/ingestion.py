from data_pipeline.loader import load_document
from data_pipeline.splitter import split_text
from data_pipeline.embedder import get_embeddings
from vectorstore.pinecone_client import upsert_vectors


def ingest_document(source):

    #  LOAD
    doc = load_document(source)

    # SAFETY CHECK (IMPORTANT)
    if not doc or not doc.get("content"):
        return {
            "metadata": doc,
            "chunks": [],
            "vectors": [],
            "inserted": 0
        }

    # SPLIT
    chunks = split_text(doc["content"])

    # Extra safety check
    if not chunks:
        return {
            "metadata": doc,
            "chunks": [],
            "vectors": [],
            "inserted": 0
        }

    # EMBED
    vectors = get_embeddings(chunks)

    # Extra safety check
    if not vectors:
        return {
            "metadata": doc,
            "chunks": [],
            "vectors": [],
            "inserted": 0
        }

    # STORE IN PINECONE
    inserted = upsert_vectors(vectors, doc)

    # RETURN FULL PIPELINE RESULT
    return {
        "metadata": doc,
        "chunks": chunks,
        "vectors": vectors,
        "inserted": inserted
    }


# THIS code FIXES

# Prevents crash on empty document
# Prevents crash on empty chunks
# Prevents crash on failed embeddings
# Safe Pinecone insertion
# Clean production-style pipeline