"""
POST /reserve
GET  /availability

These call app.tools.reservation_create and app.tools.availability_check
DIRECTLY (bypassing the LangGraph agent) - a structured, non-chat way to hit
the same booking logic. Useful for a future non-chat UI or direct API
testing.

Both tools return a plain string message (confirmed against the real
files), not a dict. So we just pass that string straight through as
`message`. We treat "could not" in the string as a failure signal, since
that's how both tools report errors.
"""

from fastapi import APIRouter, HTTPException

from app.tools.availability_tool import availability_check
from app.tools.reservation_tool import reservation_create
from app.api.schemas import (
    AvailabilityRequest,
    AvailabilityResponse,
    ReservationRequest,
    ReservationResponse,
)

router = APIRouter(tags=["reservation"])


@router.post("/reserve", response_model=ReservationResponse)
async def reserve(request: ReservationRequest) -> ReservationResponse:
    try:
        result = reservation_create.invoke(
            {
                "customer_name": request.customer_name,
                "phone": request.phone,
                "date": request.date,
                "time": request.time,
                "party_size": request.party_size,
                "table_id": request.table_id,
            }
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Reservation error: {exc}") from exc

    success = "could not" not in result.lower()
    return ReservationResponse(success=success, message=result)


@router.get("/availability", response_model=AvailabilityResponse)
async def availability(date: str, time: str, party_size: int) -> AvailabilityResponse:
    try:
        result = availability_check.invoke(
            {"date": date, "time": time, "party_size": party_size}
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Availability check error: {exc}") from exc

    return AvailabilityResponse(message=result)