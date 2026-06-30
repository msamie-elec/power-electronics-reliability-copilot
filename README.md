# Power Electronics Reliability Copilot

Enterprise AI Copilot for diagnosing reliability issues in power electronic systems using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Knowledge Graphs, and Agentic AI.

---

# Project Overview

Power Electronics Reliability Copilot is an enterprise-grade AI application designed to assist reliability engineers with diagnosing failures in power electronic systems using engineering documents, maintenance records, knowledge graphs, and AI reasoning.

The project is being developed incrementally as a portfolio-quality demonstration of modern AI engineering techniques.

## Example capabilities

* Upload engineering documents
* Analyse datasheets and technical manuals
* Retrieve technical evidence using RAG
* Reason over engineering knowledge graphs
* Recommend likely failure mechanisms
* Explain recommendations with supporting evidence
* Support engineering decision making

---

# Technology Stack

| Layer           | Technology                    |
| --------------- | ----------------------------- |
| Frontend        | React + TypeScript + Vite     |
| Backend         | FastAPI                       |
| AI Framework    | LlamaIndex                    |
| Agent Framework | LangGraph                     |
| Knowledge Graph | Neo4j                         |
| Vector Store    | FAISS (later Azure AI Search) |
| LLM             | OpenAI / Azure OpenAI         |
| Deployment      | Docker                        |
| Cloud           | Microsoft Azure               |
| Orchestration   | Kubernetes                    |

---

# Repository Structure

```text
power-electronics-copilot
│
├── architecture/
├── backend/
│   ├── app/
│   ├── uploads/
│   └── tests/
│
├── frontend/
│   ├── src/
│   └── public/
│
├── graph/
├── docker/
├── docs/
│   ├── releases/
│   └── CHANGELOG.md
│
├── LICENSE
└── README.md
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

---

# Current Status

**Current Release**

## v0.2.0 — Backend Foundation

### Completed

* Professional React dashboard
* FastAPI REST API
* Modular backend architecture
* File upload API
* Document management API
* Frontend–backend integration
* Local document repository
* Versioned release documentation
* Enterprise project structure

### Next Release

**v0.3.0 — Engineering Knowledge Retrieval**

Planned additions:

* PDF parsing
* Text extraction
* Document chunking
* Embedding generation
* Vector database
* Semantic search
* Source attribution

---

# Long-Term Architecture

```
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

