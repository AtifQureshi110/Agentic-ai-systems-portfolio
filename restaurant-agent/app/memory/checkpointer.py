"""
Gives the graph a 'memory'.

Without this, every message is treated as brand new — the agent
forgets slots, intent, everything, on the very next turn.

This file uses LangGraph's built-in SqliteSaver. It saves the full
AgentState after every node runs, keyed by a thread_id. Next
time the graph is called with the same thread_id, LangGraph loads
the saved state back in automatically — so past messages, slots,
and missing_slots are all still there.

Why SQLite and not SQL Server for this file:
LangGraph does not ship a SQL Server checkpointer. Writing one
by hand means matching LangGraph's internal save/load rules
manually — a lot of extra work for no real benefit at this stage.
SqliteSaver does the same job, needs zero setup, and is a normal,
accepted choice even in real production LangGraph apps. The main
data (menus, tables, reservations) stays in SQL Server exactly as
before — this file only handles conversation memory, and it can
be swapped later if needed.
"""

import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

# Where the memory file lives. It's separate from your main
# SQL Server database on purpose — this file only stores chat
# state, not restaurant data.
DB_PATH = Path(__file__).parent / "checkpoints.sqlite"


def get_checkpointer() -> SqliteSaver:
    """
    Creates (or opens) the sqlite file and wraps it as a
    LangGraph checkpointer.

    check_same_thread=False is needed because FastAPI can call
    this connection from different threads/requests.
    """
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    return SqliteSaver(conn)


# One shared instance for the whole app. Import this everywhere
# instead of calling get_checkpointer() again, so everyone uses
# the same open connection.
checkpointer = get_checkpointer()

