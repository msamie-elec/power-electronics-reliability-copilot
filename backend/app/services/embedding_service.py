import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sentence_transformers import SentenceTransformer

from app.config import CHUNKS_DIR, EMBEDDINGS_DIR, EMBEDDING_MODEL_NAME

EMBEDDINGS_DIR.mkdir(exist_ok=True)

_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return _model


def generate_embeddings_from_chunks_file(chunks_path: Path) -> dict[str, Any]:
    payload = json.loads(chunks_path.read_text(encoding="utf-8"))

    chunks = payload["chunks"]
    texts = [chunk["text"] for chunk in chunks]

    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True)

    created_at = datetime.now().isoformat(timespec="seconds")

    embedding_records = []

    for chunk, vector in zip(chunks, vectors):
        embedding_records.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source_document": chunk["source_document"],
                "source_text_file": chunk["source_text_file"],
                "chunk_index": chunk["chunk_index"],
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "character_count": chunk["character_count"],
                "word_count": chunk["word_count"],
                "embedding_model": EMBEDDING_MODEL_NAME,
                "embedding_dimension": len(vector),
                "created_at": created_at,
                "embedding": vector.tolist(),
            }
        )

    output_path = EMBEDDINGS_DIR / f"{chunks_path.stem.replace('_chunks', '')}_embeddings.json"

    result = {
        "source_chunks_file": chunks_path.name,
        "source_document": payload.get("source_document"),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_count": len(embedding_records),
        "embedding_dimension": len(embedding_records[0]["embedding"])
        if embedding_records
        else 0,
        "created_at": created_at,
        "embeddings": embedding_records,
    }

    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result


def generate_all_embeddings() -> list[dict[str, Any]]:
    results = []

    for chunks_path in CHUNKS_DIR.glob("*_chunks.json"):
        results.append(generate_embeddings_from_chunks_file(chunks_path))

    return results