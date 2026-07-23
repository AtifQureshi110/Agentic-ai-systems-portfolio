"""
LangGraph StateGraph for the restaurant reservation agent.

This file only wires nodes and edges together.
Node logic lives in app/agent/nodes/.
"""

from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.agent.nodes.intent_router import classify_and_extract_node


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classify_and_extract", classify_and_extract_node)

    workflow.set_entry_point("classify_and_extract")
    workflow.add_edge("classify_and_extract", END)  # temporary, until more nodes exist

    return workflow.compile()