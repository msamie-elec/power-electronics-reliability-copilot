"""
Power Electronics Reliability Copilot
Base Storage Provider
"""

from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile


class BaseStorageProvider(ABC):
    @abstractmethod
    def save_uploaded_file(self, file: UploadFile) -> dict[str, Any]:
        pass

    @abstractmethod
    def list_documents(self) -> list[dict[str, Any]]:
        pass