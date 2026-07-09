"""
==============================================================================
Power Electronics Reliability Copilot
Document Registry Service

File
----
document_registry_service.py

Purpose
-------
Builds frontend-ready document registry records for uploaded engineering
documents.

Responsibilities
----------------
- List uploaded engineering documents.
- Attach stable document identifiers.
- Keep document registry formatting separate from the API layer.

Security
--------
- Does not store secrets.
- Does not print credentials, keys, or connection strings.
- Uses Document ID Service for deterministic document identifiers.

Version
-------
v0.6.1
==============================================================================
"""

from typing import Any

from app.services.document_id_service import document_id_service
from app.services.file_service import list_uploaded_documents


class DocumentRegistryService:
    """
    Builds frontend-ready document registry records.
    """

    def list_documents(self) -> list[dict[str, Any]]:
        """
        Return metadata describing uploaded engineering documents.
        """
        documents: list[dict[str, Any]] = []

        for document in list_uploaded_documents():
            filename = document.get("filename", "")

            if not filename:
                continue

            documents.append(
                {
                    "documentId": document_id_service.build_document_id(filename),
                    "filename": filename,
                    "sizeBytes": document.get("size_bytes"),
                    "uploadedAt": document.get("uploaded_at"),
                    "source": "upload_registry",
                    "status": "available",
                }
            )

        return documents


document_registry_service = DocumentRegistryService()