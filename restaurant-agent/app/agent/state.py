"""
Agent state schema for the restaurant reservation LangGraph workflow.
"""

from typing import Optional, List, Literal, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


IntentType = Literal[
    "faq",
    "menu",
    "availability_check",
    "reservation_create",
    "unknown",
]

SlotName = Literal[
    "customer_name",
    "phone",
    "reservation_date",
    "reservation_time",
    "party_size",
]


class Slots(TypedDict, total=False):
    customer_name: Optional[str]
    phone: Optional[str]
    reservation_date: Optional[str]   # ISO format, e.g. "2026-07-25"
    reservation_time: Optional[str]   # ISO format, e.g. "19:30"
    party_size: Optional[int]


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    intent: Optional[IntentType]
    slots: Slots
    missing_slots: List[SlotName]
    tool_result: Optional[dict]
    response: Optional[str]