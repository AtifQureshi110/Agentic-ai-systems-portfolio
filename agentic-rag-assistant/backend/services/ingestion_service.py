from data_pipeline.ingestion import ingest_document
from data_pipeline.ingestion import normalize_source
from vectorstore.pinecone_client import get_all_sources

def ingest_source(source: str, force_update: bool = False):

    normalized = normalize_source(source)

    existing_sources = get_all_sources()

    if normalized in existing_sources and not force_update:
        return {
            "success": False,
            "message": "Source already exists. Set force_update=true to update.",
            "inserted": 0,
            "source": normalized
        }

    result = ingest_document(source)

    return {
        "success": True,
        "message": "Document ingested successfully.",
        "inserted": result["inserted"],
        "source": normalized
    }