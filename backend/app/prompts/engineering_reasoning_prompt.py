from typing import Any


MAX_HISTORY_TURNS = 6
MAX_HISTORY_ANSWER_CHARS = 900


def _truncate(value: str | None, limit: int) -> str:
    if not value:
        return ""
    value = value.strip()
    if len(value) <= limit:
        return value
    return f"{value[:limit].rstrip()}..."


def _format_conversation_history(
    conversation_history: list[dict[str, Any]] | None,
) -> str:
    if not conversation_history:
        return "No previous conversation supplied."

    selected_history = conversation_history[-MAX_HISTORY_TURNS:]

    return "\n\n".join(
        "\n".join(
            [
                f"Turn {index}",
                f"Previous question: {_truncate(str(turn.get('question', '')), 500)}",
                f"Previous answer summary: {_truncate(str(turn.get('answer', '')), MAX_HISTORY_ANSWER_CHARS) or 'No previous answer text supplied.'}",
            ]
        )
        for index, turn in enumerate(selected_history, start=1)
    )


def build_engineering_reasoning_prompt(
    question: str,
    semantic_evidence: list[dict],
    graph_evidence: dict,
    conversation_history: list[dict[str, Any]] | None = None,
) -> str:

    semantic_text = "\n\n".join(
        f"""
Evidence Chunk
--------------
Document ID: {item.get("documentId")}
Chunk ID: {item.get("chunkId")}
Similarity Score: {item.get("score")}

{item.get("text")}
"""
        for item in semantic_evidence
    )

    graph_entities = graph_evidence.get("entities", [])
    graph_relationships = graph_evidence.get("relationships", [])

    entity_text = "\n".join(
        f"- {entity.get('properties', {}).get('name') or entity.get('name')}"
        for entity in graph_entities
    )

    relationship_text = "\n".join(
        f"- {rel.get('source')} "
        f"--[{rel.get('relationshipType')}]--> "
        f"{rel.get('target')}"
        for rel in graph_relationships
    )

    history_text = _format_conversation_history(conversation_history)

    return f"""
You are a senior Power Electronics Reliability Engineer.

Your responsibility is to analyse engineering evidence and produce
a technically accurate answer.

Rules

• Use the previous conversation only to understand context and follow-up intent.
• Use ONLY the supplied semantic evidence and Knowledge Graph evidence for engineering claims.
• Never invent engineering facts.
• Never invent values, test results, citations, or causal mechanisms.
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
Recent Conversation Context
======================================================

{history_text}

======================================================
Semantic Engineering Evidence
======================================================

{semantic_text or "No semantic engineering evidence supplied."}

======================================================
Knowledge Graph
======================================================

Entities

{entity_text or "No graph entities supplied."}

Relationships

{relationship_text or "No graph relationships supplied."}

======================================================
Return your answer using EXACTLY this structure
======================================================

## Summary

Provide a concise engineering summary in 2–4 sentences.

## Engineering Analysis

Explain the likely engineering interpretation based only on the supplied evidence.
Clearly distinguish observed evidence from engineering inference.

## Supporting Document Evidence

List the most relevant document evidence.
Mention document IDs and chunk IDs where useful.

## Supporting Graph Reasoning

Explain the relevant entities and relationships from the Knowledge Graph.
If graph evidence is weak or missing, state this clearly.

## Confidence

High / Medium / Low

Explain briefly why this confidence level was selected.

## Recommended Next Step

Provide one practical engineering next step.
Clearly state whether it is an inspection, test, analysis, or maintenance action.
"""