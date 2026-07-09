"""
==============================================================================
Power Electronics Reliability Copilot
File Service

File
----
file_service.py

Purpose
-------
Coordinates uploaded engineering document handling.

This service delegates physical file storage to the environment-aware Document
Storage Service, then triggers local document processing for supported files.

Responsibilities
----------------
- Save uploaded files through the active storage provider.
- Assign deterministic document identifiers.
- Extract text from uploaded PDFs.
- Create legacy chunk metadata for frontend/backward compatibility.
- Create knowledge chunks, embeddings and FAISS indexes for Engineering Copilot.
- Return upload and processing metadata.

Security
--------
- Does not store secrets.
- Does not print API keys, storage keys, connection strings or credentials.
- Uses environment-based storage configuration.

Version
-------
v0.6.1
==============================================================================
"""

from datetime import datetime
import logging
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from app.config import DOCUMENTS_DIR, UPLOAD_DIR
from app.services.chunk_service import create_chunks_from_text_file
from app.services.document_id_service import document_id_service
from app.services.document_storage_service import document_storage_service
from app.services.knowledge_chunk_service import knowledge_chunk_service
from app.services.knowledge_embedding_service import knowledge_embedding_service
from app.services.knowledge_faiss_service import knowledge_faiss_service
from app.services.parser_service import extract_text_from_pdf


logger = logging.getLogger(__name__)

UPLOAD_DIR.mkdir(exist_ok=True)


async def save_uploaded_file(file: UploadFile) -> dict[str, Any]:
    storage_metadata = await _save_file_to_storage(file)

    filename = storage_metadata["filename"]
    document_id = document_id_service.build_document_id(filename)

    uploaded_at = storage_metadata.get("uploaded_at") or datetime.now().isoformat(
        timespec="seconds"
    )

    extracted_metadata = None
    chunk_metadata = None
    knowledge_chunk_metadata = None
    knowledge_embedding_metadata = None
    knowledge_index_metadata = None
    knowledge_pipeline_status = "not_applicable"
    knowledge_pipeline_error = None

    local_path = Path(
        storage_metadata.get("local_processing_path") or UPLOAD_DIR / filename
    )

    if local_path.exists() and local_path.suffix.lower() == ".pdf":
        try:
            logger.info(
                "Processing uploaded engineering document filename=%s document_id=%s",
                filename,
                document_id,
            )

            extracted_metadata = extract_text_from_pdf(local_path)

            chunk_metadata = create_chunks_from_text_file(
                DOCUMENTS_DIR / f"{local_path.stem}.txt",
                source_document=local_path.name,
            )

            knowledge_chunk_metadata = knowledge_chunk_service.create_chunks(
                document_id=document_id,
                file_path=str(local_path),
            )

            knowledge_embedding_metadata = knowledge_embedding_service.create_embeddings(
                document_id=document_id,
            )

            knowledge_index_metadata = knowledge_faiss_service.build_index(
                document_id=document_id,
            )

            knowledge_pipeline_status = "success"

        except Exception as exc:
            knowledge_pipeline_status = "failed"
            knowledge_pipeline_error = str(exc)

            logger.exception(
                "Knowledge indexing failed filename=%s document_id=%s",
                filename,
                document_id,
            )

    elif local_path.suffix.lower() == ".pdf":
        knowledge_pipeline_status = "failed"
        knowledge_pipeline_error = "Local processing copy was not found."

        logger.error(
            "Local processing copy missing filename=%s document_id=%s path=%s",
            filename,
            document_id,
            local_path,
        )

    return {
        "document_id": document_id,
        "filename": filename,
        "content_type": file.content_type,
        "size_bytes": storage_metadata.get("size_bytes", 0),
        "uploaded_at": uploaded_at,
        "storage_backend": storage_metadata.get("storage_backend", "local"),
        "local_processing_path": str(local_path),
        "extracted_metadata": extracted_metadata,
        "chunk_metadata": chunk_metadata,
        "knowledge_pipeline_status": knowledge_pipeline_status,
        "knowledge_pipeline_error": knowledge_pipeline_error,
        "knowledge_chunk_metadata": knowledge_chunk_metadata,
        "knowledge_embedding_metadata": knowledge_embedding_metadata,
        "knowledge_index_metadata": knowledge_index_metadata,
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
    """
    return document_storage_service.save_uploaded_file(file)