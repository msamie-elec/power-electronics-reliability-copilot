# Changelog

Current Version: v0.3.0

All notable changes to this project will be documented in this file.

The format follows Keep a Changelog principles.

---

# v0.4.0
# Sprint 4.1:
Sprint 4.1 Status

We can now officially mark the first major objective of v0.4.0 as complete.

Sprint 4.1 — Neo4j Integration
Completed
✅ Created dedicated Neo4j Aura database for the Power Electronics project
✅ Configured secure environment variables
✅ Installed Neo4j Python driver
✅ Implemented Graph Service
✅ Added /graph/health API endpoint
✅ Verified FastAPI ↔ Neo4j connectivity
✅ Confirmed successful query execution (RETURN 1)
Current Architecture
Frontend (React)
        │
        ▼
FastAPI
        │
        ├─────────────► FAISS
        │                │
        │                ▼
        │           Semantic Search
        │
        └─────────────► Neo4j Aura
                         │
                         ▼
                 Graph Database

This is a significant architectural milestone: your application now has both retrieval mechanisms in place:

a vector store (FAISS) for semantic similarity, and
a graph database (Neo4j) for structured relationships.

which means:

✅ FastAPI can reach Neo4j Aura
✅ DNS resolution is working
✅ Authentication succeeded
✅ The Neo4j Python driver is working
✅ Your .env configuration is correct
✅ Your Graph Service is functioning


# v0.3.0 — Engineering RAG Copilot

Release status:
🚧 Release Candidate

## Added

### Sprint 3.1 — Document Processing

- PDF parsing
- Automatic text extraction
- TXT generation
- Metadata generation

### Sprint 3.2 — Intelligent Chunking

- Document chunk generation
- Chunk metadata
- Word counts
- Chunk identifiers
- Timestamp metadata

### Sprint 3.3 — Embedding Generation

- Sentence Transformer embeddings
- Embedding persistence
- Embedding metadata

### Sprint 3.4 — Semantic Search

- Cosine similarity search
- Top-k retrieval
- Search API

### Sprint 3.5 — Engineering Retrieval

- Evidence retrieval
- Structured engineering responses
- Confidence estimation

### Sprint 3.6 — Frontend Integration

- Frontend RAG integration
- Evidence display
- Confidence display
- Source attribution

### Sprint 3.7 — LLM Integration

- OpenAI integration
- Prompt engineering
- Grounded engineering answers
- RAG pipeline

### Sprint 3.8 — Testing & Release Preparation

#### Sprint 3.8.1

- Pytest integration
- API tests
- TestClient configuration
- Backend validation

#### Sprint 3.8.2

- End-to-end workflow validation
- Invalid input handling
- File type validation
- Empty question validation
- Upload workflow improvements

#### Sprint 3.8.3

- Documentation updates
- README improvements
- Roadmap updates
- Release preparation

---

# v0.2.0 — Backend Foundation

Released: 30 June 2026

## Added

- FastAPI backend
- REST API architecture
- Swagger/OpenAPI
- File upload
- Document management
- Modular backend

---

# v0.1.0 — Frontend Prototype

Released: 30 June 2026

## Added

- React frontend
- TypeScript
- Vite
- Enterprise dashboard
- Engineering UI
- Project documentation