from fastapi import APIRouter

from backend.schemas.query import QueryRequest
from backend.services.query_service import ask_question

router = APIRouter( prefix="/query", tags=["Query"] )

# ==================================
# ASK QUESTION
# ==================================

@router.post("")
def query(request: QueryRequest):
    answer = ask_question(request.question )
    return { "answer": answer }