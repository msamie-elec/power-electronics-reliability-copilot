import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import CHUNKS_DIR

CHUNKS_DIR.mkdir(exist_ok=True)

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def normalise_document_id(text_path: Path) -> str:
    name = text_path.stem.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    return name or "document"


def count_words(text: str) -> int:
    return len(text.split())


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start <= 0:
            start = end

    return chunks


def create_chunks_from_text_file(
    text_path: Path,
    source_document: str | None = None,
) -> dict[str, Any]:
    text = text_path.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    document_id = normalise_document_id(text_path)
    created_at = datetime.now().isoformat(timespec="seconds")

    chunk_records = []

    for index, chunk in enumerate(chunks, start=1):
        chunk_records.append(
            {
                "chunk_id": f"doc_{document_id}_chunk_{index:06d}",
                "source_document": source_document,
                "source_text_file": text_path.name,
                "chunk_index": index,
                "page_start": None,
                "page_end": None,
                "character_count": len(chunk),
                "word_count": count_words(chunk),
                "created_at": created_at,
                "text": chunk,
            }
        )

    output_path = CHUNKS_DIR / f"{text_path.stem}_chunks.json"

    payload = {
        "source_document": source_document,
        "source_text_file": text_path.name,
        "chunk_count": len(chunk_records),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "created_at": created_at,
        "chunks": chunk_records,
    }

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return payload