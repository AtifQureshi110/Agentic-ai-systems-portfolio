"""
POST /chat

Invokes the compiled LangGraph agent (app.agent.graph) with the user's
message and thread_id, and returns the conversational reply.

NOTE: confirm this against your real file before trusting it as-is - the
exact key names on AgentState (assumed here: "messages", "response",
"intent", "slots", "missing_slots"). Adjust the field lookups below if your
state.py uses different names.
"""

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

from app.agent.graph import build_graph
from app.api.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])

# build_graph() compiles the StateGraph once when this module loads.
# Reuse this single compiled graph for every request instead of rebuilding
# it on every call.
graph = build_graph()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    config = {"configurable": {"thread_id": request.thread_id}}

    try:
        result = graph.invoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Agent error: {exc}") from exc

    reply = result.get("response")
    if not reply:
        raise HTTPException(
            status_code=500,
            detail="Agent did not produce a response for this turn.",
        )

    return ChatResponse(
        reply=reply,
        thread_id=request.thread_id,
        intent=result.get("intent"),
        slots=result.get("slots"),
        missing_slots=result.get("missing_slots"),
        tool_result=result.get("tool_result"),  
    )