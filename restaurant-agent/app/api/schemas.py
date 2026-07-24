"""
Pydantic request/response models for app/api/.

Kept separate from app/agent/state.py on purpose:
state.py is the internal LangGraph state (can change freely as the graph evolves),
these are the external HTTP contract (should change rarely, on purpose).
"""

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


# ---------- Chat (goes through the LangGraph agent) ----------

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's chat message")
    thread_id: str = Field(..., description="Conversation/session id, required so LangGraph memory persists")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="Final natural-language reply from response_node")
    thread_id: str
    # Optional debug info. Keep Optional so routes_chat.py can omit it
    # without breaking the response model.
    state: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional snapshot of slots/intent/etc. for debugging. Populate only if easy to grab from graph output.",
    )


# ---------- Direct REST endpoints (bypass the agent, call tools directly) ----------

class AvailabilityRequest(BaseModel):
    date: str = Field(..., description="Reservation date, e.g. 2026-07-24")
    time: str = Field(..., description="Reservation time, e.g. 19:30")
    party_size: int = Field(..., gt=0)


class AvailabilityResponse(BaseModel):
    available: bool
    details: Optional[Dict[str, Any]] = None


class ReservationRequest(BaseModel):
    customer_name: str
    phone: str
    date: str
    time: str
    party_size: int = Field(..., gt=0)
    table_id: Optional[int] = None


class ReservationResponse(BaseModel):
    success: bool
    reservation_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None
    message: Optional[str] = None