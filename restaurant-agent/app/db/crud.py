"""
CRUD functions for the restaurant agent.

These are the functions app/tools/ will import and wrap as LangChain/LangGraph
tools. Each function takes a SQLAlchemy Session as its first argument so the
caller controls the session lifecycle (e.g. via the get_db FastAPI dependency).
"""

from datetime import date as date_type, time as time_type
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models import Menu, Table, Reservation, ReservationStatus


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def get_menu_items(
    db: Session,
    category: Optional[str] = None,
    only_available: bool = True,
) -> List[Menu]:
    """
    Returns menu items, optionally filtered by category (e.g. "Pizza").
    By default only returns items currently marked available.
    """
    query = db.query(Menu)
    if only_available:
        query = query.filter(Menu.is_available == 1)
    if category:
        query = query.filter(Menu.category.ilike(category))
    return query.order_by(Menu.category, Menu.name).all()


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------

def get_table_by_id(db: Session, table_id: int) -> Optional[Table]:
    """Fetches a single table by its primary key."""
    return db.query(Table).filter(Table.id == table_id).first()


def get_all_tables(db: Session) -> List[Table]:
    """Returns every table in the restaurant."""
    return db.query(Table).order_by(Table.table_number).all()


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------

def check_availability(
    db: Session,
    date: date_type,
    time: time_type,
    party_size: int,
) -> List[Table]:
    """
    Returns the list of tables that can seat `party_size` and are NOT already
    booked for the given date/time. A table is considered booked if it has a
    reservation at that exact date+time with status PENDING or CONFIRMED.

    An empty list means nothing is available for that slot.
    """
    booked_table_ids = (
        db.query(Reservation.table_id)
        .filter(
            Reservation.reservation_date == date,
            Reservation.reservation_time == time,
            Reservation.status.in_(
                [ReservationStatus.PENDING, ReservationStatus.CONFIRMED]
            ),
        )
        .subquery()
    )

    available_tables = (
        db.query(Table)
        .filter(
            Table.capacity >= party_size,
            ~Table.id.in_(booked_table_ids),
        )
        .order_by(Table.capacity)
        .all()
    )
    return available_tables


# ---------------------------------------------------------------------------
# Reservations
# ---------------------------------------------------------------------------

def create_reservation(
    db: Session,
    customer_name: str,
    phone: str,
    date: date_type,
    time: time_type,
    party_size: int,
    table_id: Optional[int] = None,
) -> Reservation:
    """
    Creates a reservation.

    If `table_id` is not given, picks the smallest available table that fits
    `party_size` for the requested date/time. Raises ValueError if no table
    is available, or if the specified table_id is already booked for that
    slot.
    """
    if table_id is None:
        available = check_availability(db, date, time, party_size)
        if not available:
            raise ValueError(
                f"No table available for {party_size} guests on {date} at {time}."
            )
        chosen_table = available[0]
    else:
        chosen_table = get_table_by_id(db, table_id)
        if chosen_table is None:
            raise ValueError(f"Table {table_id} does not exist.")
        if chosen_table.capacity < party_size:
            raise ValueError(
                f"Table {table_id} only seats {chosen_table.capacity}, "
                f"but party size is {party_size}."
            )
        available_ids = {t.id for t in check_availability(db, date, time, party_size)}
        if chosen_table.id not in available_ids:
            raise ValueError(f"Table {table_id} is already booked for that slot.")

    reservation = Reservation(
        customer_name=customer_name,
        phone=phone,
        reservation_date=date,
        reservation_time=time,
        party_size=party_size,
        table_id=chosen_table.id,
        status=ReservationStatus.CONFIRMED,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


def cancel_reservation(db: Session, reservation_id: int) -> Optional[Reservation]:
    """Marks a reservation as CANCELLED. Returns None if it doesn't exist."""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation is None:
        return None
    reservation.status = ReservationStatus.CANCELLED
    db.commit()
    db.refresh(reservation)
    return reservation


def get_reservation_by_id(db: Session, reservation_id: int) -> Optional[Reservation]:
    """Fetches a single reservation by its primary key."""
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()