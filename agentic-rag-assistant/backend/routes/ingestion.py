from fastapi import APIRouter
from backend.schemas.ingestion import (IngestionRequest, IngestionResponse, SourceCheckRequest,)
from backend.services.ingestion_service import ingest_source
from data_pipeline.ingestion import normalize_source
from vectorstore.pinecone_client import get_all_sources

router = APIRouter( prefix="/ingest", tags=["Ingestion"] )

# -------------------------------
# Check existing document / URL
# -------------------------------
@router.post("/check-source")
def check_source(request: SourceCheckRequest):

    normalized = normalize_source(request.source)

    existing_sources = get_all_sources()

    print("Normalized:", normalized)
    print("Existing Sources:", existing_sources)

    if normalized in existing_sources:
        return { "exists": True, "message": "Source already exists. Do you want to update?" }

    return { "exists": False, "message": "New source detected" }

# -------------------------------
# Ingest document / URL
# -------------------------------

@router.post("", response_model=IngestionResponse )
def ingest(request: IngestionRequest):

    return ingest_source( source=request.source, force_update=request.force_update )