"""
Power Electronics Reliability Copilot
Evidence Preparation Service

Ranks, deduplicates, and normalises semantic and graph evidence before it is
sent to the Engineering Copilot LLM prompt.
"""

from typing import Any


class EvidencePreparationService:
    def rank_and_deduplicate_semantic_evidence(
        self,
        semantic_evidence: list[dict[str, Any]],
        limit: int,
    ) -> list[dict[str, Any]]:
        seen_chunk_ids: set[str] = set()

        ranked_items = sorted(
            semantic_evidence,
            key=lambda item: item.get("score") or 0,
            reverse=True,
        )

        deduplicated: list[dict[str, Any]] = []

        for item in ranked_items:
            chunk_id = item.get("chunkId") or item.get("chunk_id")

            if chunk_id and chunk_id in seen_chunk_ids:
                continue

            if chunk_id:
                seen_chunk_ids.add(chunk_id)

            deduplicated.append(item)

            if len(deduplicated) >= limit:
                break

        return deduplicated

    def prepare_graph_evidence(
        self,
        graph_evidence: dict[str, Any],
        limit: int,
    ) -> dict[str, list[dict[str, Any]]]:
        entities = graph_evidence.get("entities", [])
        relationships = graph_evidence.get("relationships", [])

        return {
            "entities": self._deduplicate_entities(entities, limit),
            "relationships": self._deduplicate_relationships(relationships, limit),
        }

    def _deduplicate_entities(
        self,
        entities: list[dict[str, Any]],
        limit: int,
    ) -> list[dict[str, Any]]:
        seen_names: set[str] = set()
        deduplicated: list[dict[str, Any]] = []

        for entity in entities:
            properties = entity.get("properties", {})
            name = (
                properties.get("canonicalName")
                or properties.get("name")
                or entity.get("name")
            )

            if not name:
                continue

            key = name.lower().strip()

            if key in seen_names:
                continue

            seen_names.add(key)

            deduplicated.append(
                {
                    "name": name,
                    "labels": entity.get("labels", []),
                    "properties": properties,
                }
            )

            if len(deduplicated) >= limit:
                break

        return deduplicated

    def _deduplicate_relationships(
        self,
        relationships: list[dict[str, Any]],
        limit: int,
    ) -> list[dict[str, Any]]:
        seen_relationships: set[str] = set()
        deduplicated: list[dict[str, Any]] = []

        ranked_relationships = sorted(
            relationships,
            key=self._relationship_priority,
            reverse=True,
        )

        for relationship in ranked_relationships:
            source = relationship.get("source")
            relationship_type = relationship.get("relationshipType")
            target = relationship.get("target")

            if not source or not relationship_type or not target:
                continue

            key = f"{source.lower()}|{relationship_type}|{target.lower()}"

            if key in seen_relationships:
                continue

            seen_relationships.add(key)

            deduplicated.append(
                {
                    "source": source,
                    "relationshipType": relationship_type,
                    "target": target,
                    "properties": relationship.get("properties")
                    or relationship.get("relationshipProperties", {}),
                }
            )

            if len(deduplicated) >= limit:
                break

        return deduplicated

    @staticmethod
    def _relationship_priority(relationship: dict[str, Any]) -> int:
        priority = {
            "CAUSES": 10,
            "LEADS_TO": 9,
            "INDICATES": 8,
            "HAS_FAILURE_MODE": 8,
            "AFFECTS": 7,
            "TESTED_BY": 6,
            "MITIGATED_BY": 6,
            "PART_OF": 5,
            "RELATED_TO": 1,
        }

        return priority.get(relationship.get("relationshipType", ""), 0)


evidence_preparation_service = EvidencePreparationService()