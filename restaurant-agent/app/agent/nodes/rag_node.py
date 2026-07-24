"""
RAG node - handles FAQ/policy questions.

Calls faq_lookup ONCE per query (single Pinecone search).
No LLM call happens here - this node only fetches the raw result.
The response node (response_node.py) is the only place that turns
this result into a natural reply, using ONE LLM call.
"""

from app.agent.state import AgentState
from app.tools.faq_tool import faq_lookup


def rag_node(state: AgentState) -> AgentState:
    user_message = state["messages"][-1].content

    result = faq_lookup.invoke(user_message)  # single Pinecone call (via faq_lookup's embed + query)

    return {
        **state,
        "tool_result": result,
    }