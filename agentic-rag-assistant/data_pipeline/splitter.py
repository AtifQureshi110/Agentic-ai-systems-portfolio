import re
import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity


def split_text(text: str,chunk_size: int = 350,   # was 500
    overlap: int = 80 # was 50
) -> List[str]:

    if not text:
        return []

    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    chunks = []

    current_words = []

    for para in paragraphs:

        # Split paragraph into sentences
        sentences = re.split(r'(?<=[.!?])\s+',para)

        for sentence in sentences:

            sentence_words = sentence.split()

            # Large sentence
            while len(sentence_words) > chunk_size:

                chunks.append(" ".join(sentence_words[:chunk_size]))

                sentence_words = (sentence_words[chunk_size-overlap:])

            # Normal accumulation
            if (len(current_words) + len(sentence_words) > chunk_size ):

                chunks.append(" ".join(current_words))

                current_words = (current_words [ -overlap: ] )

            current_words.extend( sentence_words )

    if current_words:

        chunks.append( " ".join( current_words ) )

    return chunks

def split_into_sentences(text: str) -> List[str]:
    return re.split(r'(?<=[.!?])\s+', text)

def embed_sentences(sentences: List[str], embedder) -> List[List[float]]:
    result = embedder(sentences)
    return [r["embedding"] for r in result]

def cluster_sentences(sentences, embeddings, threshold=0.65):
    """
    Groups sentences based on semantic similarity
    """

    clusters = []
    current_cluster = [0]

    for i in range(1, len(sentences)):

        sim = cosine_similarity( [embeddings[i]], [embeddings[current_cluster[-1]]] )[0][0]

        if sim >= threshold:
            current_cluster.append(i)
        else:
            clusters.append(current_cluster)
            current_cluster = [i]

    if current_cluster:
        clusters.append(current_cluster)

    return clusters


def build_semantic_chunks(sentences, clusters):
    chunks = []

    for cluster in clusters:
        chunk = " ".join(sentences[i] for i in cluster)
        chunks.append(chunk)

    return chunks


def semantic_chunking(text: str, embedder) -> List[str]:

    sentences = split_into_sentences(text)

    if len(sentences) <= 2:
        return [text]

    embeddings = embed_sentences(sentences, embedder)

    clusters = cluster_sentences(sentences, embeddings, threshold=0.65)

    chunks = build_semantic_chunks(sentences, clusters)

    # ---------------- FIXED SAFE FALLBACK ----------------
    # DO NOT break semantic structure
    if len(chunks) == 0:
        return [text]

    if len(chunks) == 1 and len(sentences) > 6:
        # prevent over-compression
        mid = len(sentences) // 2
        return [
            " ".join(sentences[:mid]),
            " ".join(sentences[mid:])
        ]

    return chunks

