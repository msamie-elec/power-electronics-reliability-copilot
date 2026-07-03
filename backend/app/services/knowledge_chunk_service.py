"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.2 — Knowledge Chunk Pipeline
===========================================================================

File:
    knowledge_chunk_service.py

Purpose:
    Create traceable chunks from approved engineering evidence documents.

Why this file exists:
    Evidence documents that are approved for the knowledge workflow must be
    converted into reusable chunks before they can be embedded, indexed,
    analysed by LLMs, or linked to Neo4j graph entities.

Responsibilities:
    - Load an approved evidence PDF
    - Split document text into chunks using LlamaIndex
    - Generate chunk identifiers
    - Preserve document metadata
    - Persist chunks as JSON for downstream processing

This service DOES NOT:
    - Generate embeddings
    - Perform BM25 retrieval
    - Search FAISS
    - Extract engineering entities
    - Populate Neo4j
"""

import json
from pathlib import Path
from typing import Any

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


class KnowledgeChunkService:
    """Service for chunking approved evidence documents."""

    def __init__(
        self,
        output_dir: str = "chunks/knowledge",
        chunk_size: int = 700,
        chunk_overlap: int = 100,
    ) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def create_chunks(
        self,
        document_id: str,
        file_path: str,
    ) -> dict[str, Any]:
        """
        Create chunks from an approved engineering PDF.

        Args:
            document_id: Registered document identifier.
            file_path: Path to the PDF file.

        Returns:
            Summary of generated chunks and output file.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("Knowledge chunking currently supports PDF documents only.")

        documents = SimpleDirectoryReader(input_files=[str(path)]).load_data()

        nodes = self.splitter.get_nodes_from_documents(documents)

        chunks: list[dict[str, Any]] = []

        for index, node in enumerate(nodes):
            text = node.get_content()

            chunk = {
                "chunkId": f"{document_id}-CHUNK-{index + 1:05d}",
                "documentId": document_id,
                "chunkIndex": index,
                "text": text,
                "characterCount": len(text),
                "wordCount": len(text.split()),
                "metadata": {
                    "sourceFile": path.name,
                    "sourcePath": str(path),
                    "workflow": "knowledge",
                    "splitter": "LlamaIndex SentenceSplitter",
                },
            }

            chunks.append(chunk)

        output_file = self.output_dir / f"{document_id}.json"

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(chunks, file, indent=2, ensure_ascii=False)

        return {
            "status": "success",
            "documentId": document_id,
            "chunksCreated": len(chunks),
            "outputFile": str(output_file),
        }


knowledge_chunk_service = KnowledgeChunkService()