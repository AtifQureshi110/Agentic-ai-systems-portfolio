from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


@lru_cache
def get_llm() -> ChatGoogleGenerativeAI:
    """
    Returns a single shared Gemini client, built once per process.
    agent/, tools/, and retrieval/ should all import `llm` from here
    rather than instantiating their own ChatGoogleGenerativeAI.
    """
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=settings.gemini_temperature,
        # transport="rest",
    )


# Shared instance — import directly: `from app.core.llm import llm`
llm = get_llm()