from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class RetrievedDoc(BaseModel):
    text: str
    source: Optional[str] = None
    score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class State(BaseModel):

    # ---------------- USER INPUT ----------------
    question: str

    # ---------------- ROUTING ----------------
    query_type: Optional[str] = None   # simple | complex

    # ---------------- PLANNING ----------------
    plan: Optional[str] = None

    # ---------------- RETRIEVAL ----------------
    retrieved_docs: Optional[List[Dict[str, Any]]] = None

    # ---------------- VERIFICATION ----------------
    is_verified: Optional[bool] = None
    verification_notes: Optional[str] = None

    # ---------------- FINAL OUTPUT ----------------
    answer: Optional[str] = None

    # ---------------- DEBUG / OBSERVABILITY ----------------
    trace: Optional[List[str]] = None
    confidence: Optional[float] = None