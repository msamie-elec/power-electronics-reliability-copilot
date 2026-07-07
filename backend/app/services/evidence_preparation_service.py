"""
Power Electronics Reliability Copilot
Evidence Preparation Service

Ranks, deduplicates, normalises, and JSON-safes semantic and graph evidence
before it is sent to the Engineering Copilot LLM prompt or API response.
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

            deduplicated.append(self._make_json_safe(item))

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
            properties = self._make_json_safe(entity.get("properties", {}))

            name = (
                properties.get("canonicalName")
                or properties.get("name")
                or entity.get("name")
            )

            if not name:
                continue

            name = str(name)
            key = name.lower().strip()

            if key in seen_names:
                continue

            seen_names.add(key)

            deduplicated.append(
                {
                    "name": name,
                    "labels": self._make_json_safe(entity.get("labels", [])),
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

            source = str(source)
            relationship_type = str(relationship_type)
            target = str(target)

            key = f"{source.lower()}|{relationship_type}|{target.lower()}"

            if key in seen_relationships:
                continue

            seen_relationships.add(key)

            properties = (
                relationship.get("properties")
                or relationship.get("relationshipProperties", {})
            )

            deduplicated.append(
                {
                    "source": source,
                    "relationshipType": relationship_type,
                    "target": target,
                    "properties": self._make_json_safe(properties),
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

    @classmethod
    def _make_json_safe(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): cls._make_json_safe(item) for key, item in value.items()}

        if isinstance(value, list):
            return [cls._make_json_safe(item) for item in value]

        if isinstance(value, tuple):
            return [cls._make_json_safe(item) for item in value]

        if isinstance(value, set):
            return [cls._make_json_safe(item) for item in value]

        if hasattr(value, "iso_format"):
            return value.iso_format()

        if hasattr(value, "isoformat"):
            return value.isoformat()

        return value


evidence_preparation_service = EvidencePreparationService()