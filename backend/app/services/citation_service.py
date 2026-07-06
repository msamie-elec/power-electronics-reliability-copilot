"""
Power Electronics Reliability Copilot
Citation Service

Builds lightweight citation metadata from semantic and graph evidence.
"""

from typing import Any


class CitationService:
    def build_citations(
        self,
        semantic_evidence: list[dict[str, Any]],
        graph_evidence: dict[str, Any],
    ) -> list[dict[str, Any]]:
        citations: list[dict[str, Any]] = []

        citations.extend(self._build_semantic_citations(semantic_evidence))
        citations.extend(self._build_graph_citations(graph_evidence))

        return citations

    def _build_semantic_citations(
        self,
        semantic_evidence: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        citations: list[dict[str, Any]] = []

        for item in semantic_evidence:
            citations.append(
                {
                    "citationType": "document_chunk",
                    "source": item.get("documentId")
                    or item.get("sourceDocument")
                    or item.get("source_document"),
                    "chunkId": item.get("chunkId") or item.get("chunk_id"),
                    "score": item.get("score"),
                    "relationship": None,
                }
            )

        return citations

    def _build_graph_citations(
        self,
        graph_evidence: dict[str, Any],
    ) -> list[dict[str, Any]]:
        citations: list[dict[str, Any]] = []

        for relationship in graph_evidence.get("relationships", []):
            source = relationship.get("source")
            relationship_type = relationship.get("relationshipType")
            target = relationship.get("target")

            if not source or not relationship_type or not target:
                continue

            citations.append(
                {
                    "citationType": "graph_relationship",
                    "source": None,
                    "chunkId": None,
                    "score": None,
                    "relationship": f"{source} -[{relationship_type}]-> {target}",
                }
            )

        return citations


citation_service = CitationService()