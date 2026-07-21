"""
SQLAlchemy models for the restaurant agent.

Three tables:
    Menu         - menu items, prices, category
    Table        - physical restaurant tables and their capacity
    Reservation  - a booking, linked to a Table
"""

import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    Time,
    ForeignKey,
    Enum,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # e.g. Pizza, Burgers, Drinks
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String(500), nullable=True)
    is_available = Column(Integer, default=1, nullable=False)  # 1 = available, 0 = 86'd

    def __repr__(self):
        return f"<Menu id={self.id} name={self.name!r} category={self.category!r}>"


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, unique=True, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)

    reservations = relationship("Reservation", back_populates="table")

    def __repr__(self):
        return f"<Table id={self.id} number={self.table_number} capacity={self.capacity}>"


class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    reservation_date = Column(Date, nullable=False, index=True)
    reservation_time = Column(Time, nullable=False, index=True)
    party_size = Column(Integer, nullable=False)

    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    table = relationship("Table", back_populates="reservations")

    status = Column(
        Enum(ReservationStatus, name="reservation_status"),
        default=ReservationStatus.CONFIRMED,
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return (
            f"<Reservation id={self.id} customer={self.customer_name!r} "
            f"date={self.reservation_date} time={self.reservation_time} "
            f"table_id={self.table_id} status={self.status}>"
        )