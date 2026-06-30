from fastapi import APIRouter

from app.services.embedding_service import generate_all_embeddings

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])


@router.post("/generate")
def generate_embeddings() -> dict:
    results = generate_all_embeddings()

    return {
        "status": "completed",
        "processed_files": len(results),
        "results": results,
    }