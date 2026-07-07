"""
===========================================================================
Power Electronics Reliability Copilot
Document Registry Service
===========================================================================

Purpose
-------
Build frontend-ready document registry records for uploaded engineering
documents.

Version
-------
v0.5.2 — Professional Engineering Workspace

Responsibilities
----------------
- Build document registry records for uploaded engineering documents.
- Return stable document identifiers for the frontend.
- Preserve compatibility with the current evidence retrieval pipeline.
- Keep document registry logic separate from the API layer.

Notes
-----
This service provides a lightweight document registry for v0.5.2 while the
project transitions towards a fully persistent document registry in a later
release.
"""

import hashlib
from typing import Any

from app.services.file_service import list_uploaded_documents


# --------------------------------------------------------------------------
# Temporary pipeline-compatible document identifiers.
#
# These mappings preserve compatibility with the existing evidence retrieval
# pipeline until the persistent document registry is introduced.
# --------------------------------------------------------------------------

_PIPELINE_DOCUMENT_IDS = {
    "a_review_on_igbt_module_failure_modes_and_lifetime_testing.pdf":
        "DOC-B3198A5",
}


class DocumentRegistryService:
    """
    Builds frontend-ready document registry records.
    """

    def list_documents(self) -> list[dict[str, Any]]:
        """
        Return metadata describing all uploaded engineering documents.
        """
        documents: list[dict[str, Any]] = []

        for document in list_uploaded_documents():
            filename = document.get("filename", "")

            if not filename:
                continue

            documents.append(
                {
                    "documentId": self._build_document_id(filename),
                    "filename": filename,
                    "sizeBytes": document.get("size_bytes"),
                    "uploadedAt": document.get("uploaded_at"),
                    "source": "upload_registry",
                    "status": "available",
                }
            )

        return documents

    def _build_document_id(self, filename: str) -> str:
        """
        Return a pipeline-compatible document identifier.

        Known engineering documents retain their existing document IDs to
        preserve compatibility with the current evidence retrieval pipeline.
        All other uploaded documents receive a deterministic identifier based
        on their filename until the persistent document registry is available.
        """
        filename_key = filename.lower().strip()

        if filename_key in _PIPELINE_DOCUMENT_IDS:
            return _PIPELINE_DOCUMENT_IDS[filename_key]

        digest = hashlib.sha1(filename.encode("utf-8")).hexdigest()[:8].upper()
        return f"DOC-{digest}"


document_registry_service = DocumentRegistryService()