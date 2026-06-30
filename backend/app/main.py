from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import documents, embeddings, upload
from app.config import APP_NAME, APP_VERSION, FRONTEND_ORIGIN

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check() -> dict:
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
    }


app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(embeddings.router)