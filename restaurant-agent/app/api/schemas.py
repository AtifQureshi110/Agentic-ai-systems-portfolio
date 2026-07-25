"""
Pydantic request/response models for app/api/.

Two groups:
1. Chat models (used by routes_chat.py) - talk to the LangGraph agent.
2. Reservation/Availability models (used by routes_reservation.py) - talk
   directly to app.tools.reservation_create / app.tools.availability_check,
   bypassing the agent, for a structured non-chat way to hit booking logic.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chat models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    reply: str
    thread_id: str
    # Optional debug info - current extracted slots / intent, useful while
    # testing the agent from Swagger UI or Streamlit dev mode.
    intent: Optional[str] = None
    slots: Optional[dict[str, Any]] = None
    missing_slots: Optional[list[str]] = None


# ---------------------------------------------------------------------------
# Direct reservation models (bypass the agent)
# ---------------------------------------------------------------------------

class ReservationRequest(BaseModel):
    customer_name: str
    phone: str
    date: str
    time: str
    party_size: int
    table_id: Optional[int] = None


class ReservationResponse(BaseModel):
    success: bool
    message: str


class AvailabilityRequest(BaseModel):
    date: str
    time: str
    party_size: int


class AvailabilityResponse(BaseModel):
    message: str