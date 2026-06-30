from typing import Any

from app.services.search_service import search_similar_chunks


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

    evidence_summary = []

    for chunk in chunks:
        evidence_summary.append(
            {
                "source_document": chunk["source_document"],
                "chunk_id": chunk["chunk_id"],
                "score": chunk["score"],
                "excerpt": chunk["text"][:500],
            }
        )

    answer = (
        "Based on the retrieved engineering evidence, the most relevant information "
        "appears in the indexed document chunks listed below. These chunks should be "
        "reviewed to support diagnosis, identify likely failure mechanisms, and plan "
        "inspection or maintenance actions."
    )

    confidence = "Medium" if chunks[0]["score"] >= 0.6 else "Low"

    return {
        "query": query,
        "answer": answer,
        "confidence": confidence,
        "sources": evidence_summary,
        "retrieved_chunks": chunks,
    }