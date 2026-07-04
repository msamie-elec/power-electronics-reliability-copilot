"""
===========================================================================
Power Electronics Reliability Copilot
Engineering Reasoning Prompt
===========================================================================

Purpose
-------
Construct the prompt used by the Engineering Copilot to generate
evidence-backed engineering answers.
"""


def build_engineering_reasoning_prompt(
    question: str,
    semantic_evidence: list[dict],
    graph_evidence: dict,
) -> str:

    semantic_text = "\n\n".join(
        f"""
Evidence Chunk
--------------
Chunk ID: {item.get("chunkId")}
Similarity Score: {item.get("score")}

{item.get("text")}
"""
        for item in semantic_evidence
    )

    graph_entities = graph_evidence.get("entities", [])
    graph_relationships = graph_evidence.get("relationships", [])

    entity_text = "\n".join(
        f"- {entity.get('properties', {}).get('name')}"
        for entity in graph_entities
    )

    relationship_text = "\n".join(
        f"- {rel.get('source')} "
        f"--[{rel.get('relationshipType')}]--> "
        f"{rel.get('target')}"
        for rel in graph_relationships
    )

    return f"""
You are a senior Power Electronics Reliability Engineer.

Your responsibility is to analyse engineering evidence and produce
a technically accurate answer.

Rules

• Use ONLY the supplied evidence.
• Never invent engineering facts.
• If evidence is insufficient, explicitly state this.
• Distinguish observed evidence from engineering inference.
• Base conclusions on both semantic evidence and graph relationships.
• If multiple pieces of evidence support the same conclusion, combine them into a single engineering statement.
• Prefer evidence with stronger semantic relevance and explicit graph relationships.
• If semantic evidence and graph evidence appear inconsistent, explain the inconsistency rather than choosing one.
• When making engineering recommendations, clearly distinguish between observations, engineering judgement, and suggested actions.

Question

{question}

======================================================
Semantic Engineering Evidence
======================================================

{semantic_text}

======================================================
Knowledge Graph
======================================================

Entities

{entity_text}

Relationships

{relationship_text}

======================================================
Return your answer using EXACTLY this structure
======================================================

## Engineering Answer

...

## Supporting Evidence

...

## Knowledge Graph Reasoning

...

## Confidence

High / Medium / Low

## Recommended Next Step

...
"""