"""
Reservation tool — creates a table reservation by calling into
app/db/crud.py. Handles parsing plain date/time strings (as an LLM would
pass them) into the types crud.py expects.
"""

import logging
from datetime import datetime
from typing import Optional

from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.db.crud import create_reservation

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@tool
def reservation_create(
    customer_name: str,
    phone: str,
    date: str,
    time: str,
    party_size: int,
    table_id: Optional[int] = None,
) -> str:
    """
    Create a restaurant table reservation.

    Args:
        customer_name: Name of the customer booking the table.
        phone: Customer's contact phone number.
        date: Reservation date in YYYY-MM-DD format (e.g. "2026-08-01").
        time: Reservation time in 24-hour HH:MM format (e.g. "19:30").
        party_size: Number of guests.
        table_id: Optional specific table to book. If not given, the
            smallest available table that fits the party is chosen automatically.

    Returns:
        A confirmation message with the reservation details, or an error
        message explaining why the reservation could not be made.
    """
    logger.info(
        f"Reservation request: {customer_name}, {date} {time}, party of {party_size}"
    )

    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        parsed_time = datetime.strptime(time, "%H:%M").time()
    except ValueError:
        return (
            "Could not understand the date/time provided. "
            "Please use YYYY-MM-DD for date and HH:MM (24-hour) for time."
        )

    db = SessionLocal()
    try:
        reservation = create_reservation(
            db,
            customer_name=customer_name,
            phone=phone,
            date=parsed_date,
            time=parsed_time,
            party_size=party_size,
            table_id=table_id,
        )
        return (
            f"Reservation confirmed for {reservation.customer_name}, "
            f"party of {reservation.party_size}, on {reservation.reservation_date} "
            f"at {reservation.reservation_time} (table {reservation.table_id})."
        )
    except ValueError as e:
        return f"Could not create reservation: {e}"
    finally:
        db.close()


# ---------------------------------------------------------------------------
# TESTING — run this file directly to check everything works
# ---------------------------------------------------------------------------
# if __name__ == "__main__":
#     print("=== Live check: create a reservation ===")
#     print(reservation_create.invoke({
#         "customer_name": "Test User",
#         "phone": "555-1234",
#         "date": "2026-08-01",
#         "time": "19:30",
#         "party_size": 2,
#     }))