"""
===========================================================================
Power Electronics Reliability Copilot
LLM Service
===========================================================================

Purpose
-------
Provides all OpenAI interactions used throughout the project.

Responsibilities
----------------
- Generate RAG answers
- Extract engineering knowledge
"""

import json

from openai import OpenAI

from app.prompts.evidence_backed_answer_prompt import (
    build_evidence_backed_prompt,
)

from app.prompts.engineering_reasoning_prompt import (
    build_engineering_reasoning_prompt,
)


from app.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_EXTRACTION_MODEL,
)


client = OpenAI(api_key=OPENAI_API_KEY)


# ==========================================================================
# RAG Answer Generation
# ==========================================================================

def build_rag_prompt(query: str, evidence_chunks: list[dict]) -> str:
    evidence_text = "\n\n".join(
        f"Source: {chunk['source_document']} | Chunk: {chunk['chunk_id']} | Score: {chunk['score']}\n"
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
    evidence_chunks: list[dict],
) -> str:

    prompt = build_rag_prompt(query, evidence_chunks)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are a careful engineering AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
    )

    return response.choices[0].message.content or ""


# ==========================================================================
# Knowledge Extraction
# ==========================================================================

def extract_engineering_knowledge(text: str) -> dict:
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

    response = client.chat.completions.create(
        model=OPENAI_EXTRACTION_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(response.choices[0].message.content)


# ==========================================================================
# Evidence-backed Engineering Answer Generation
# ==========================================================================

def generate_evidence_backed_answer(
    question: str,
    semantic_evidence: list[dict],
    graph_evidence: dict,
) -> str:
#    prompt = build_evidence_backed_prompt(
#        question=question,
#        semantic_evidence=semantic_evidence,
#        graph_evidence=graph_evidence,
#    )
    prompt = build_engineering_reasoning_prompt(
        question=question,
        semantic_evidence=semantic_evidence,
        graph_evidence=graph_evidence,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are a cautious engineering AI assistant. Use only supplied evidence.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content or ""