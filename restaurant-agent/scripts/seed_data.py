"""
Seed script — inserts sample Menu, Table, and Reservation data so you have
something to test app/tools/ and app/agent/ against.

Run from the restaurant-agent/ root:
    python scripts/seed_data.py

Safe to re-run: it clears existing rows in these 3 tables first, then
re-inserts, so you won't get duplicates.
"""

from datetime import date, time, timedelta

from app.db.database import SessionLocal, engine, Base
from app.db.models import Menu, Table, Reservation, ReservationStatus


MENU_ITEMS = [
    # (name, category, price, description)
    ("Margherita Pizza", "Pizza", 8.99, "Classic tomato, mozzarella, basil"),
    ("Pepperoni Pizza", "Pizza", 10.49, "Tomato, mozzarella, pepperoni"),
    ("BBQ Chicken Pizza", "Pizza", 11.99, "BBQ sauce, chicken, red onion, mozzarella"),
    ("Veggie Supreme Pizza", "Pizza", 10.99, "Peppers, mushrooms, olives, onion, mozzarella"),
    ("Classic Cheeseburger", "Burgers", 7.99, "Beef patty, cheddar, lettuce, tomato"),
    ("Bacon BBQ Burger", "Burgers", 9.49, "Beef patty, bacon, BBQ sauce, onion rings"),
    ("Veggie Burger", "Burgers", 8.49, "Grilled veggie patty, lettuce, vegan mayo"),
    ("Chicken Burger", "Burgers", 8.99, "Grilled chicken breast, lettuce, garlic mayo"),
    ("French Fries", "Sides", 3.49, "Crispy salted fries"),
    ("Onion Rings", "Sides", 3.99, "Beer-battered onion rings"),
    ("Garlic Bread", "Sides", 4.49, "Toasted bread, garlic butter, herbs"),
    ("Caesar Salad", "Salads", 6.99, "Romaine, parmesan, croutons, caesar dressing"),
    ("Greek Salad", "Salads", 6.49, "Feta, olives, cucumber, tomato, red onion"),
    ("Chicken Tikka Masala", "Mains", 12.99, "Chicken in creamy spiced tomato sauce, served with rice"),
    ("Butter Chicken", "Mains", 12.49, "Chicken in mild buttery tomato sauce, served with rice"),
    ("Vegetable Biryani", "Mains", 10.99, "Spiced rice, mixed vegetables"),
    ("Kung Pao Chicken", "Mains", 11.49, "Chicken, peanuts, chili, vegetables"),
    ("Sweet & Sour Chicken", "Mains", 10.99, "Battered chicken, sweet and sour sauce"),
    ("Spaghetti Bolognese", "Mains", 10.49, "Beef ragu, spaghetti, parmesan"),
    ("Fettuccine Alfredo", "Mains", 10.99, "Creamy parmesan sauce, fettuccine"),
    ("Pad Thai", "Mains", 11.49, "Rice noodles, tofu or chicken, peanuts, lime"),
    ("Green Curry", "Mains", 11.99, "Thai green curry, chicken, jasmine rice"),
    ("Chocolate Brownie", "Desserts", 4.99, "Warm brownie, vanilla ice cream"),
    ("Cheesecake", "Desserts", 5.49, "New York style cheesecake"),
    ("Tiramisu", "Desserts", 5.99, "Coffee-soaked sponge, mascarpone"),
    ("Kids Chicken Nuggets", "Kids Menu", 5.49, "Chicken nuggets, fries"),
    ("Kids Mini Pizza", "Kids Menu", 5.49, "Cheese and tomato mini pizza"),
    ("Soft Drink", "Drinks", 2.49, "Coke, Sprite, or Fanta"),
    ("Fresh Orange Juice", "Drinks", 3.49, "Freshly squeezed orange juice"),
    ("Sparkling Water", "Drinks", 2.29, "500ml bottle"),
    ("House Red Wine (Glass)", "Drinks", 5.99, "125ml glass"),
    ("House White Wine (Glass)", "Drinks", 5.99, "125ml glass"),
]

TABLES = [
    # (table_number, capacity)
    (1, 2), (2, 2), (3, 2), (4, 2),
    (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
    (10, 6), (11, 6), (12, 6),
    (13, 8), (14, 8),
]


def seed():
    Base.metadata.create_all(bind=engine)  # creates tables if they don't exist yet
    db = SessionLocal()

    try:
        # Clear existing rows (children first, to respect the FK)
        db.query(Reservation).delete()
        db.query(Menu).delete()
        db.query(Table).delete()
        db.commit()

        # Menu
        db.add_all(
            Menu(name=name, category=category, price=price, description=desc, is_available=1)
            for name, category, price, desc in MENU_ITEMS
        )

        # Tables
        tables = [Table(table_number=num, capacity=cap) for num, cap in TABLES]
        db.add_all(tables)
        db.commit()  # commit so tables get real IDs before we reference them

        # A few sample reservations, spread over the next few days
        today = date.today()
        sample_reservations = [
            Reservation(
                customer_name="Ahmed Raza",
                phone="03001234567",
                reservation_date=today + timedelta(days=1),
                reservation_time=time(19, 0),
                party_size=2,
                table_id=tables[0].id,
                status=ReservationStatus.CONFIRMED,
            ),
            Reservation(
                customer_name="Sara Khan",
                phone="03007654321",
                reservation_date=today + timedelta(days=1),
                reservation_time=time(20, 30),
                party_size=4,
                table_id=tables[4].id,
                status=ReservationStatus.CONFIRMED,
            ),
            Reservation(
                customer_name="Bilal Ahmed",
                phone="03219876543",
                reservation_date=today + timedelta(days=2),
                reservation_time=time(13, 0),
                party_size=6,
                table_id=tables[9].id,
                status=ReservationStatus.PENDING,
            ),
        ]
        db.add_all(sample_reservations)
        db.commit()

        print(f"Seeded {len(MENU_ITEMS)} menu items, {len(TABLES)} tables, "
              f"{len(sample_reservations)} reservations.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()