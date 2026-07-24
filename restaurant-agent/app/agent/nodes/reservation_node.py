"""
Reservation node - handles availability_check and reservation_create.

No LLM call here. No Pinecone call here.
Slots were already extracted earlier by intent_router (one LLM call there).
This node just checks missing_slots and, if nothing is missing, calls
ONE tool (availability_check or reservation_create) with the collected slots.
If something is missing, it does not call any tool - it just says what's missing,
so the response node can ask the user for it.
"""

from app.agent.state import AgentState
from app.tools.availability_tool import availability_check
from app.tools.reservation_tool import reservation_create


def reservation_node(state: AgentState) -> AgentState:
    intent = state["intent"]
    slots = state["slots"]
    missing = state["missing_slots"]

    # Availability check only needs date, time, party_size
    if intent == "availability_check":
        needed_for_check = [s for s in ["reservation_date", "reservation_time", "party_size"] if s in missing]
        if needed_for_check:
            return {**state, "tool_result": {"status": "missing_slots", "missing": needed_for_check}}

        result = availability_check.invoke({
            "date": slots["reservation_date"],
            "time": slots["reservation_time"],
            "party_size": slots["party_size"],
        })
        return {**state, "tool_result": result}

    # Reservation create needs all 5 slots
    if intent == "reservation_create":
        if missing:
            return {**state, "tool_result": {"status": "missing_slots", "missing": missing}}

        result = reservation_create.invoke({
            "customer_name": slots["customer_name"],
            "phone": slots["phone"],
            "date": slots["reservation_date"],
            "time": slots["reservation_time"],
            "party_size": slots["party_size"],
        })
        return {**state, "tool_result": result}

    return {**state, "tool_result": {"status": "error", "message": "Unsupported intent for this node."}}