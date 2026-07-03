"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.4 — Knowledge FAISS Index Pipeline
===========================================================================

Purpose:
    Build a FAISS vector index from knowledge embeddings.

This service reads embedding JSON files produced by the Knowledge Embedding
Pipeline and creates a searchable FAISS index for semantic retrieval.

This service DOES NOT:
    - Generate embeddings
    - Perform BM25 retrieval
    - Call GPT
    - Populate Neo4j
"""

import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np


class KnowledgeFaissService:
    """Service for building FAISS indexes from knowledge embeddings."""

    def __init__(
        self,
        embedding_dir: str = "embeddings/knowledge",
        index_dir: str = "vector_store/knowledge",
    ) -> None:
        self.embedding_dir = Path(embedding_dir)
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def build_index(self, document_id: str) -> dict[str, Any]:
        embedding_file = self.embedding_dir / f"{document_id}.json"

        if not embedding_file.exists():
            raise FileNotFoundError(f"Embedding file not found: {embedding_file}")

        with embedding_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        embedding_records = data.get("embeddings", [])

        if not embedding_records:
            raise ValueError(f"No embeddings found for document: {document_id}")

        vectors = np.array(
            [record["embedding"] for record in embedding_records],
            dtype="float32",
        )

        dimension = vectors.shape[1]

        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)

        index_file = self.index_dir / f"{document_id}.index"
        mapping_file = self.index_dir / f"{document_id}_mapping.json"

        faiss.write_index(index, str(index_file))

        mapping = [
            {
                "vectorIndex": i,
                "chunkId": record["chunkId"],
                "documentId": record["documentId"],
                "chunkIndex": record["chunkIndex"],
            }
            for i, record in enumerate(embedding_records)
        ]

        with mapping_file.open("w", encoding="utf-8") as file:
            json.dump(mapping, file, indent=2, ensure_ascii=False)

        return {
            "status": "success",
            "documentId": document_id,
            "vectorsIndexed": int(index.ntotal),
            "dimension": dimension,
            "indexFile": str(index_file),
            "mappingFile": str(mapping_file),
        }


knowledge_faiss_service = KnowledgeFaissService()