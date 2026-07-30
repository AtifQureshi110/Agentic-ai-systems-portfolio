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

# def response_node(state: AgentState) -> AgentState:
#     tool_result = state.get("tool_result")

#     user_message = state["messages"][-1].content

#     prompt = RESPONSE_SYSTEM_PROMPT.format(
#         tool_result=tool_result,
#         user_message=user_message,
#     )

#     reply = llm.invoke(prompt).content
#     if isinstance(reply, list):
#         reply = "".join(
#             part if isinstance(part, str) else part.get("text", "")
#             for part in reply
#         )
#     return {**state, "response": reply}


def response_node(state: AgentState) -> AgentState:
    tool_result = state.get("tool_result")
    user_message = state["messages"][-1].content
    last_reservation = state.get("last_reservation") or "None yet."

    prompt = RESPONSE_SYSTEM_PROMPT.format(
        tool_result=tool_result,
        user_message=user_message,
        last_reservation=last_reservation,
    )

    reply = llm.invoke(prompt).content
    if isinstance(reply, list):
        reply = "".join(
            part if isinstance(part, str) else part.get("text", "")
            for part in reply
        )
    return {**state, "response": reply}