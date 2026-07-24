"""
Response node - writes the final reply shown to the user.

Exactly ONE LLM call happens here - no more, no less.
No Pinecone call here at all.

This node only looks at tool_result (from rag_node or reservation_node).
It does not re-check slots or re-classify intent - that work is already
done by earlier nodes, so this node just turns the result into a
natural-sounding reply.
"""

from app.agent.state import AgentState
from app.agent.prompts.system_prompt import RESPONSE_SYSTEM_PROMPT
from app.core.llm import llm


def response_node(state: AgentState) -> AgentState:
    tool_result = state.get("tool_result")

    prompt = RESPONSE_SYSTEM_PROMPT.format(tool_result=tool_result)

    reply = llm.invoke(prompt).content  # single LLM call

    return {
        **state,
        "response": reply,
    }