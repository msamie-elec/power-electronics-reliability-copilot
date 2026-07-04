"""
===========================================================================
Power Electronics Reliability Copilot
Application Entry Point
===========================================================================

File:
    main.py

Purpose:
    Create and configure the FastAPI application.

Why this file exists:
    This is the main entry point of the backend application. It initializes
    the FastAPI server, configures middleware, registers API routes and
    exposes the application that serves all backend services.

Responsibilities:
    - Create the FastAPI application
    - Configure CORS middleware
    - Register API routers
    - Expose health check endpoint
    - Bootstrap the backend application

This file DOES NOT:
    - Implement business logic
    - Process engineering documents
    - Perform AI reasoning
    - Interact directly with Neo4j or FAISS

Those responsibilities are delegated to the corresponding API endpoints
and service modules.
"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import documents, embeddings, graph, rag, search, upload
from app.api.knowledge_documents import router as knowledge_documents_router
from app.config import APP_NAME, APP_VERSION, FRONTEND_ORIGIN
from app.api.knowledge_chunks import router as knowledge_chunks_router
from app.api.knowledge_embeddings import router as knowledge_embeddings_router
from app.api.knowledge_faiss import router as knowledge_faiss_router
from app.api.knowledge_search import router as knowledge_search_router
from app.api.knowledge_pipeline import router as knowledge_pipeline_router
from app.api.knowledge_extraction import router as knowledge_extraction_router
from app.api.graph_population import router as graph_population_router
from app.api.graph_validation import router as graph_validation_router
from app.api.knowledge_graph_retrieval import router as knowledge_graph_retrieval_router
from app.api.evidence_reasoning import router as evidence_reasoning_router

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
app.include_router(search.router)
app.include_router(rag.router)
app.include_router(graph.router)
app.include_router(knowledge_documents_router)
app.include_router(knowledge_chunks_router)
app.include_router(knowledge_embeddings_router)
app.include_router(knowledge_faiss_router)
app.include_router(knowledge_search_router)
app.include_router(knowledge_pipeline_router)
app.include_router(knowledge_extraction_router)
app.include_router(graph_population_router)
app.include_router(graph_validation_router)
app.include_router(knowledge_graph_retrieval_router)
app.include_router(evidence_reasoning_router)
