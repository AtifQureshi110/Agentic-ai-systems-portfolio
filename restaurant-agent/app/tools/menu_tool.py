"""
Menu tool — answers menu questions by querying SQL Server for current items,
optionally filtered by category.
"""

import logging
from typing import Optional

from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.db.crud import get_menu_items

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def format_menu_items(items) -> str:
    """Turn Menu rows into a clean string ready to hand back to the LLM/agent."""
    if not items:
        return "No menu items were found for this request."

    lines = []
    for item in items:
        line = f"{item.name} ({item.category}) - ${item.price}"
        if item.description:
            line += f": {item.description}"
        lines.append(line)

    return "\n".join(lines)


@tool
def menu_lookup(category: Optional[str] = None) -> str:
    """
    Look up current menu items, optionally filtered by category
    (e.g. "Pizza", "Burgers", "Drinks"). Only returns items currently available.

    Args:
        category: Optional menu category to filter by. Leave empty to get the full menu.

    Returns:
        A formatted list of matching menu items with name, category, price,
        and description, or a message saying nothing was found.
    """
    logger.info(f"Menu lookup: category={category}")

    db = SessionLocal()
    try:
        items = get_menu_items(db, category=category)
        return format_menu_items(items)
    finally:
        db.close()


# ---------------------------------------------------------------------------
# TESTING — run this file directly to check everything works
# ---------------------------------------------------------------------------
# if __name__ == "__main__":
#     print("=== Live check: full menu ===")
#     print(menu_lookup.invoke({}))
#     print()
#     print("=== Live check: filtered by category ===")
    print(menu_lookup.invoke({"category": "Pizza"}))