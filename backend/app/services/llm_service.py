from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL


def build_rag_prompt(query: str, evidence_chunks: list[dict]) -> str:
    evidence_text = "\n\n".join(
        f"Source: {chunk['source_document']} | Chunk: {chunk['chunk_id']} | Score: {chunk['score']}\n"
        f"{chunk['text']}"
        for chunk in evidence_chunks
    )

    return f"""
You are a power electronics reliability engineering assistant.

Use only the retrieved evidence below to answer the user's question.
If the evidence is insufficient, say so clearly.
Do not invent facts outside the evidence.

User question:
{query}

Retrieved evidence:
{evidence_text}

Answer using this structure:

1. Summary
2. Supporting evidence
3. Confidence
4. Recommended next step
"""


def generate_llm_answer(query: str, evidence_chunks: list[dict]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = build_rag_prompt(query, evidence_chunks)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a careful engineering AI assistant. Keep answers grounded in provided evidence.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""