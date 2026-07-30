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

    if intent == "availability_check":
        required = ["reservation_date", "reservation_time", "party_size"]
        needed = [s for s in required if s in missing]
        if needed:
            return {**state, "tool_result": {"status": "missing_slots", "missing": needed}}

        result = availability_check.invoke({
            "date": slots["reservation_date"],
            "time": slots["reservation_time"],
            "party_size": slots["party_size"],
        })
        return {**state, "tool_result": result}

    if intent == "reservation_create":
            required = ["customer_name", "phone", "reservation_date", "reservation_time", "party_size"]
            needed = [s for s in required if s in missing]
            if needed:
                return {**state, "tool_result": {"status": "missing_slots", "missing": needed}}

            result = reservation_create.invoke({
                "customer_name": slots["customer_name"],
                "phone": slots["phone"],
                "date": slots["reservation_date"],
                "time": slots["reservation_time"],
                "party_size": slots["party_size"],
            })

            return {
                **state,
                "tool_result": result,
                "last_reservation": result,
                "slots": {},
                "missing_slots": ["customer_name", "phone", "reservation_date", "reservation_time", "party_size"],
            }