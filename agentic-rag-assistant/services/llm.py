from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

LLM_MODEL = "gemini-2.5-flash"


# ================================================================
#  PLANNER
#  Role: decide HOW to retrieve — never answers the question
#  Works for any domain, any document type
# ================================================================
def generate_plan(question: str) -> str:

    prompt = f"""
You are a Retrieval Planning Agent inside an Agentic RAG pipeline.

YOUR ONLY JOB:
Decide whether this question needs a structured retrieval plan,
and if so, produce one that helps the downstream retrieval and
answer generation steps do their job better.

You do NOT answer the question.
You do NOT invent or assume any information.
You think purely about: what needs to be retrieved, and in what order.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHEN TO SKIP PLANNING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If the question is simple, factual, or single-hop — return EXACTLY:

No plan needed

Examples that need NO plan:
- "Who is the CEO?"
- "What is the price?"
- "When was it founded?"
- "What does X stand for?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHEN TO PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate a plan ONLY when the question requires:
- Comparing two or more things
- Multi-hop reasoning (A relates to B relates to C)
- Summarizing across multiple sections
- Extracting and aggregating a list
- Understanding a system, architecture, or workflow
- Analyzing relationships between entities

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLAN FORMAT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Maximum 4 steps
- Each step must be a specific retrieval or synthesis action
- Write in plain natural language
- No numbering required
- No generic steps like "analyze carefully" or "think deeply"
- No markdown, no headers, no explanation

Good plan examples:

Question: Compare Plan A vs Plan B
→ Retrieve description and features of Plan A.
   Retrieve description and features of Plan B.
   Extract key differences across audience, tools, and structure.
   Prepare a grounded side-by-side comparison.

Question: Explain the system architecture
→ Retrieve architecture overview sections.
   Collect component-level implementation details.
   Identify how components connect and interact.
   Merge into a structured layered explanation.

Question: List all available certifications
→ Retrieve all certification-related sections.
   Extract certification names, levels, and requirements.
   Consolidate into a clean list.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUESTION:
{question}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Return ONLY the plan text or "No plan needed". Nothing else.
"""

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
        config={
            "temperature": 0.05,
            "max_output_tokens": 200
        }
    )

    return response.text.strip()


# ================================================================
#  ANSWER GENERATOR
#  Role: produce a grounded, human-toned answer from retrieved chunks
#  Generic — works for any domain or document type
# ================================================================
def generate_answer(question: str, chunks: list, plan: str = None) -> str:

    if not chunks:
        return "I wasn't able to find any relevant information to answer that. Try rephrasing your question."

    top_chunks = chunks[:5]

    context = "\n\n".join(
        f"[Source {i+1}]\n{x.get('metadata', {}).get('text', '').strip()}"
        for i, x in enumerate(top_chunks)
        if x.get('metadata', {}).get('text', '').strip()
    )

    if not context.strip():
        return "I found some results but couldn't extract usable content from them. Try asking in a different way."

    # Only inject plan if it's meaningful
    plan_section = ""
    if plan and plan.strip() and plan.strip().lower() != "no plan needed":
        plan_section = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RETRIEVAL PLAN (follow this structure when forming your answer)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{plan.strip()}
"""

    prompt = f"""
You are a knowledgeable and helpful AI assistant.

Your job is to answer the user's question using ONLY the information
provided in the context below — nothing else.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW TO BEHAVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Respond like a knowledgeable human assistant — not like a machine
reading from a database. Be warm, clear, and direct.

- Talk TO the user, not at them ("you can", "you'll find", "this covers")
- Lead with the most useful information first
- Use bullet points only when listing multiple distinct items
- For comparisons, use a clear structured format
- For explanations, build logically from simple to complex
- Keep it concise — don't pad with unnecessary words
- Never start your answer with "Based on the context" or "According to the documents"
  — just answer naturally as if you already know this

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Use ONLY what is in the context — no external knowledge, no guessing
- If the answer is genuinely not in the context, respond with:
  "I don't have that information in the documents I have access to.
   You might want to check the official source directly."
- Do NOT hallucinate names, numbers, dates, or facts
- Do NOT repeat the same point twice
- Do NOT mention "chunks", "context", "documents", or "retrieval" in your answer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{context}
{plan_section}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER QUESTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{question}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR ANSWER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
        config={"temperature": 0.3}
    )

    return response.text.strip()