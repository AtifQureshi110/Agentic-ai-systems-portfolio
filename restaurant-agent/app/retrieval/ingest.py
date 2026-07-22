"""
Loads restaurant_faq.txt.txt, splits it into one chunk per Q&A pair,
embeds the QUESTION only (for accurate query matching), and upserts
into Pinecone with stable IDs (safe to re-run after edits).

Run directly: python -m app.retrieval.ingest
"""

import hashlib
import logging
import re
import time
from pathlib import Path

from app.retrieval.pinecone_client import get_index
from app.retrieval.embeddings import embed_batch

FAQ_FILE = Path("app/data/restaurant_faq.txt")
BATCH_SIZE = 20
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_qa_pairs(file_path: Path) -> list[dict]:
    """Split the FAQ file into (question, answer) pairs."""
    text = file_path.read_text(encoding="utf-8")
    raw_chunks = re.split(r"\n(?=Q:)", text)

    pairs = []
    for chunk in raw_chunks:
        chunk = chunk.strip()
        if not chunk.startswith("Q:"):
            continue
        match = re.match(r"Q:\s*(.+?)\nA:\s*(.+)", chunk, re.DOTALL)
        if match:
            question = match.group(1).strip()
            answer = match.group(2).strip()
            pairs.append({"question": question, "answer": answer})
        else:
            logger.warning(f"Skipped malformed chunk: {chunk[:50]}...")

    return pairs


def stable_id(question: str) -> str:
    """Hash the question into a stable ID — same question always maps to the same ID,
    so re-running ingest after edits updates instead of duplicating."""
    return "faq-" + hashlib.sha256(question.encode("utf-8")).hexdigest()[:16]


def build_records(pairs: list[dict]) -> list[dict]:
    records = []
    for pair in pairs:
        records.append({
            "id": stable_id(pair["question"]),
            "question": pair["question"],
            "answer": pair["answer"],
        })
    return records


def upsert_with_retry(index, vectors: list[dict], attempt: int = 1):
    try:
        index.upsert(vectors=vectors)
    except Exception as e:
        if attempt >= MAX_RETRIES:
            logger.error(f"Upsert failed after {MAX_RETRIES} attempts: {e}")
            raise
        wait = 2 ** attempt
        logger.warning(f"Upsert failed (attempt {attempt}), retrying in {wait}s: {e}")
        time.sleep(wait)
        upsert_with_retry(index, vectors, attempt + 1)


def upsert_records(records: list[dict], batch_size: int = BATCH_SIZE):
    index = get_index()
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]

        # Embed the QUESTION only — matches how users actually query
        questions = [r["question"] for r in batch]
        vectors = embed_batch(questions)

        to_upsert = [
            {
                "id": r["id"],
                "values": vec,
                "metadata": {
                    "question": r["question"],
                    "answer": r["answer"],
                },
            }
            for r, vec in zip(batch, vectors)
        ]
        upsert_with_retry(index, to_upsert)
        logger.info(f"Upserted batch {i // batch_size + 1} ({len(to_upsert)} records)")


if __name__ == "__main__":
    confirm = input(f"This will upsert into Pinecone index. Continue? (y/n): ")
    if confirm.lower() != "y":
        logger.info("Ingestion cancelled.")
        exit()
    logger.info("Loading FAQ file...")
    pairs = load_qa_pairs(FAQ_FILE)
    logger.info(f"Found {len(pairs)} Q&A pairs")

    records = build_records(pairs)
    upsert_records(records)

    logger.info("Ingestion complete.")