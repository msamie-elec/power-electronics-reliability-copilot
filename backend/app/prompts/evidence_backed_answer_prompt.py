def build_evidence_backed_prompt(
    question: str,
    semantic_evidence: list[dict],
    graph_evidence: dict,
) -> str:
    semantic_text = "\n\n".join(
        f"Chunk: {item.get('chunkId')} | Score: {item.get('score')}\n{item.get('text')}"
        for item in semantic_evidence
    )

    graph_entities = graph_evidence.get("entities", [])
    graph_relationships = graph_evidence.get("relationships", [])

    graph_entity_text = "\n".join(
        f"- {entity.get('properties', {}).get('name')} "
        f"({', '.join(entity.get('labels', []))})"
        for entity in graph_entities
    )

    graph_relationship_text = "\n".join(
        f"- {rel.get('source')} -[{rel.get('relationshipType')}]-> {rel.get('target')}"
        for rel in graph_relationships
    )

    return f"""
You are a careful power electronics reliability engineering assistant.

Answer the user's engineering question using ONLY the evidence provided below.

If the evidence is insufficient, clearly say so.
Do not invent facts.
Separate document evidence from graph-based reasoning.

User Question:
{question}

Semantic Document Evidence:
{semantic_text}

Knowledge Graph Entities:
{graph_entity_text}

Knowledge Graph Relationships:
{graph_relationship_text}

Return the answer in this structure:

1. Engineering Answer
2. Supporting Document Evidence
3. Supporting Graph Reasoning
4. Confidence Level
5. Recommended Next Step
"""