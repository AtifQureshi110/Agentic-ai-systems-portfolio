import re

def clean_text(text: str, source_type: str = "text") -> str:
    """
    Clean text for RAG ingestion.

    Goals:
    - Preserve semantic meaning
    - Normalize whitespace
    - Fix PDF extraction artifacts
    - Improve chunking quality
    """
    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove invisible chars
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)

    # Fix hyphenated line breaks from PDFs only
    if source_type == "pdf":
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
        # Merge wrapped lines ONLY for PDFs
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Preserve paragraph separation
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse repeated spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Remove repeated punctuation
    text = re.sub(r"([.!?]){3,}", r"\1", text)

    return text.strip()