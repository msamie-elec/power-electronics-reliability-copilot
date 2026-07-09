"""
==============================================================================
Power Electronics Reliability Copilot
LLM Service

File
----
llm_service.py

Purpose
-------
Provides language-model operations used throughout the project.

Responsibilities
----------------
- Generate RAG answers.
- Extract engineering knowledge.
- Generate evidence-backed engineering answers.
- Keep prompt construction separate from provider-specific AI calls.

Security
--------
- Does not store API keys.
- Does not print prompts, credentials or provider secrets.
- Routes model calls through AI Provider Service.

Version
-------
v0.6.1
==============================================================================
"""

import json
import logging
from typing import Any

from app.prompts.engineering_reasoning_prompt import (
    build_engineering_reasoning_prompt,
)
from app.services.ai_provider_service import ai_provider_service


logger = logging.getLogger(__name__)


def build_rag_prompt(query: str, evidence_chunks: list[dict[str, Any]]) -> str:
    evidence_text = "\n\n".join(
        f"Source: {chunk['source_document']} | "
        f"Chunk: {chunk['chunk_id']} | "
        f"Score: {chunk['score']}\n"
        f"{chunk['text']}"
        for chunk in evidence_chunks
    )

    return f"""
You are a power electronics reliability engineering assistant.

Use only the retrieved evidence below to answer the user's question.

If the evidence is insufficient, clearly say so.

Do not invent facts.

User Question

{query}

Retrieved Evidence

{evidence_text}

Answer using:

1. Summary
2. Supporting Evidence
3. Confidence
4. Recommended Next Step
"""


def generate_llm_answer(
    query: str,
    evidence_chunks: list[dict[str, Any]],
) -> str:
    prompt = build_rag_prompt(query, evidence_chunks)

    return ai_provider_service.generate_chat_completion(
        system_prompt="You are a careful engineering AI assistant.",
        user_prompt=prompt,
        temperature=0.2,
    )


def extract_engineering_knowledge(text: str) -> dict[str, Any]:
    """
    Extract graph-ready engineering knowledge from text.
    """
    prompt = f"""
You are an expert Power Electronics Reliability Engineer.

Extract engineering knowledge from the text below.

Return ONLY valid JSON.

Schema:

{{
    "entities":[
        {{
            "name":"",
            "type":"",
            "description":""
        }}
    ],

    "relationships":[
        {{
            "source":"",
            "relation":"",
            "target":"",
            "description":""
        }}
    ]
}}

Engineering Text:

{text}
"""

    response_text = ai_provider_service.generate_chat_completion(
        system_prompt="Return valid JSON only.",
        user_prompt=prompt,
        temperature=0,
        use_extraction_model=True,
        response_format={"type": "json_object"},
    )

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        logger.exception("Engineering knowledge extraction returned invalid JSON.")
        raise


def generate_evidence_backed_answer(
    question: str,
    semantic_evidence: list[dict[str, Any]],
    graph_evidence: dict[str, Any],
    conversation_history: list[dict[str, Any]] | None = None,
) -> str:
    """
    Generate an evidence-backed engineering answer.
    """
    prompt = build_engineering_reasoning_prompt(
        question=question,
        semantic_evidence=semantic_evidence,
        graph_evidence=graph_evidence,
        conversation_history=conversation_history or [],
    )

    return ai_provider_service.generate_chat_completion(
        system_prompt=(
            "You are a cautious engineering AI assistant. "
            "Use only supplied evidence."
        ),
        user_prompt=prompt,
        temperature=0.2,
    )