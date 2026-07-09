"""
==============================================================================
Power Electronics Reliability Copilot
Document ID Service

File
----
document_id_service.py

Purpose
-------
Provides deterministic document identifiers for uploaded engineering
documents.

Responsibilities
----------------
- Generate stable document identifiers.
- Ensure identical filenames always produce identical IDs.
- Support future migration to persistent document registry.

Security
--------
Contains no credentials or environment-specific information.

Version
-------
v0.6.1
==============================================================================
"""

import hashlib


class DocumentIdService:
    """Generate deterministic document identifiers."""

    @staticmethod
    def build_document_id(filename: str) -> str:
        digest = hashlib.sha1(
            filename.strip().lower().encode("utf-8")
        ).hexdigest()[:8].upper()

        return f"DOC-{digest}"


document_id_service = DocumentIdService()