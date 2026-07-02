"""
Ingestion CLI — run this independently to add any URL, PDF, DOCX, or TXT
Usage:
    python -m maintenance.ingest --url "https://example.com"
    python -m maintenance.ingest --file "files/document.pdf"
    python -m maintenance.ingest --all
    python -m maintenance.ingest --file "files/document.pdf" --dry-run
"""

import argparse
import sys
from pathlib import Path
from data_pipeline.ingestion import ingest_document


# ----------------------------------------------------------------
# CENTRALIZED SOURCE REGISTRY
# ----------------------------------------------------------------
SOURCES = [
    # "files/RAG original paper by Meta.pdf",
    "files/project_overview.docx"
]


# ----------------------------------------------------------------
# CORE INGEST FUNCTION
# ----------------------------------------------------------------
def run_ingest(source: str, dry_run: bool = False):

    print(f"\n⏳ Processing: {source}")

    try:
        from data_pipeline.loader import load_document
        from data_pipeline.splitter import split_text

        doc = load_document(source)
        content = doc.get("content", "")
        chunks = split_text(content)

        print(f"📄 Content Length : {len(content)} chars")
        print(f"📦 Chunks         : {len(chunks)}")
        print(f"🔍 First Chunk Preview:\n{chunks[0][:300] if chunks else 'None'}")

        if dry_run:
            print(f"⚠️  DRY RUN — nothing sent to Pinecone")
            return

        result = ingest_document(source)
        print(f"✅ Done | Chunks: {len(result['chunks'])} | Upserted: {result['inserted']}")

    except Exception as e:
        print(f"❌ Failed: {source} | {e}")


# ----------------------------------------------------------------
# CLI
# ----------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser(
        description="Ingest documents into the RAG vector store"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url",  type=str,        help="Ingest a single URL")
    group.add_argument("--file", type=str,        help="Ingest a single local file")
    group.add_argument("--all",  action="store_true", help="Ingest all sources in SOURCES registry")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test loading and chunking without writing to Pinecone"
    )

    args = parser.parse_args()

    if args.url:
        run_ingest(args.url, dry_run=args.dry_run)

    elif args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"❌ File not found: {path}")
            print(f"   Make sure the path is correct relative to your project root")
            sys.exit(1)
        run_ingest(str(path), dry_run=args.dry_run)

    elif args.all:
        print(f"\n📦 Processing {len(SOURCES)} sources...\n")
        for source in SOURCES:
            run_ingest(source, dry_run=args.dry_run)
        print("\n✅ All sources processed.")


if __name__ == "__main__":
    main()