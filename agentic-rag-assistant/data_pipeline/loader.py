import requests
from bs4 import BeautifulSoup
from pathlib import Path
from pypdf import PdfReader
from docx import Document
import logging
from data_pipeline.cleaner import clean_text


logger = logging.getLogger(__name__)

# ---------------- WEBSITE LOADER ----------------
def load_website(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n")
        return " ".join(text.split())

    except Exception as e:
        logger.error(f"Website loading failed: {e}")
        return ""


# ---------------- FILE LOADER ----------------
def load_document(path_or_url: str) -> dict:

    try:

        source = path_or_url
        file_type = "website"

        # WEBSITE
        if path_or_url.startswith("http"):

            raw_text = load_website(path_or_url)

        else:

            path = Path(path_or_url)

            file_type = path.suffix.lower().replace(".", "")

            if file_type == "pdf":

                reader = PdfReader(path)

                raw_text = "\n".join(
                    (page.extract_text() or "").strip()
                    for page in reader.pages
                )

            elif file_type == "docx":

                doc = Document(path)

                raw_text = "\n".join(
                    p.text.strip()
                    for p in doc.paragraphs
                    if p.text.strip()
                )

            elif file_type == "txt":

                raw_text = path.read_text(
                    encoding="utf-8"
                )

            else:
                raise ValueError(
                    f"Unsupported type: {file_type}"
                )

        # CLEAN
        cleaned_text = clean_text(raw_text)

        # RETURN STRUCTURED DATA
        return {
            "content": cleaned_text,
            "source": source,
            "type": file_type,
            "tokens": len(cleaned_text.split())
        }

    except Exception as e:

        logger.error(
            f"Document loading failed: {e}"
        )

        return {}