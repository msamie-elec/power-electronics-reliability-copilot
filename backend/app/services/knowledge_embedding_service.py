"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.3 — Knowledge Embedding Pipeline
===========================================================================

File:
    knowledge_embedding_service.py

Purpose:
    Generate embeddings for approved knowledge chunks.

Why this file exists:
    Knowledge chunks must be converted into vector embeddings before they can
    be indexed in FAISS and used for semantic retrieval in the GraphRAG
    pipeline.

Responsibilities:
    - Load knowledge chunk JSON files
    - Generate embeddings for each chunk
    - Preserve chunk-to-document traceability
    - Save embeddings using documentId-based filenames

This service DOES NOT:
    - Create chunks
    - Search FAISS
    - Perform BM25 retrieval
    - Extract engineering entities
    - Populate Neo4j
"""

import json
from pathlib import Path
from typing import Any

from sentence_transformers import SentenceTransformer


class KnowledgeEmbeddingService:
    """Service for generating embeddings from approved knowledge chunks."""

    def __init__(
        self,
        chunk_dir: str = "chunks/knowledge",
        output_dir: str = "embeddings/knowledge",
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.chunk_dir = Path(chunk_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def create_embeddings(self, document_id: str) -> dict[str, Any]:
        """
        Generate embeddings for all chunks belonging to a document.

        Args:
            document_id: Registered document identifier.

        Returns:
            Summary of generated embeddings and output file path.
        """
        chunk_file = self.chunk_dir / f"{document_id}.json"

        if not chunk_file.exists():
            raise FileNotFoundError(f"Chunk file not found: {chunk_file}")

        with chunk_file.open("r", encoding="utf-8") as file:
            chunks = json.load(file)

        if not chunks:
            raise ValueError(f"No chunks found for document: {document_id}")

        texts = [chunk["text"] for chunk in chunks]
        vectors = self.model.encode(texts, convert_to_numpy=True)

        embedding_records = []

        for chunk, vector in zip(chunks, vectors):
            embedding_records.append(
                {
                    "chunkId": chunk["chunkId"],
                    "documentId": chunk["documentId"],
                    "chunkIndex": chunk["chunkIndex"],
                    "embedding": vector.tolist(),
                    "metadata": {
                        "model": self.model_name,
                        "sourceChunkFile": str(chunk_file),
                        "workflow": "knowledge",
                    },
                }
            )

        output_file = self.output_dir / f"{document_id}.json"

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(
                {
                    "documentId": document_id,
                    "embeddingModel": self.model_name,
                    "embeddingCount": len(embedding_records),
                    "embeddings": embedding_records,
                },
                file,
                indent=2,
                ensure_ascii=False,
            )

        return {
            "status": "success",
            "documentId": document_id,
            "embeddingModel": self.model_name,
            "embeddingsCreated": len(embedding_records),
            "outputFile": str(output_file),
        }


knowledge_embedding_service = KnowledgeEmbeddingService()