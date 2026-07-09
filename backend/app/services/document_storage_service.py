"""
==============================================================================
Power Electronics Reliability Copilot
Document Storage Service

File
----
document_storage_service.py

Purpose
-------
Selects the active document storage provider based on environment
configuration.

Responsibilities
----------------
- Route uploads to local storage or Azure Blob Storage.
- Route document listing to the active provider.
- Keep API and file-processing code independent of storage backend.

Security
--------
- Does not store secrets.
- Does not print credentials or connection strings.
- Uses environment-backed configuration.

Version
-------
v0.6.1
==============================================================================
"""

from typing import Any

from fastapi import UploadFile

from app.config import storage_config
from app.services.storage.azure_blob_storage_provider import AzureBlobStorageProvider
from app.services.storage.local_storage_provider import LocalStorageProvider


class DocumentStorageService:
    """
    Storage provider selector for uploaded engineering documents.
    """

    def __init__(self) -> None:
        self._local_provider = LocalStorageProvider()
        self._azure_provider = AzureBlobStorageProvider()

    def save_uploaded_file(self, file: UploadFile) -> dict[str, Any]:
        return self._get_provider().save_uploaded_file(file)

    def list_documents(self) -> list[dict[str, Any]]:
        return self._get_provider().list_documents()

    def _get_provider(self):
        provider = storage_config.storage_provider.lower().strip()

        if provider == "azure_blob":
            return self._azure_provider

        return self._local_provider


document_storage_service = DocumentStorageService()