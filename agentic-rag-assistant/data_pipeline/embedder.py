import os, time, random, logging
from google import genai
from google.genai.errors import ServerError, ClientError
from dotenv import load_dotenv
from services.errors import QuotaExceededError, next_quota_reset_message

load_dotenv()
logger = logging.getLogger(__name__)
EMBED_MODEL = "models/gemini-embedding-001"
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def _embed_with_retry(chunk, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return client.models.embed_content(model=EMBED_MODEL, contents=chunk)

        except ClientError as e:
            if getattr(e, "status_code", None) == 429:
                reset_msg = next_quota_reset_message()
                raise QuotaExceededError(
                    f"You've used all your free messages for today. Try again after {reset_msg}."
                ) from e
            raise
	
        except ServerError as e:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"Embedding attempt {attempt+1} failed: {e}. Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)

    raise RuntimeError("Embedding failed after all retries")

def get_embeddings(chunks):
    vectors = []
    for idx, chunk in enumerate(chunks):
        result = _embed_with_retry(chunk)  # let QuotaExceededError bubble up
        vectors.append({
            "chunk_id": idx,
            "text": chunk,
            "embedding": result.embeddings[0].values
        })
    return vectors