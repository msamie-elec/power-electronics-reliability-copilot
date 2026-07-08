"""
Power Electronics Reliability Copilot
File Service

Coordinates uploaded engineering document handling.

This service preserves the existing local processing workflow while delegating
physical file storage to the environment-aware Document Storage Service.

v0.6.0 introduces this separation so document storage can later switch between
local filesystem storage and Azure Blob Storage without changing API routes.
"""

from datetime import datetime
from typing import Any

from fastapi import UploadFile

from app.config import DOCUMENTS_DIR, UPLOAD_DIR
from app.services.chunk_service import create_chunks_from_text_file
from app.services.document_storage_service import document_storage_service
from app.services.parser_service import extract_text_from_pdf


UPLOAD_DIR.mkdir(exist_ok=True)


async def save_uploaded_file(file: UploadFile) -> dict[str, Any]:
    storage_metadata = await _save_file_to_storage(file)

    filename = storage_metadata["filename"]
    uploaded_at = storage_metadata.get("uploaded_at") or datetime.now().isoformat(
        timespec="seconds"
    )

    extracted_metadata = None
    chunk_metadata = None

    local_path = UPLOAD_DIR / filename

    if local_path.exists() and local_path.suffix.lower() == ".pdf":
        extracted_metadata = extract_text_from_pdf(local_path)
        chunk_metadata = create_chunks_from_text_file(
            DOCUMENTS_DIR / f"{local_path.stem}.txt",
            source_document=local_path.name,
        )

    return {
        "filename": filename,
        "content_type": file.content_type,
        "size_bytes": storage_metadata.get("size_bytes", 0),
        "uploaded_at": uploaded_at,
        "storage_backend": storage_metadata.get("storage_backend", "local"),
        "extracted_metadata": extracted_metadata,
        "chunk_metadata": chunk_metadata,
    }


def list_uploaded_documents() -> list[dict[str, Any]]:
    documents = []

    for document in document_storage_service.list_documents():
        filename = document.get("filename")

        if not filename or filename == ".gitkeep":
            continue

        documents.append(
            {
                "filename": filename,
                "size_bytes": document.get("size_bytes", 0),
                "uploaded_at": document.get("uploaded_at"),
                "storage_backend": document.get("storage_backend", "local"),
            }
        )

    return documents


async def _save_file_to_storage(file: UploadFile) -> dict[str, Any]:
    """
    Save the uploaded file through the active storage backend.

    The current document parsing and chunking pipeline still expects local files.
    When Azure Blob Storage is enabled later, a local processing copy may be
    added before extraction/chunking.
    """
    return document_storage_service.save_uploaded_file(file)