# Changelog

All notable changes to this project are documented in this file.

The format is based on **Keep a Changelog** and follows semantic versioning.

---

# [Unreleased]

## Planned
✅ v0.1 — Frontend Prototype
✅ v0.2 — Backend Foundation
✅ v0.3 — Engineering RAG Copilot
✅ v0.4 — Knowledge Graph Foundation
🚧 v0.5 — Explainable Engineering Copilot (currently in progress)
✅ Sprint 5.10
✅ Sprint 5.11
✅ Sprint 5.12
▶️ Sprint 5.13 (next)

At this stage, the backend architecture is becoming quite mature. Sprint 5.13 can now focus on making the copilot produce high-quality engineering answers rather than simply connecting the pipeline. This is where the system begins transitioning from a RAG application into an explainable engineering AI assistant.

# Sprint 5.12 — Engineering Copilot API (Completed)

Implemented the first end-to-end Engineering Copilot backend, enabling evidence-backed engineering question answering by combining semantic retrieval, knowledge graph reasoning, and Large Language Model (LLM) generation.

Completed
Added /engineering-copilot/ask REST API.
Integrated semantic evidence retrieval with Knowledge Graph context.
Implemented evidence-backed prompt generation using a dedicated prompt module.
Refactored LLM prompt construction out of llm_service.py to improve modularity and maintainability.
Implemented end-to-end engineering answer generation using OpenAI.
Added comprehensive API validation and error handling.
Added automated unit and integration tests for the Engineering Copilot endpoint.
Verified compatibility with Sprint 5.10 (Knowledge Graph Retrieval) and Sprint 5.11 (Evidence-backed Reasoning Context).
Validation
Engineering Copilot API tests: 5/5 passed
Backend regression tests (Sprints 5.10–5.12): 20/20 passed

Status: ✅ Completed


## Sprint 5.11 — Evidence-backed AI Reasoning ✅

Introduced the first version of the Evidence-backed AI Reasoning layer, providing a unified reasoning context for engineering questions by combining semantic document retrieval and Knowledge Graph evidence.

### Added

- Evidence Reasoning Service for building structured reasoning context.
- Integration of FAISS semantic retrieval with Neo4j graph retrieval.
- REST API endpoint: `POST /evidence-reasoning/context`.
- Structured reasoning context containing semantic evidence, graph evidence, and reasoning metadata.
- Request validation to reject invalid or empty engineering questions.
- Comprehensive integration tests covering successful requests, validation, retrieval limits, and error handling.

### Outcome

The backend now provides a reusable evidence-backed reasoning context that serves as the foundation for the Engineering Copilot's grounded AI responses in the next sprint.



# Add that Sprint 5.9 delivered:

Neo4j population service
/knowledge-graph/populate
successful population from DOC-B3198A5
graph summary endpoint
/knowledge-graph/summary
34 nodes and 21 relationships verified

## Completed up to end of Sprint 5.9B Status: Completed ✅

You now have the first version of an automatically populated engineering knowledge graph.

From the screenshots I can see:

23 EngineeringEntity nodes
11 specialised entity labels
23 relationships
No skipped relationships
Neo4j MERGE working correctly
REST endpoint working correctly
Population service working correctly

Where we are in the overall architecture

This is approximately where the project now stands.

PDF
 │
 ▼
Registration
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
Knowledge Extraction
 │
 ▼
Graph JSON
 │
 ▼
Neo4j Population   ← COMPLETE
 │
 ▼
Knowledge Graph
 │
 ├─────────────► Graph Queries
 │
 └─────────────► GraphRAG

Everything above the line is now operational.

# Sprint 5.6 is complete

# Sprint 5.5 is COMPLETE ✅

From your screenshots:

✅ /knowledge-search/search appears in Swagger.
✅ Endpoint returns 200 OK.
✅ FAISS successfully searched the index.
✅ The embedding model loaded correctly.
✅ The correct document was searched.
✅ Top-k results were returned.
✅ Returned chunk text, chunk ID, score and metadata.
✅ No Python exceptions.

# Sprint 5.4 is complete.

Confirmed:

{
  "status": "success",
  "documentId": "DOC-7E311A25",
  "vectorsIndexed": 15,
  "dimension": 384,
  "indexFile": "vector_store\\knowledge\\DOC-7E311A25.index",
  "mappingFile": "vector_store\\knowledge\\DOC-7E311A25_mapping.json"
}

You now have:

Knowledge PDF
↓
Register
↓
Chunk
↓
Embedding
↓
FAISS Index


### v0.5.0 — GraphRAG Pipeline

- GraphRAG implementation
- Neo4j retrieval integration
- Hybrid vector + graph retrieval
- Knowledge graph traversal
- Engineering reasoning pipeline

---

# v0.4.0 — Knowledge Graph Foundation

Release Status:
✅ Completed

## Added

### Sprint 4.1 — Neo4j Integration

- Neo4j Aura database
- Graph service
- FastAPI connectivity
- Health endpoint
- Environment configuration

### Sprint 4.2 — Ontology Design

- Engineering ontology
- Node definitions
- Relationship definitions
- Property model
- Identifier strategy

### Sprint 4.3 — Knowledge Graph Design

- Neo4j schema
- Knowledge ingestion architecture
- Engineering ontology documentation
- Three ontology diagrams
- Graph schema documentation

### Sprint 4.4 — Graph Implementation

- Graph constraints
- Search indexes
- Seed engineering dataset
- Knowledge graph creation
- Sample engineering graph

### Sprint 4.5 — Validation & Querying

- Graph validation
- Graph statistics
- Engineering Cypher queries
- Validation queries
- End-to-end graph verification

### Sprint 4.6 — Repository Structure

- Graph module
- Documentation structure
- ADR framework
- Standards directory
- Sprint history
- Graph README

### Sprint 4.7 — GraphRAG Preparation

- GraphRAG preparation
- Chunking strategy
- Embedding strategy
- Retrieval workflow
- Source tracking design

### Sprint 4.8 — Enterprise Documentation

- Knowledge Graph Overview
- Neo4j Schema documentation
- Repository documentation
- Architecture documentation
- Data model documentation
- Future expansion roadmap

## Repository Milestone

The repository now includes:

- Engineering ontology
- Neo4j knowledge graph
- Cypher schema
- Constraints
- Indexes
- Seed dataset
- Validation queries
- Engineering queries
- Enterprise documentation
- Architecture Decision Records (ADRs)

This release establishes the complete **Knowledge Graph Foundation** for future GraphRAG development.

---

# v0.3.0 — Engineering Knowledge Retrieval

Released:
June 2026

## Added

### Sprint 3.1 — Document Processing

- PDF parsing
- Automatic text extraction
- Metadata generation

### Sprint 3.2 — Chunking

- Document chunking
- Chunk identifiers
- Metadata generation

### Sprint 3.3 — Embeddings

- Sentence Transformer embeddings
- Embedding persistence

### Sprint 3.4 — Vector Search

- FAISS vector database
- Semantic similarity search
- Top-k retrieval

### Sprint 3.5 — Engineering Retrieval

- Evidence retrieval
- Confidence estimation
- Structured engineering responses

### Sprint 3.6 — Frontend Integration

- React integration
- Evidence display
- Confidence indicator
- Source attribution

### Sprint 3.7 — LLM Integration

- OpenAI integration
- Prompt engineering
- Retrieval-Augmented Generation (RAG)

### Sprint 3.8 — Testing

- Pytest
- API validation
- End-to-end testing
- Documentation improvements

---

# v0.2.0 — Backend Foundation

Released:
June 2026

## Added

- FastAPI backend
- REST API
- File upload
- Document management
- Modular backend architecture

---

# v0.1.0 — Frontend Prototype

Released:
June 2026

## Added

- React
- TypeScript
- Vite
- Engineering dashboard
- Initial project documentation