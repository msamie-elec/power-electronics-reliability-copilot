from typing import Any

from app.services.search_service import search_similar_chunks


def calculate_confidence(score: float) -> str:
    if score >= 0.85:
        return "High"
    if score >= 0.70:
        return "Medium"
    return "Low"


def answer_question_with_retrieval(query: str, top_k: int = 5) -> dict[str, Any]:
    retrieval_result = search_similar_chunks(query=query, top_k=top_k)
    chunks = retrieval_result["results"]

    if not chunks:
        return {
            "query": query,
            "answer": "No relevant engineering evidence was found in the indexed documents.",
            "confidence": "Low",
            "sources": [],
            "retrieved_chunks": [],
        }

    top_score = chunks[0]["score"]
    confidence = calculate_confidence(top_score)

    evidence_summary = []

    for chunk in chunks:
        evidence_summary.append(
            {
                "source_document": chunk["source_document"],
                "chunk_id": chunk["chunk_id"],
                "chunk_index": chunk["chunk_index"],
                "score": chunk["score"],
                "excerpt": chunk["text"][:700],
            }
        )

    answer = (
        "The retrieved engineering evidence suggests that the most relevant information "
        "is contained in the source documents listed below. Review the highest-scoring "
        "chunks first, as they are most semantically related to the question. "
        "A full LLM-generated engineering explanation will be added in Sprint 3.7."
    )

    return {
        "query": query,
        "answer": answer,
        "confidence": confidence,
        "top_score": top_score,
        "sources": evidence_summary,
        "retrieved_chunks": chunks,
    }