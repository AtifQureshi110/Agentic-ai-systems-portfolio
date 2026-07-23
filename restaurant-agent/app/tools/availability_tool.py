"""
Availability tool — checks which tables are free for a given date, time,
and party size by calling into app/db/crud.py.
"""

import logging
from datetime import datetime

from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.db.crud import check_availability

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def format_availability(tables) -> str:
    """Turn Table rows into a clean string ready to hand back to the LLM/agent."""
    if not tables:
        return "No tables are available for that date, time, and party size."

    lines = [f"Table {t.table_number} (seats {t.capacity})" for t in tables]
    return "Available tables:\n" + "\n".join(lines)


@tool
def availability_check(date: str, time: str, party_size: int) -> str:
    """
    Check which tables are available for a given date, time, and party size.

    Args:
        date: Date to check, in YYYY-MM-DD format (e.g. "2026-08-01").
        time: Time to check, in 24-hour HH:MM format (e.g. "19:30").
        party_size: Number of guests.

    Returns:
        A list of available tables with their seating capacity, or a message
        saying nothing is available for that slot.
    """
    logger.info(f"Availability check: {date} {time}, party of {party_size}")

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
        tables = check_availability(db, parsed_date, parsed_time, party_size)
        return format_availability(tables)
    finally:
        db.close()


# ---------------------------------------------------------------------------
# TESTING — run this file directly to check everything works
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Live check: availability ===")
    print(availability_check.invoke({
        "date": "2026-08-01",
        "time": "19:30",
        "party_size": 2,
    }))