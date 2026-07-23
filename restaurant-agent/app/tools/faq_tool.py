"""
FAQ tool — answers natural-language questions by embedding the query and
retrieving the closest matching FAQ(s) from Pinecone.

Exposed as a LangChain/LangGraph-callable tool: `faq_lookup`.
"""

import logging

from langchain_core.tools import tool

from app.retrieval.embeddings import embed_text
from app.retrieval.pinecone_client import get_index

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

TOP_K = 3
SCORE_THRESHOLD = 0.75  # below this, we treat the match as "not confident enough"


def query_faq(question: str, top_k: int = TOP_K) -> list[dict]:
    """
    Embed `question` and query Pinecone for the closest matching FAQ(s).

    Returns a list of matches sorted by relevance, each shaped as:
        {"question": str, "answer": str, "score": float}
    """
    index = get_index()
    vector = embed_text(question)

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
    )

    matches = []
    for match in results.get("matches", []):
        metadata = match.get("metadata", {})
        matches.append({
            "question": metadata.get("question", ""),
            "answer": metadata.get("answer", ""),
            "score": match.get("score", 0.0),
        })

    return matches


def format_faq_response(matches: list[dict]) -> str:
    """Turn raw FAQ matches into a clean string ready to hand back to the LLM/agent."""
    if not matches or matches[0]["score"] < SCORE_THRESHOLD:
        return (
            "No confident FAQ match was found for this question. "
            "Let the user know this isn't covered in the FAQs and offer to help another way."
        )

    best = matches[0]
    return best["answer"]


@tool
def faq_lookup(question: str) -> str:
    """
    Answer a restaurant FAQ or policy question (e.g. opening hours, refund policy,
    parking, dress code, payment methods) by searching the FAQ knowledge base.

    Args:
        question: The user's natural-language question.

    Returns:
        The best-matching FAQ answer as plain text, or a message saying no
        confident match was found.
    """
    logger.info(f"FAQ lookup: {question}")
    matches = query_faq(question)
    return format_faq_response(matches)