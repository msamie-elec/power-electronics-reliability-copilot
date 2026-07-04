"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.10 — Graph Retrieval Service
===========================================================================

Purpose:
    Provide read-only retrieval operations over the Neo4j Engineering
    Knowledge Graph.

This service is used by API endpoints now, and will later support Hybrid
GraphRAG and the Engineering Copilot.
"""

from typing import Any

from app.config import NEO4J_DATABASE
from app.services.neo4j_service import Neo4jService


class GraphRetrievalService:
    """Read-only graph retrieval service."""

    def __init__(self):
        self.neo4j = Neo4jService()

    def get_entity(self, name: str) -> dict[str, Any] | None:
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(
                """
                MATCH (e)
                WHERE toLower(e.canonicalName) = toLower($name)
                   OR toLower(e.name) = toLower($name)
                RETURN labels(e) AS labels,
                       properties(e) AS properties
                LIMIT 1
                """,
                name=name,
            )

            record = result.single()

            if not record:
                return None

            return {
                "labels": record["labels"],
                "properties": record["properties"],
            }

    def search_entities(self, search_text: str, limit: int = 10) -> list[dict[str, Any]]:
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(
                """
                MATCH (e)
                WHERE toLower(coalesce(e.canonicalName, "")) CONTAINS toLower($searchText)
                OR toLower(coalesce(e.name, "")) CONTAINS toLower($searchText)
                OR toLower(coalesce(e.description, "")) CONTAINS toLower($searchText)
                RETURN labels(e) AS labels,
                    properties(e) AS properties
                LIMIT $limit
                """,
                searchText=search_text,
                limit=limit,
            )

            return [
                {
                    "labels": record["labels"],
                    "properties": record["properties"],
                }
                for record in result
            ]

    def get_neighbors(self, name: str, limit: int = 25) -> list[dict[str, Any]]:
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(
                """
                MATCH (e)
                WHERE toLower(e.canonicalName) = toLower($name)
                   OR toLower(e.name) = toLower($name)
                MATCH (e)-[r]-(neighbor)
                RETURN
                    e.canonicalName AS source,
                    type(r) AS relationshipType,
                    startNode(r).canonicalName AS relationshipSource,
                    endNode(r).canonicalName AS relationshipTarget,
                    labels(neighbor) AS neighborLabels,
                    properties(neighbor) AS neighborProperties,
                    properties(r) AS relationshipProperties
                LIMIT $limit
                """,
                name=name,
                limit=limit,
            )

            return [
                {
                    "source": record["source"],
                    "relationshipType": record["relationshipType"],
                    "relationshipSource": record["relationshipSource"],
                    "relationshipTarget": record["relationshipTarget"],
                    "neighborLabels": record["neighborLabels"],
                    "neighborProperties": record["neighborProperties"],
                    "relationshipProperties": record["relationshipProperties"],
                }
                for record in result
            ]

    def get_relationships(
        self,
        source: str | None = None,
        relation: str | None = None,
        target: str | None = None,
        limit: int = 25,
    ) -> list[dict[str, Any]]:
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(
                """
                MATCH (source)-[r]->(target)
                WHERE ($source IS NULL OR toLower(source.canonicalName) = toLower($source))
                  AND ($target IS NULL OR toLower(target.canonicalName) = toLower($target))
                  AND ($relation IS NULL OR type(r) = $relation)
                RETURN
                    source.canonicalName AS source,
                    type(r) AS relationshipType,
                    target.canonicalName AS target,
                    properties(r) AS relationshipProperties
                LIMIT $limit
                """,
                source=source,
                relation=relation,
                target=target,
                limit=limit,
            )

            return [
                {
                    "source": record["source"],
                    "relationshipType": record["relationshipType"],
                    "target": record["target"],
                    "relationshipProperties": record["relationshipProperties"],
                }
                for record in result
            ]

    def get_entity_evidence(self, name: str) -> dict[str, Any] | None:
        entity = self.get_entity(name)

        if not entity:
            return None

        properties = entity["properties"]

        return {
            "canonicalName": properties.get("canonicalName"),
            "name": properties.get("name"),
            "sourceDocuments": properties.get("sourceDocuments", []),
            "evidenceChunkIds": properties.get("evidenceChunkIds", []),
        }

    def close(self):
        self.neo4j.close()


graph_retrieval_service = GraphRetrievalService()