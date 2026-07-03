"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.6 — Knowledge Retrieval Service
===========================================================================

Purpose:
    Provide reusable semantic retrieval over the local FAISS knowledge index.

This service centralises retrieval logic so it can be reused later by RAG,
GraphRAG, LlamaIndex integration, LangGraph agents and API endpoints.
"""

import json
from pathlib import Path
from typing import Any

import faiss
from sentence_transformers import SentenceTransformer


class KnowledgeRetrievalService:
    """Reusable semantic retrieval service for the knowledge workflow."""

    def __init__(
        self,
        index_dir: str = "vector_store/knowledge",
        chunk_dir: str = "chunks/knowledge",
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.index_dir = Path(index_dir)
        self.chunk_dir = Path(chunk_dir)
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def search(
        self,
        document_id: str,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        index_file = self.index_dir / f"{document_id}.index"
        mapping_file = self.index_dir / f"{document_id}_mapping.json"
        chunk_file = self.chunk_dir / f"{document_id}.json"

        if not index_file.exists():
            raise FileNotFoundError(f"FAISS index not found: {index_file}")

        if not mapping_file.exists():
            raise FileNotFoundError(f"FAISS mapping file not found: {mapping_file}")

        if not chunk_file.exists():
            raise FileNotFoundError(f"Chunk file not found: {chunk_file}")

        index = faiss.read_index(str(index_file))

        with mapping_file.open("r", encoding="utf-8") as file:
            mapping = json.load(file)

        with chunk_file.open("r", encoding="utf-8") as file:
            chunks = json.load(file)

        chunks_by_id = {chunk["chunkId"]: chunk for chunk in chunks}

        query_vector = self.model.encode(
            [query],
            convert_to_numpy=True,
        ).astype("float32")

        distances, indices = index.search(query_vector, top_k)

        results = []

        for distance, vector_index in zip(distances[0], indices[0]):
            if vector_index == -1:
                continue

            mapped = mapping[vector_index]
            chunk_id = mapped["chunkId"]
            chunk = chunks_by_id.get(chunk_id)

            if not chunk:
                continue

            results.append(
                {
                    "chunkId": chunk_id,
                    "documentId": document_id,
                    "chunkIndex": chunk["chunkIndex"],
                    "score": float(distance),
                    "text": chunk["text"],
                    "metadata": chunk.get("metadata", {}),
                }
            )

        return {
            "status": "success",
            "documentId": document_id,
            "query": query,
            "topK": top_k,
            "embeddingModel": self.model_name,
            "results": results,
        }


knowledge_retrieval_service = KnowledgeRetrievalService()