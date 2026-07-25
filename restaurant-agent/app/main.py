"""
FastAPI app instance for restaurant-agent.

Run from the project root (restaurant-agent/) with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_chat import router as chat_router
from app.api.routes_reservation import router as reservation_router

app = FastAPI(
    title="Restaurant Reservation Agent",
    description="Agentic AI assistant for restaurant info, menu, and reservations.",
    version="1.0.0",
)

# Allow the local Streamlit UI (default port 8501) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(reservation_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}