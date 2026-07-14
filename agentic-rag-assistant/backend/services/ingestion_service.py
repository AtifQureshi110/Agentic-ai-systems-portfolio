from data_pipeline.ingestion import ingest_document
# Import the function that actually performs ingestion: 
# reading the source, chunking it, embedding it, and storing it in the vector DB.

from data_pipeline.ingestion import normalize_source
# Import a helper that standardizes the source string 
# (e.g., trims whitespace, lowercases, resolves relative paths, 
# strips trailing slashes) so duplicate checks work reliably.

from vectorstore.pinecone_client import get_all_sources
# Import a function that fetches the list of sources 
# already stored in Pinecone, used to detect duplicates.

def ingest_source(source: str, force_update: bool = False):
    # Main service function. Takes a raw source string and an optional flag 
    # to force re-ingestion even if the source already exists.

    normalized = normalize_source(source)
    # Fetch all sources currently stored in the vector DB, 
    # to check whether this source was already ingested.

    existing_sources = get_all_sources()
    # If the source already exists AND the caller did not explicitly 
    # request a forced re-ingestion, skip the ingestion process.

    if normalized in existing_sources and not force_update:
        return {
            "success": False,
            # Ingestion did not happen — signal failure/skip to the caller.
            "message": "Source already exists. Set force_update=true to update.",
            # Human-readable reason explaining why nothing was inserted.
            "inserted": 0,
            # No new chunks were inserted into the vector DB.
            "source": normalized
            # Return the normalized source so the caller/UI can display 
            # the exact value that was checked.
        }

    result = ingest_document(source)
    # Either the source is new, or force_update=True — proceed to actually 
    # ingest the document (chunk, embed, store in vector DB).
    # Note: passes the ORIGINAL `source`, not `normalized` — the ingestion 
    # pipeline likely needs the raw path/URL to actually read the file.

    return {
        "success": True,
        # Ingestion completed successfully.
        "message": "Document ingested successfully.",
        # Human-readable success message.
        "inserted": result["inserted"],
        # Number of chunks/records inserted, pulled from ingestion pipeline's result.
        "source": normalized
        # Return the normalized source for consistency with the DB record.
    }