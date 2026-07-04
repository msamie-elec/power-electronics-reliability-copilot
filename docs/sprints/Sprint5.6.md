# Sprint 5.6 — Retrieval Service

Instead of returning huge JSON directly from the search endpoint, create a reusable retrieval service.

Currently:

API
 ↓
FAISS

Better:

API
 ↓
Retrieval Service
 ↓
FAISS

Why?

Because later:

RAG
Agent
Neo4j
LlamaIndex

will all reuse the same retrieval layer.

This is proper software architecture.

Sprint 5.7 — Pipeline Orchestrator ⭐

This is the one I strongly recommend.

Instead of manually calling

Register

↓

Chunk

↓

Embedding

↓

FAISS

create one endpoint:

POST /knowledge/pipeline

Input

{
    "file_path": "knowledge_base/reliability/Graph.pdf"
}

It automatically performs

Register

↓

Chunks

↓

Embeddings

↓

FAISS

and returns

{
  "documentId":"...",
  "chunks":15,
  "embeddings":15,
  "vectors":15,
  "status":"completed"
}

This is exactly how enterprise AI ingestion pipelines are designed.

Why I recommend these two

If we stop now, every document requires four manual API calls.

Real systems never do that.

Instead they expose one ingestion pipeline.

It also looks much more impressive in interviews.

After v0.5

Then we move to v0.6, where the really interesting AI work begins:

v0.6

LlamaIndex

↓

Document Store

↓

Vector Store Index

↓

Query Engine

↓

Retriever

↓

Hybrid Retrieval

↓

Comparison with our FAISS pipeline

This is where you'll gain hands-on experience with LlamaIndex, which, as you noted, appears in many AI and GenAI job descriptions. We'll build it properly rather than just calling a library, so you'll understand both the underlying architecture (which we've just implemented ourselves) and the higher-level framework.

My recommendation

Let's treat v0.5 as an enterprise-quality ingestion pipeline by adding just two more sprints:

Sprint 5.6 — Retrieval Service
Sprint 5.7 — One-click Knowledge Pipeline Orchestrator

Then we can close v0.5.0 completely and move on to v0.6.0 (LlamaIndex Integration). I think that's the strongest progression both technically and for your CV/interviews.


# Updates:
Sprint 5.6 — Retrieval Service
Goal

Move all FAISS retrieval logic out of the API and into a reusable service layer.

Current architecture:

API
 │
 ▼
FAISS

Target architecture:

API
 │
 ▼
Knowledge Retrieval Service
 │
 ▼
FAISS Index

Later this same service will be used by:

RAG
LlamaIndex
LangGraph Agents
Neo4j GraphRAG
Future REST endpoints