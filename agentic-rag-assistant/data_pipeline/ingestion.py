from data_pipeline.loader import load_document
from data_pipeline.splitter import split_text
from data_pipeline.embedder import get_embeddings


def ingest_document(source):

    # 1 Load
    doc = load_document(source)
    
    # 2 Split
    chunks = split_text(doc["content"])

    # 3 Embed
    vectors = get_embeddings(chunks)

    # Return complete object
    return {
        "metadata": doc,
        "chunks": chunks,
        "vectors": vectors
    }
