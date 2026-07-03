"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.9 — Neo4j Population Service
===========================================================================

Purpose:
    Populate the Neo4j engineering knowledge graph from graph-ready JSON files
    produced by the Sprint 5.8 knowledge extraction pipeline.

Design:
    - Read extracted knowledge from backend/knowledge_graph/{document_id}.json
    - MERGE entity nodes using canonicalName
    - MERGE graph relationships using normalized relationship types
    - Preserve source document and evidence chunk IDs for traceability
"""

import json
import re
from pathlib import Path
from typing import Any

from app.config import NEO4J_DATABASE
from app.services.neo4j_service import Neo4jService


_RELATIONSHIP_TYPE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")


class Neo4jPopulationService:
    """Service for loading graph-ready extracted knowledge into Neo4j."""

    def __init__(self, knowledge_graph_dir: str = "knowledge_graph") -> None:
        self.knowledge_graph_dir = Path(knowledge_graph_dir)

    def populate_from_document(self, document_id: str) -> dict[str, Any]:
        """Populate Neo4j from one graph-ready JSON document."""

        graph_file = self.knowledge_graph_dir / f"{document_id}.json"

        if not graph_file.exists():
            raise FileNotFoundError(f"Knowledge graph JSON not found: {graph_file}")

        with graph_file.open("r", encoding="utf-8") as file:
            graph_data = json.load(file)

        return self.populate_from_data(graph_data=graph_data, source_file=str(graph_file))

    def populate_from_data(
        self,
        graph_data: dict[str, Any],
        source_file: str | None = None,
    ) -> dict[str, Any]:
        """Populate Neo4j from already-loaded graph-ready JSON data."""

        document_id = graph_data.get("documentId")
        entities = graph_data.get("entities", [])
        relationships = graph_data.get("relationships", [])

        if not document_id:
            raise ValueError("graph_data must include documentId")

        service = Neo4jService()

        try:
            with service.driver.session(database=NEO4J_DATABASE) as session:
                entity_results = [
                    session.execute_write(
                        self._merge_entity,
                        entity,
                        document_id,
                    )
                    for entity in entities
                ]

                relationship_results = []
                skipped_relationships = []

                for relationship in relationships:
                    relation_type = relationship.get("relation", "")

                    if not self._is_valid_relationship_type(relation_type):
                        skipped_relationships.append(
                            {
                                "relationship": relationship,
                                "reason": "Invalid relationship type",
                            }
                        )
                        continue

                    result = session.execute_write(
                        self._merge_relationship,
                        relationship,
                        document_id,
                    )
                    relationship_results.append(result)

            return {
                "status": "success",
                "documentId": document_id,
                "sourceFile": source_file,
                "entitiesRead": len(entities),
                "relationshipsRead": len(relationships),
                "entitiesMerged": len(entity_results),
                "relationshipsMerged": len(relationship_results),
                "relationshipsSkipped": len(skipped_relationships),
                "skippedRelationships": skipped_relationships,
            }

        finally:
            service.close()

    @staticmethod
    def _merge_entity(tx, entity: dict[str, Any], document_id: str) -> dict[str, Any]:
        canonical_name = entity.get("canonicalName") or entity.get("name")

        if not canonical_name:
            raise ValueError(f"Entity has no canonicalName or name: {entity}")

        result = tx.run(
            """
            MERGE (e:EngineeringEntity {canonicalName: $canonicalName})
            SET
                e.name = coalesce($name, e.name),
                e.type = coalesce($type, e.type),
                e.description = coalesce($description, e.description),
                e.aliases = $aliases,
                e.sourceDocuments = CASE
                    WHEN e.sourceDocuments IS NULL THEN [$documentId]
                    WHEN NOT $documentId IN e.sourceDocuments THEN e.sourceDocuments + $documentId
                    ELSE e.sourceDocuments
                END,
                e.evidenceChunkIds = $evidenceChunkIds,
                e.updatedAt = datetime()
            ON CREATE SET
                e.createdAt = datetime()
            RETURN e.canonicalName AS canonicalName
            """,
            canonicalName=canonical_name,
            name=entity.get("name"),
            type=entity.get("type", "Concept"),
            description=entity.get("description", ""),
            aliases=entity.get("aliases", []),
            evidenceChunkIds=entity.get("evidenceChunkIds", []),
            documentId=document_id,
        )

        record = result.single()
        return {"canonicalName": record["canonicalName"] if record else canonical_name}

    @staticmethod
    def _merge_relationship(
        tx,
        relationship: dict[str, Any],
        document_id: str,
    ) -> dict[str, Any]:
        source_canonical_name = relationship.get("sourceCanonicalName") or relationship.get("source")
        target_canonical_name = relationship.get("targetCanonicalName") or relationship.get("target")
        relation_type = relationship.get("relation")

        if not source_canonical_name or not target_canonical_name or not relation_type:
            raise ValueError(f"Relationship is incomplete: {relationship}")

        cypher = f"""
            MATCH (source:EngineeringEntity {{canonicalName: $sourceCanonicalName}})
            MATCH (target:EngineeringEntity {{canonicalName: $targetCanonicalName}})
            MERGE (source)-[r:{relation_type}]->(target)
            SET
                r.description = coalesce($description, r.description),
                r.evidenceChunkIds = $evidenceChunkIds,
                r.sourceDocuments = CASE
                    WHEN r.sourceDocuments IS NULL THEN [$documentId]
                    WHEN NOT $documentId IN r.sourceDocuments THEN r.sourceDocuments + $documentId
                    ELSE r.sourceDocuments
                END,
                r.updatedAt = datetime()
            ON CREATE SET
                r.createdAt = datetime()
            RETURN type(r) AS relationType
            """

        result = tx.run(
            cypher,
            sourceCanonicalName=source_canonical_name,
            targetCanonicalName=target_canonical_name,
            description=relationship.get("description", ""),
            evidenceChunkIds=relationship.get("evidenceChunkIds", []),
            documentId=document_id,
        )

        record = result.single()
        return {
            "sourceCanonicalName": source_canonical_name,
            "relation": record["relationType"] if record else relation_type,
            "targetCanonicalName": target_canonical_name,
        }

    @staticmethod
    def _is_valid_relationship_type(relation_type: str) -> bool:
        return bool(_RELATIONSHIP_TYPE_PATTERN.match(relation_type or ""))


neo4j_population_service = Neo4jPopulationService()
