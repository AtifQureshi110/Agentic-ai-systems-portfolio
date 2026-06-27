from dotenv import load_dotenv
from google import genai
import os 

load_dotenv()  # Load variables from .env
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY) 

def generate_answer(question, chunks):

    if not chunks:
        return "No relevant context found."

    top_chunks = chunks[:4]

    context = "\n\n".join(
        f"[Chunk {i+1}]\n{x['metadata']['text']}"
        for i, x in enumerate(top_chunks)
        if x.get("metadata", {}).get("text")
    )

    if not context.strip():
        return "No usable context found."

    prompt = f"""
You are a STRICT retrieval-based assistant.

RULES:
- Use ONLY context
- If answer not found: say "Not found in documents"
- Do NOT guess
- Be short

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()