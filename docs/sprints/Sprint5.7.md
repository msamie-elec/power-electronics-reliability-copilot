# Sprint 5.7 — Knowledge Pipeline Orchestrator.

Goal:

One API call:
Register → Chunk → Embed → Build FAISS

Create:

backend/app/services/knowledge_pipeline_service.py
backend/app/api/knowledge_pipeline.py

Endpoint:

POST /knowledge-pipeline/run

Input:

{
  "file_path": "knowledge_base/reliability/Graph.pdf"
}

Output should summarise all stages:

{
  "status": "success",
  "documentId": "...",
  "chunksCreated": 15,
  "embeddingsCreated": 15,
  "vectorsIndexed": 15
}