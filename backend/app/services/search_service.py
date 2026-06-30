import json
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import EMBEDDINGS_DIR, EMBEDDING_MODEL_NAME

_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return _model


def cosine_similarity(query_vector: np.ndarray, document_vector: np.ndarray) -> float:
    return float(np.dot(query_vector, document_vector))


def load_embedding_records() -> list[dict[str, Any]]:
    records = []

    for embedding_path in EMBEDDINGS_DIR.glob("*_embeddings.json"):
        payload = json.loads(embedding_path.read_text(encoding="utf-8"))
        records.extend(payload.get("embeddings", []))

    return records


def search_similar_chunks(query: str, top_k: int = 5) -> dict[str, Any]:
    records = load_embedding_records()

    if not records:
        return {
            "query": query,
            "top_k": top_k,
            "result_count": 0,
            "results": [],
        }

    model = get_embedding_model()
    query_vector = model.encode(query, normalize_embeddings=True)

    scored_results = []

    for record in records:
        document_vector = np.array(record["embedding"], dtype=np.float32)
        score = cosine_similarity(query_vector, document_vector)

        scored_results.append(
            {
                "score": round(score, 4),
                "chunk_id": record["chunk_id"],
                "source_document": record["source_document"],
                "source_text_file": record["source_text_file"],
                "chunk_index": record["chunk_index"],
                "page_start": record["page_start"],
                "page_end": record["page_end"],
                "character_count": record["character_count"],
                "word_count": record["word_count"],
                "text": record.get("text", ""),
            }
        )

    scored_results.sort(key=lambda item: item["score"], reverse=True)

    return {
        "query": query,
        "top_k": top_k,
        "result_count": min(top_k, len(scored_results)),
        "results": scored_results[:top_k],
    }