"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.8 — Knowledge Extraction Service
===========================================================================
"""

import json
from pathlib import Path
from typing import Any

from app.services.llm_service import extract_engineering_knowledge


class KnowledgeExtractionService:
    """Service for extracting and cleaning graph-ready knowledge from chunks."""

    def __init__(
        self,
        chunk_dir: str = "chunks/knowledge",
        output_dir: str = "knowledge_graph",
    ) -> None:
        self.chunk_dir = Path(chunk_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_knowledge(
        self,
        document_id: str,
        max_chunks: int | None = None,
    ) -> dict[str, Any]:
        chunk_file = self.chunk_dir / f"{document_id}.json"

        if not chunk_file.exists():
            raise FileNotFoundError(f"Chunk file not found: {chunk_file}")

        with chunk_file.open("r", encoding="utf-8") as file:
            chunks = json.load(file)

        if max_chunks is not None:
            chunks = chunks[:max_chunks]

        entities = []
        relationships = []
        failed_chunks = []

        for chunk in chunks:
            text = chunk.get("text", "")
            chunk_id = chunk.get("chunkId")

            try:
                extracted = extract_engineering_knowledge(text)

                for entity in extracted.get("entities", []):
                    entity["evidenceChunkId"] = chunk_id
                    entities.append(entity)

                for relationship in extracted.get("relationships", []):
                    relationship["evidenceChunkId"] = chunk_id
                    relationships.append(relationship)

            except Exception as ex:
                failed_chunks.append(
                    {
                        "chunkId": chunk_id,
                        "error": str(ex),
                    }
                )

        entities = self._deduplicate_entities(entities)
        relationships = self._deduplicate_relationships(relationships)

        output = {
            "documentId": document_id,
            "sourceChunkFile": str(chunk_file),
            "entityCount": len(entities),
            "relationshipCount": len(relationships),
            "entities": entities,
            "relationships": relationships,
            "failedChunks": failed_chunks,
            "metadata": {
                "workflow": "knowledge",
                "extractionMethod": "gpt-4.1-mini",
                "postProcessing": "entity_and_relationship_deduplication",
                "chunksProcessed": len(chunks),
                "failedChunks": len(failed_chunks),
            },
        }

        output_file = self.output_dir / f"{document_id}.json"

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(output, file, indent=2, ensure_ascii=False)

        return {
            "status": "success",
            "documentId": document_id,
            "chunksProcessed": len(chunks),
            "failedChunks": len(failed_chunks),
            "entitiesExtracted": len(entities),
            "relationshipsExtracted": len(relationships),
            "outputFile": str(output_file),
        }

    def _normalize_name(self, name: str) -> str:
        value = name.strip().lower()
        value = value.replace("-", " ")
        value = " ".join(value.split())

        aliases = {
            "igbt": "igbt module",
            "igbt modules": "igbt module",
            "failure modes": "failure mode",
            "failure mechanisms": "failure mechanism",
            "power cycling tests": "power cycling test",
            "power cycles": "power cycling",
            "thermal cycles": "thermal cycling",
            "bond wires": "bond wire",
            "al wires": "al wire",
            "al wire": "aluminum wire",
            "aluminum wires": "aluminum wire",
        }

        return aliases.get(value, value)

    def _canonical_display_name(self, normalized_name: str) -> str:
        acronyms = {
            "igbt": "IGBT",
            "mosfet": "MOSFET",
        }

        words = normalized_name.split()
        return " ".join(acronyms.get(word, word.capitalize()) for word in words)

    def _deduplicate_entities(
        self,
        entities: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        merged: dict[tuple[str, str], dict[str, Any]] = {}

        for entity in entities:
            raw_name = entity.get("name", "").strip()
            raw_type = entity.get("type", "Concept").strip() or "Concept"

            if not raw_name:
                continue

            canonical_key = self._normalize_name(raw_name)
            key = (canonical_key, raw_type.lower())

            if key not in merged:
                merged[key] = {
                    "name": self._canonical_display_name(canonical_key),
                    "canonicalName": canonical_key,
                    "type": raw_type,
                    "description": entity.get("description", ""),
                    "aliases": sorted({raw_name}),
                    "evidenceChunkIds": sorted({entity.get("evidenceChunkId")}),
                }
            else:
                merged[key]["aliases"] = sorted(
                    set(merged[key]["aliases"] + [raw_name])
                )

                if entity.get("evidenceChunkId"):
                    merged[key]["evidenceChunkIds"] = sorted(
                        set(
                            merged[key]["evidenceChunkIds"]
                            + [entity.get("evidenceChunkId")]
                        )
                    )

                if not merged[key].get("description") and entity.get("description"):
                    merged[key]["description"] = entity["description"]

        return list(merged.values())

    def _normalize_relation(self, relation: str) -> str:
        value = relation.strip().lower()
        value = value.replace("-", " ")
        value = " ".join(value.split())

        aliases = {
            "cause": "CAUSES",
            "causes": "CAUSES",
            "lead to": "LEADS_TO",
            "leads to": "LEADS_TO",
            "result in": "RESULTS_IN",
            "results in": "RESULTS_IN",
            "affect": "AFFECTS",
            "affects": "AFFECTS",
            "has": "HAS",
            "include": "INCLUDES",
            "includes": "INCLUDES",
            "part of": "PART_OF",
            "is part of": "PART_OF",
            "associated with": "ASSOCIATED_WITH",
            "is associated with": "ASSOCIATED_WITH",
        }

        return aliases.get(value, value.upper().replace(" ", "_"))

    def _deduplicate_relationships(
        self,
        relationships: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        merged: dict[tuple[str, str, str], dict[str, Any]] = {}

        for rel in relationships:
            source = rel.get("source", "").strip()
            target = rel.get("target", "").strip()
            relation = rel.get("relation", "").strip()

            if not source or not target or not relation:
                continue

            source_key = self._normalize_name(source)
            target_key = self._normalize_name(target)
            relation_type = self._normalize_relation(relation)

            key = (source_key, relation_type, target_key)

            if key not in merged:
                merged[key] = {
                    "source": self._canonical_display_name(source_key),
                    "sourceCanonicalName": source_key,
                    "relation": relation_type,
                    "target": self._canonical_display_name(target_key),
                    "targetCanonicalName": target_key,
                    "description": rel.get("description", ""),
                    "evidenceChunkIds": sorted({rel.get("evidenceChunkId")}),
                }
            else:
                if rel.get("evidenceChunkId"):
                    merged[key]["evidenceChunkIds"] = sorted(
                        set(
                            merged[key]["evidenceChunkIds"]
                            + [rel.get("evidenceChunkId")]
                        )
                    )

                if not merged[key].get("description") and rel.get("description"):
                    merged[key]["description"] = rel["description"]

        return list(merged.values())


knowledge_extraction_service = KnowledgeExtractionService()