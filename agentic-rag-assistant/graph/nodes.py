from services.llm import generate_plan, generate_answer
from vectorstore.pinecone_client import query_vectors

# ---------------- CLASSIFIER ----------------
def classify(state):

    q = state.question.lower().strip()

    # strong signals (high confidence complex)
    strong_complex = [
        "compare", "difference between", "design", "architecture",
        "workflow", "multi-step", "step by step", "plan",
        "optimize", "evaluate", "tradeoff"
    ]

    # weak signals (only context-aware)
    weak_complex = ["how", "why"]

    # strong rules first
    if any(w in q for w in strong_complex):
        return {"query_type": "complex"}

    # weak signals only if long question
    if any(w in q for w in weak_complex) and len(q.split()) > 14:
        return {"query_type": "complex"}

    return {"query_type": "simple"}

from services.errors import QuotaExceededError

def retrieve(state):
    question = state.question

    expansion_map = {
        "teachers": "faculty instructors team",
        "teacher": "faculty instructor",
        "cost": "fee price tuition",
        "courses": "programs curriculum",
    }

    q_lower = question.lower()
    extra = [v for k, v in expansion_map.items() if k in q_lower]
    optimized_query = question + (" " + " ".join(extra) if extra else "")

    top_k = 6
    if state.query_type == "complex":
        top_k = 8
    if len(question.split()) > 18:
        top_k += 2
    top_k = min(top_k, 12)

    try:
        chunks = query_vectors(question=optimized_query, top_k=top_k)

    except QuotaExceededError as e:
        return {"retrieved_docs": [], "answer": str(e)}

    if not chunks:
        return {"retrieved_docs": []}

    filtered = [c for c in chunks if c.get("score", 0) > 0.2]
    if not filtered:
        filtered = chunks[:3]

    return {"retrieved_docs": filtered}

# ---------------- PLANNER ----------------
def planner_agent(state):
    plan = generate_plan(state.question)
    return { "plan": plan }

# ---------------- VERIFIER ----------------
def verify(state):

    docs = state.retrieved_docs or []

    if not docs:
        return { "is_verified": False, "verification_notes": "No retrieval results" }

    valid_docs = [
        d for d in docs
        if d.get("metadata", {}).get("text")
        and len(d["metadata"]["text"]) > 30
    ]

    if not valid_docs:
        return {
            "is_verified": False,
            "verification_notes": "Retrieved content too weak"
        }

    return {
        "is_verified": True,
        "verification_notes": "Valid context retrieved"
    }

# ---------------- ANSWER NODE ----------------
def answer_node(state):
    if state.answer:  # already set by retrieve() due to quota error
        return {"answer": state.answer}

    chunks = state.retrieved_docs or []
    if not chunks:
        return {"answer": "Not enough information found in documents."}

    plan = state.plan
    if state.query_type != "complex" or not plan:
        plan = None

    answer = generate_answer(question=state.question, chunks=chunks, plan=plan)
    return {"answer": answer}