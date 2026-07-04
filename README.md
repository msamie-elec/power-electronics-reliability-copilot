# Power Electronics Reliability Copilot

Enterprise AI Copilot for diagnosing reliability issues in power electronic systems using Knowledge Graphs, GraphRAG, Retrieval-Augmented Generation (RAG), Large Language Models (LLMs) and Agentic AI

---

# Project Overview

Power Electronics Reliability Copilot is an enterprise-grade AI application designed to assist reliability engineers with diagnosing failures in power electronic systems using engineering documents, maintenance records, knowledge graphs, and AI reasoning.

The project is being developed incrementally as a portfolio-quality demonstration of modern AI engineering techniques.

## Example capabilities

- Upload PDF, TXT and CSV engineering documents
- Automatically parse and index technical documents
- Generate semantic embeddings
- Retrieve relevant engineering evidence using RAG
- Produce evidence-backed AI answers
- Display confidence level and retrieved source chunks
- Prepare engineering knowledge for future GraphRAG reasoning
Also graph:
• Engineering ontology modelling
• Neo4j knowledge graph
• Engineering document ingestion
• Graph validation
• Cypher query library
• GraphRAG preparation
• Hybrid graph + vector retrieval
• Evidence-backed AI reasoning

---

# Technology Stack

| Layer           | Technology                    |
| --------------- | ----------------------------- |
| Frontend        | React + TypeScript + Vite     |
| Backend         | FastAPI                       |
| AI Framework    | LlamaIndex                    |
| Agent Framework | LangGraph                     |
| Knowledge Graph | Neo4j                         |
| Graph Query Language | Cypher                   |
| Vector Store    | FAISS (later Azure AI Search) |
| Embeddings      | OpenAI Embeddings             |
| LLM             | OpenAI GPT-4.1 (Azure OpenAI planned)         |
| Deployment      | Docker                        |
| Cloud           | Microsoft Azure               |
| Orchestration   | Kubernetes                    |
| Agent Framework | LangGraph                     |

---

# Repository Structure

```text
power-electronics-copilot/
│
├── architecture/
│
├── backend/
│   ├── app/
│   ├── uploads/
│   └── tests/
│
├── frontend/
│   ├── public/
│   └── src/
│
├── graph/
│   ├── schema/
│   ├── seed/
│   ├── queries/
│   └── README.md
│
├── documents/
│
├── docker/
│
├── docs/
│   ├── adr/
│   ├── graph_rag/
│   ├── ontology/
│   ├── releases/
│   ├── sprints/
│   ├── standards/
│   ├── AI_ENGINEERING_DEVELOPMENT_MANUAL.md
│   ├── CHANGELOG.md
│   ├── PROJECT_METHODOLOGY.md
│   ├── PROJECT_ROADMAP.md
│   └── SYSTEM_ARCHITECTURE.md
│
├── .gitignore
├── LICENSE
└── README.md

Updates:
backend/
│
├── app/
├── uploads/
├── knowledge_base/
├── chunks/
│   ├── investigation/
│   └── knowledge/
├── embeddings/
│   ├── investigation/
│   └── knowledge/
├── graph/
├── metadata/
└── tests/


```

---

# Development Roadmap

| Version | Capability                      | Main Technology           |
| ------- | ------------------------------- | ------------------------- |
| v0.1.0  | Frontend Prototype              | React                     |
| v0.2.0  | Backend Foundation              | FastAPI                   |
| v0.3.0  | Engineering Knowledge Retrieval | LlamaIndex + Vector Store |
| v0.4.0  | Knowledge Graph Intelligence    | Neo4j + GraphRAG          |
| v0.5.0  | AI Engineering Agent            | LangGraph                 |
| v0.6.0  | Cloud Deployment                | Azure                     |
| v0.7.0  | Production Platform             | Docker + Kubernetes       |
| v1.0.0  | Enterprise AI Copilot           | Complete System           |

---

# Skills Demonstrated

* Enterprise AI Architecture
* FastAPI API Development
* React & TypeScript
* Retrieval-Augmented Generation (RAG)
* Knowledge Graphs (Neo4j)
* GraphRAG
* Agentic AI
* LangGraph
* LlamaIndex
* Prompt Engineering
* Azure AI
* Docker
* Kubernetes
* Git & GitHub
* Software Architecture
* Engineering Documentation
* Vector Databases (FAISS)
* Automated Testing (Pytest)
Knowledge Engineering
* Ontology Design
* Graph Data Modelling
* Cypher
* Graph Validation
* Knowledge Representation
---

# Current Status

**Current Release**

## v0.3.0 — Engineering Knowledge Retrieval

### Completed

- Professional React + TypeScript dashboard
- FastAPI REST API
- Modular backend architecture
- Multi-document upload
- Document management API
- PDF, TXT and CSV ingestion
- Automatic text extraction
- Document chunking
- Embedding generation using Sentence Transformers
- Local FAISS vector database
- Semantic similarity search
- Retrieval-Augmented Generation (RAG)
- OpenAI LLM integration
- Source attribution with evidence chunks
- Engineering confidence indicator
- Backend API validation
- Automated API testing using Pytest
- Manual validation scenarios
- Enterprise project structure

Completed
✓ Engineering ontology
✓ Neo4j schema
✓ Knowledge graph
✓ Constraints
✓ Indexes
✓ Seed graph
✓ Validation
✓ Cypher query library
✓ GraphRAG preparation

### Next Release

**v0.4.0 — Knowledge Graph Intelligence**

v0.5

GraphRAG Integration

---
# Architecture:
Engineering Documents
          │
          ▼
      LlamaIndex
(Document Processing)
          │
 ┌────────┴────────┐
 ▼                 ▼
Neo4j          Vector Store
 │                  │
 └────────┬─────────┘
          ▼
     Hybrid GraphRAG
          ▼
      LangGraph
          ▼
Engineering AI Copilot

### Notice this makes each technology's responsibility clear:

LlamaIndex → ingestion, indexing, retrieval orchestration
Neo4j → structured engineering knowledge
FAISS/Azure AI Search → semantic vector retrieval
LangGraph → agent orchestration
GPT → reasoning and generation

# Long-Term Architecture

```
New version:

Engineering Documents
          │
          ▼
      LlamaIndex
(Document Processing)
          │
          ▼
      Chunking
          │
          ▼
      Embeddings
          │
    ┌─────┴─────┐
    ▼           ▼
 FAISS      Neo4j Knowledge Graph
(Vector)     (Structured Knowledge)
    │           │
    └─────┬─────┘
          ▼
 Hybrid Retrieval
(Graph + Vector)
          │
          ▼
   LangGraph Agent
          │
          ▼
 OpenAI GPT-4.1
 (Reasoning)
          │
          ▼
Engineering AI Copilot


```
### Earlier version:
React + TypeScript
          │
          ▼
FastAPI Backend
          │
          ▼
Document Processing Pipeline
          │
          ▼
Chunking + Embeddings
          │
    ┌─────┴─────┐
    ▼           ▼
 FAISS       Neo4j
    │           │
    └─────┬─────┘
          ▼
   Hybrid GraphRAG
          ▼
   LangGraph Agent
          ▼
 Engineering Recommendation

```
## Outdated Architecture:
React Frontend
        │
        ▼
FastAPI Backend
        │
        ▼
Document Processing
        │
        ▼
LlamaIndex
        │
 ┌──────┴────────┐
 ▼               ▼
Vector Store   Neo4j
      │          │
      └────┬─────┘
           ▼
      LangGraph Agent
           ▼
Engineering Recommendation
```

---

# Documentation

* Architecture diagrams
* Release notes
* CHANGELOG
* Development roadmap
* Version history

---

# License

MIT License

---

