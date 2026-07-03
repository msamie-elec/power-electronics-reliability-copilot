"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.7 — Knowledge Pipeline Orchestrator
===========================================================================

Purpose:
    Run the full approved knowledge ingestion pipeline in one operation.

Pipeline:
    Register document
        ↓
    Create chunks
        ↓
    Generate embeddings
        ↓
    Build FAISS index
"""

from typing import Any

from app.services.knowledge_document_service import knowledge_document_service
from app.services.knowledge_chunk_service import knowledge_chunk_service
from app.services.knowledge_embedding_service import knowledge_embedding_service
from app.services.knowledge_faiss_service import knowledge_faiss_service


class KnowledgePipelineService:
    """Orchestrates the complete knowledge ingestion pipeline."""

    def run_pipeline(self, file_path: str) -> dict[str, Any]:
        document_result = knowledge_document_service.register_document(
            file_path=file_path,
        )

        document_id = document_result["documentId"]

        chunk_result = knowledge_chunk_service.create_chunks(
            document_id=document_id,
            file_path=file_path,
        )

        embedding_result = knowledge_embedding_service.create_embeddings(
            document_id=document_id,
        )

        faiss_result = knowledge_faiss_service.build_index(
            document_id=document_id,
        )

        return {
            "status": "success",
            "documentId": document_id,
            "filePath": file_path,
            "document": document_result,
            "chunksCreated": chunk_result["chunksCreated"],
            "embeddingsCreated": embedding_result["embeddingsCreated"],
            "vectorsIndexed": faiss_result["vectorsIndexed"],
            "outputs": {
                "chunkFile": chunk_result["outputFile"],
                "embeddingFile": embedding_result["outputFile"],
                "faissIndexFile": faiss_result["indexFile"],
                "faissMappingFile": faiss_result["mappingFile"],
            },
        }


knowledge_pipeline_service = KnowledgePipelineService()