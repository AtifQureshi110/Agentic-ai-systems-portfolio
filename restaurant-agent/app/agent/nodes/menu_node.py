"""
Menu node - handles menu questions (items, prices, categories).

Calls menu_lookup ONCE per query. No LLM call here - reply-writing
happens later in response_node.py.

menu_lookup only takes an optional "category" filter (e.g. "Pizza").
This node currently always passes category=None (full menu) - if you
later want category filtering, intent_router would need to extract a
"category" slot from the user's message and this node would pass it through.
"""

from app.agent.state import AgentState
from app.tools.menu_tool import menu_lookup


def menu_node(state: AgentState) -> AgentState:
    result = menu_lookup.invoke({"category": None})

    return {
        **state,
        "tool_result": result,
    }