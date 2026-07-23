from pydantic import BaseModel

# Used for checking existing source
class SourceCheckRequest(BaseModel):
    source: str

# Used for actual ingestion
class IngestionRequest(BaseModel):
    source: str
    force_update: bool = False

# Response after ingestion
class IngestionResponse(BaseModel):
    success: bool
    message: str
    inserted: int
    source: str

