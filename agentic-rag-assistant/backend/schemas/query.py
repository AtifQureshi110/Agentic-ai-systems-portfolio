from pydantic import BaseModel

# Validates the incoming request.
class QueryRequest(BaseModel):
    question: str