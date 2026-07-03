"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.1 — Knowledge Document Pipeline
===========================================================================

File:
    knowledge_document_service.py

Purpose:
    Register approved engineering evidence PDF documents for the knowledge workflow.

Why this file exists:
    Trusted engineering documents must receive a unique identity and metadata
    before they can be chunked, embedded, analysed, and used to populate Neo4j.

Responsibilities:
    - Validate approved engineering PDFs
    - Ensure evidence documents come from backend/knowledge_base/
    - Parse PDFs using LlamaIndex
    - Extract basic metadata
    - Generate a unique document ID
    - Return a structured document registration record

This service DOES NOT:
    - Create chunks
    - Generate embeddings
    - Search FAISS or BM25
    - Extract entities
    - Populate Neo4j
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from llama_index.core import SimpleDirectoryReader


class KnowledgeDocumentService:
    """Service for registering approved engineering evidence PDF documents."""

    def register_document(self, file_path: str) -> dict[str, Any]:
        path = Path(file_path)

        expected_root = Path("knowledge_base")

        if expected_root not in path.parents:
            raise ValueError("Evidence documents must be stored inside 'knowledge_base'.")

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("Knowledge document pipeline currently supports PDF documents only.")

        documents = SimpleDirectoryReader(input_files=[str(path)]).load_data()
        text_pages = [doc.text for doc in documents if doc.text]

        document_id = f"DOC-{uuid4().hex[:8].upper()}"

        return {
            "documentId": document_id,
            "documentType": "evidence_document",
            "fileName": path.name,
            "filePath": str(path),
            "fileType": "pdf",
            "pageCount": len(documents),
            "characterCount": sum(len(text) for text in text_pages),
            "status": "registered",
            "registeredAt": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "parser": "LlamaIndex SimpleDirectoryReader",
                "source": "approved_evidence_pdf",
            },
        }


knowledge_document_service = KnowledgeDocumentService()