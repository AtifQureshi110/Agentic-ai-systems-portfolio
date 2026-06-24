import re
from typing import List


def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
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
        sentences = re.split(
            r'(?<=[.!?])\s+',
            para
        )

        for sentence in sentences:

            sentence_words = sentence.split()

            # Large sentence
            while len(sentence_words) > chunk_size:

                chunks.append(
                    " ".join(
                        sentence_words[:chunk_size]
                    )
                )

                sentence_words = (
                    sentence_words[
                        chunk_size-overlap:
                    ]
                )

            # Normal accumulation
            if (
                len(current_words)
                +
                len(sentence_words)
                >
                chunk_size
            ):

                chunks.append(
                    " ".join(
                        current_words
                    )
                )

                current_words = (
                    current_words[
                        -overlap:
                    ]
                )

            current_words.extend(
                sentence_words
            )

    if current_words:

        chunks.append(
            " ".join(
                current_words
            )
        )

    return chunks