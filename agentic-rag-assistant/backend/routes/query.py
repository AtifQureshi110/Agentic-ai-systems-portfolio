from fastapi import APIRouter, HTTPException
from backend.schemas.query import QueryRequest
from backend.services.query_service import ask_question

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("")
def query(request: QueryRequest):
    try:
        answer = ask_question(request.question)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="Something went wrong while processing your question. Please try again in a moment."
        )