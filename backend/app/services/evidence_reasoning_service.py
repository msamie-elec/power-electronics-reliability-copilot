"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.11 — Evidence-backed AI Reasoning Service
===========================================================================

Purpose:
    Build structured reasoning context by combining semantic document evidence
    and Neo4j graph evidence.

This first version does not call the LLM. It prepares the evidence context
that will later be used by the Engineering Reasoning / Copilot answer engine.
"""

from typing import Any

from app.services.knowledge_retrieval_service import knowledge_retrieval_service
from app.services.graph_retrieval_service import graph_retrieval_service


class EvidenceReasoningService:
    """Builds evidence-backed reasoning context for engineering questions."""

    def build_reasoning_context(
        self,
        document_id: str,
        question: str,
        top_k: int = 5,
        graph_limit: int = 10,
    ) -> dict[str, Any]:
        """Build a combined document + graph reasoning context."""

        semantic_evidence = self._retrieve_semantic_evidence(
            document_id=document_id,
            question=question,
            top_k=top_k,
        )

        graph_evidence = self._retrieve_graph_evidence(
            question=question,
            limit=graph_limit,
        )

        return {
            "status": "success",
            "documentId": document_id,
            "question": question,
            "semanticEvidence": semantic_evidence,
            "graphEvidence": graph_evidence,
            "reasoningContext": {
                "semanticEvidenceCount": len(semantic_evidence),
                "graphEntityCount": len(graph_evidence["entities"]),
                "graphRelationshipCount": len(graph_evidence["relationships"]),
                "readyForLLM": True,
            },
        }

    def _retrieve_semantic_evidence(
        self,
        document_id: str,
        question: str,
        top_k: int,
    ) -> list[dict[str, Any]]:
        """Retrieve relevant chunks from the existing FAISS knowledge index."""

        retrieval_result = knowledge_retrieval_service.search(
            document_id=document_id,
            query=question,
            top_k=top_k,
        )

        return retrieval_result.get("results", [])

    def _retrieve_graph_evidence(
        self,
        question: str,
        limit: int,
    ) -> dict[str, Any]:
        """
        Retrieve graph evidence.

        First version:
        - search entities using the question text
        - retrieve relationships connected to the most relevant entities
        """

        entities = graph_retrieval_service.search_entities(
            search_text=question,
            limit=limit,
        )

        relationships = []

        for entity in entities:
            properties = entity.get("properties", {})
            canonical_name = properties.get("canonicalName") or properties.get("name")

            if not canonical_name:
                continue

            entity_relationships = graph_retrieval_service.get_relationships(
                source=canonical_name,
                limit=limit,
            )

            relationships.extend(entity_relationships)

        return {
            "entities": entities,
            "relationships": relationships[:limit],
        }


evidence_reasoning_service = EvidenceReasoningService()