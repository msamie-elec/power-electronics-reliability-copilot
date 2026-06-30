from datetime import datetime
from typing import Any

from pathlib import Path
from app.config import DOCUMENTS_DIR
from app.services.chunk_service import create_chunks_from_text_file
from fastapi import UploadFile
from app.services.parser_service import extract_text_from_pdf

from app.config import UPLOAD_DIR

UPLOAD_DIR.mkdir(exist_ok=True)


async def save_uploaded_file(file: UploadFile) -> dict[str, Any]:
    destination = UPLOAD_DIR / file.filename

    content = await file.read()
    destination.write_bytes(content)
    extracted_metadata = None

    chunk_metadata = None
    if destination.suffix.lower() == ".pdf":
        extracted_metadata = extract_text_from_pdf(destination)
        chunk_metadata = create_chunks_from_text_file(
            DOCUMENTS_DIR / f"{destination.stem}.txt",
            source_document=destination.name,
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
        "uploaded_at": datetime.now().isoformat(timespec="seconds"),
        "extracted_metadata": extracted_metadata,
        "chunk_metadata": chunk_metadata,
    }


def list_uploaded_documents() -> list[dict[str, Any]]:
    documents = []

    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.name != ".gitkeep":
            documents.append(
                {
                    "filename": path.name,
                    "size_bytes": path.stat().st_size,
                    "uploaded_at": datetime.fromtimestamp(
                        path.stat().st_mtime
                    ).isoformat(timespec="seconds"),
                }
            )

    return documents