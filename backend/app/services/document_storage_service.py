"""
Power Electronics Reliability Copilot
Document Storage Service

Selects the active document storage provider.

v0.6.0 introduces provider-based storage so the application can switch between
local filesystem storage and Azure Blob Storage through configuration.
"""

from fastapi import UploadFile

from app.config import storage_config
from app.services.storage.azure_blob_storage_provider import AzureBlobStorageProvider
from app.services.storage.local_storage_provider import LocalStorageProvider


class DocumentStorageService:
    def __init__(self) -> None:
        self._local_provider = LocalStorageProvider()
        self._azure_provider = AzureBlobStorageProvider()

    def save_uploaded_file(self, file: UploadFile) -> dict:
        return self._get_provider().save_uploaded_file(file)

    def list_documents(self) -> list[dict]:
        return self._get_provider().list_documents()

    def _get_provider(self):
        provider = storage_config.storage_provider.lower().strip()

        if provider == "azure_blob":
            return self._azure_provider

        return self._local_provider


document_storage_service = DocumentStorageService()