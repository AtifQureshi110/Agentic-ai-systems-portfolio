import os
import logging

from google import genai
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)

EMBED_MODEL = "models/gemini-embedding-001"

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def get_embeddings(chunks):

    vectors = []

    for idx, chunk in enumerate(chunks):

        try:

            result = client.models.embed_content(
                model=EMBED_MODEL,
                contents=chunk
            )

            vectors.append({
                "chunk_id": idx,
                "text": chunk,
                "embedding": result.embeddings[0].values
            })

        except Exception as e:

            logger.error(
                f"Embedding failed for chunk {idx}: {e}"
            )

    return vectors