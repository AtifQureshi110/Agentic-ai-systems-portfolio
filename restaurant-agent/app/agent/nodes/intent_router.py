"""
Intent classification and slot extraction node.

Single LLM call that classifies intent AND extracts any slots
mentioned in the user's message, using trimmed history + known slots.
"""

import json
from datetime import date

from app.agent.state import AgentState, SlotName
# from app.agent.prompts import CLASSIFY_AND_EXTRACT_PROMPT
from app.agent.prompts.router_prompt import CLASSIFY_AND_EXTRACT_PROMPT
from app.core.llm import llm


ALL_SLOTS: list[SlotName] = [
    "customer_name",
    "phone",
    "reservation_date",
    "reservation_time",
    "party_size",
]


def _format_known_slots(slots: dict) -> str:
    known = {k: v for k, v in slots.items() if v is not None}
    return json.dumps(known) if known else "none"


def _format_missing_slots(missing: list) -> str:
    return ", ".join(missing) if missing else "none"


def _format_recent_history(messages: list, turns: int = 3) -> str:
    recent = messages[-turns * 2:]
    lines = []
    for m in recent:
        role = getattr(m, "type", "unknown")
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines) if lines else "none"


def classify_and_extract_node(state: AgentState) -> AgentState:
    user_message = state["messages"][-1].content

    prompt = CLASSIFY_AND_EXTRACT_PROMPT.format(
        current_date=date.today().isoformat(),
        known_slots=_format_known_slots(state.get("slots", {})),
        missing_slots=_format_missing_slots(state.get("missing_slots", [])),
        recent_history=_format_recent_history(state["messages"][:-1]),
        user_message=user_message,
    )

    raw_response = llm.invoke(prompt).content
    cleaned = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    parsed = json.loads(cleaned)

    new_slots = {**state.get("slots", {}), **{k: v for k, v in parsed["slots"].items() if v is not None}}
    missing = [s for s in ALL_SLOTS if new_slots.get(s) is None]

    return {
        **state,
        "intent": parsed["intent"],
        "slots": new_slots,
        "missing_slots": missing,
    }