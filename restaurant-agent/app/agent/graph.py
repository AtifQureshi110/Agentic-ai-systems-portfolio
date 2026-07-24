"""
LangGraph StateGraph for the restaurant reservation agent.

This file only wires nodes and edges together - no logic lives here.
Node logic lives in app/agent/nodes/.

Routing after classify_and_extract:
- "faq"                  -> rag_node
- "menu"                 -> menu_node
- "reservation_create"   -> reservation_node
- "availability_check"   -> reservation_node
- "unknown"              -> response_node directly (no tool needed)

All paths end at response_node, which makes the single LLM call that
writes the final reply.
"""

from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.agent.nodes.intent_router import classify_and_extract_node
from app.agent.nodes.rag_node import rag_node
from app.agent.nodes.menu_node import menu_node
from app.agent.nodes.reservation_node import reservation_node
from app.agent.nodes.response_node import response_node
from app.memory.checkpointer import checkpointer


def route_after_classification(state: AgentState) -> str:
    intent = state.get("intent")

    if intent == "faq":
        return "rag_node"
    if intent == "menu":
        return "menu_node"
    if intent in ("reservation_create", "availability_check"):
        return "reservation_node"
    # "unknown" needs no tool - goes straight to response_node.
    return "response_node"


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classify_and_extract", classify_and_extract_node)
    workflow.add_node("rag_node", rag_node)
    workflow.add_node("menu_node", menu_node)
    workflow.add_node("reservation_node", reservation_node)
    workflow.add_node("response_node", response_node)

    workflow.set_entry_point("classify_and_extract")

    workflow.add_conditional_edges(
        "classify_and_extract",
        route_after_classification,
        {
            "rag_node": "rag_node",
            "menu_node": "menu_node",
            "reservation_node": "reservation_node",
            "response_node": "response_node",
        },
    )

    workflow.add_edge("rag_node", "response_node")
    workflow.add_edge("menu_node", "response_node")
    workflow.add_edge("reservation_node", "response_node")
    workflow.add_edge("response_node", END)

    return workflow.compile(checkpointer=checkpointer)