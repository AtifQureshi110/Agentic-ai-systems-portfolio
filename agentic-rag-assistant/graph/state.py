from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class State(BaseModel):

    # ---------------- USER INPUT ----------------
    question: str

    # ---------------- ROUTING ----------------
    query_type: Optional[str] = None   # simple | complex
    next_node: Optional[str] = None

    # ---------------- PLANNING ----------------
    plan: Optional[str] = None         # step-by-step plan for complex queries

    # ---------------- RETRIEVAL ----------------
    retrieved_docs: Optional[List[Dict[str, Any]]] = None

    # ---------------- VERIFICATION ----------------
    is_verified: Optional[bool] = None
    verification_notes: Optional[str] = None

    # ---------------- FINAL OUTPUT ----------------
    answer: Optional[str] = None