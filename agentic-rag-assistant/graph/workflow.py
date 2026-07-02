from langgraph.graph import StateGraph, START, END
from graph.state import State
from graph.nodes import classify, retrieve, planner_agent, answer_node, verify
from graph.router import route_query

builder = StateGraph(state_schema=State)

# ---------- NODES ----------
builder.add_node("classifier", classify)
builder.add_node("retriever", retrieve)
builder.add_node("planner", planner_agent)
builder.add_node("verifier", verify)
builder.add_node("answer_generator", answer_node)

# ---------- ENTRY ----------
builder.add_edge(START, "classifier")

# ---------- ROUTING ----------
builder.add_conditional_edges(
    "classifier",
    route_query,
    {
        "simple": "retriever",
        "complex": "planner"
    }
)

# ---------- SIMPLE PATH ----------
builder.add_edge("retriever", "verifier")

# ---------- COMPLEX PATH ----------
builder.add_edge("planner", "retriever")   # planner influences retrieval
builder.add_edge("retriever", "verifier")

# ---------- FINAL ----------
builder.add_edge("verifier", "answer_generator")
builder.add_edge("answer_generator", END)

graph = builder.compile()