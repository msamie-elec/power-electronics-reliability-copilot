# Power Electronics Reliability Copilot

An AI-powered engineering decision-support platform for analysing reliability issues in power electronic systems using semantic retrieval, knowledge graphs, evidence-backed reasoning, and large language models.

---

# Engineering Problem

Modern power electronic systems generate large volumes of engineering documentation, technical reports, maintenance records, and reliability studies. Locating relevant technical evidence across these heterogeneous information sources is time-consuming and often depends on individual expertise.

Power Electronics Reliability Copilot addresses this challenge by combining document intelligence, semantic retrieval, knowledge graphs, and AI-assisted engineering reasoning into a single explainable engineering workflow.

Rather than generating unsupported answers, the platform retrieves engineering evidence, explores structured engineering knowledge, and produces evidence-backed responses with supporting sources and confidence information.

---

# Overview

Power Electronics Reliability Copilot is a modular AI platform designed to assist reliability engineers in exploring engineering documentation, analysing technical knowledge, and producing explainable engineering recommendations.

The platform combines:

- Intelligent document processing
- Semantic search
- Engineering Knowledge Graphs
- Retrieval-Augmented Generation (RAG)
- Hybrid GraphRAG retrieval
- Evidence-backed AI reasoning
- Conversational engineering workflows

The architecture has been designed as a collection of independent services, allowing individual components to evolve while maintaining a consistent engineering workflow.

---

# Current Features

The current implementation provides:

- ✅ React conversational engineering workspace
- ✅ FastAPI backend
- ✅ Hybrid semantic + Knowledge Graph retrieval
- ✅ Neo4j Engineering Knowledge Graph
- ✅ Evidence-backed AI reasoning
- ✅ Conversation-aware engineering discussions
- ✅ Backend conversation memory
- ✅ Backend document registry
- ✅ Active engineering document selection
- ✅ Explainable engineering responses
- ✅ Structured engineering reports
- ✅ Evidence traceability
- ✅ Automated backend regression testing

---

# Key Capabilities

## Engineering Document Intelligence

- Upload engineering documents (PDF, TXT and CSV)
- Automatic document parsing
- Metadata registration
- Intelligent document chunking
- Structured engineering document management

---

## Semantic Knowledge Retrieval

- OpenAI embedding generation
- FAISS vector indexing
- Semantic similarity search
- Retrieval-Augmented Generation (RAG)
- Source-aware evidence retrieval

---

## Engineering Knowledge Graph

- Engineering entity extraction
- Relationship extraction
- Neo4j knowledge graph population
- Engineering ontology support
- Graph validation
- Cypher query services

---

## Evidence-backed AI Reasoning

- Hybrid semantic and graph retrieval
- Knowledge Graph exploration
- Evidence-backed engineering reasoning
- Confidence-aware responses
- Explainable engineering recommendations
- Source attribution

---

## Professional Engineering Workspace

- Multi-turn engineering conversations
- Conversation-aware reasoning
- Backend conversation memory
- Active engineering document selection
- Backend document registry
- Structured engineering reports
- Interactive evidence panel
- Citation tracking
- Knowledge Graph summaries
- Professional engineering investigation workflow

---

## Software Engineering

- Modular FastAPI backend
- React + TypeScript frontend
- REST APIs
- Swagger documentation
- Automated backend testing using Pytest
- Enterprise-oriented project structure

---

# System Architecture

```text
Engineer
      │
      ▼
React Engineering Workspace
      │
      ▼
Engineering Copilot API
      │
      ▼
Engineering Answer Service
      │
      ▼
Evidence-backed Reasoning
      │
      ▼
Hybrid Retrieval
      │
 ┌────┴─────────────┐
 ▼                  ▼
FAISS         Neo4j Knowledge Graph
(Vector)      (Structured Knowledge)
      │
      ▼
Engineering Evidence
      │
      ▼
OpenAI GPT-4.1
      │
      ▼
Structured Engineering Response
```

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI |
| AI Framework | LlamaIndex |
| Workflow Orchestration | LangGraph |
| Knowledge Graph | Neo4j |
| Graph Query Language | Cypher |
| Vector Store | FAISS |
| Embeddings | OpenAI Embeddings |
| LLM | OpenAI GPT-4.1 |
| Testing | Pytest |
| Cloud (Planned) | Microsoft Azure |
| Containerisation (Planned) | Docker |
| Orchestration (Planned) | Kubernetes |

---

# Repository Structure

```text
power-electronics-reliability-copilot/

├── backend/
│   ├── app/
│   ├── uploads/
│   ├── knowledge_base/
│   ├── chunks/
│   ├── embeddings/
│   ├── graph/
│   ├── metadata/
│   └── tests/
│
├── frontend/
│
├── graph/
│
├── docker/
│
├── documents/
│
├── docs/
│   ├── architecture/
│   ├── Knowledge_Engineering/
│   ├── releases/
│   ├── development/
│   ├── adr/
│   ├── standards/
│   ├── CHANGELOG.md
│   ├── PROJECT_ROADMAP.md
│   ├── PROJECT_METHODOLOGY.md
│   ├── ENGINEERING_PLAYBOOK.md
│   └── AI_ENGINEERING_DEVELOPMENT_GUIDE.md
│
├── LICENSE
└── README.md
```

---

# Release Roadmap

| Release | Focus | Status |
|----------|-------|--------|
| v0.1.0 | Frontend Prototype | ✅ Complete |
| v0.2.0 | Backend Foundation | ✅ Complete |
| v0.3.0 | Engineering Knowledge Retrieval | ✅ Complete |
| v0.4.0 | Knowledge Graph Foundation | ✅ Complete |
| v0.5.0 | Evidence-backed Engineering Copilot | ✅ Complete |
| v0.5.1 | Conversational Engineering Copilot | ✅ Complete |
| v0.5.2 | Professional Engineering Workspace | ✅ Complete |
| v0.6.0 | Azure Cloud Deployment | 🚧 Planned |
| v0.7.0 | Production Deployment | Planned |
| v1.0.0 | Enterprise Power Electronics Reliability Copilot | Planned |

---

# Current Status

The project has completed the core engineering intelligence platform together with a professional conversational engineering workspace.

## Completed

The current implementation delivers:

- Engineering document ingestion
- Semantic document retrieval
- FAISS vector search
- Neo4j Engineering Knowledge Graph
- Hybrid GraphRAG retrieval
- Evidence-backed AI reasoning
- Engineering Copilot backend
- REST APIs
- React conversational workspace
- Backend conversation memory
- Active engineering document selection
- Backend document registry
- Structured engineering reports
- Evidence synchronisation
- Explainable engineering responses
- 20 automated backend regression tests

---

## Next Milestone

Development now transitions to **Version 0.6.0 – Azure Cloud Deployment**.

The objective of Version 0.6.0 is not to introduce significant new AI functionality, but to deploy the existing engineering platform using Microsoft Azure while preserving the architecture established during Versions 0.5.0–0.5.2.

Planned activities include:

- Azure App Service / Container Apps
- Azure OpenAI integration
- Azure Blob Storage
- Azure Key Vault
- Secure cloud configuration
- Monitoring and logging
- Deployment automation

---

# Documentation

The repository documentation is organised into dedicated engineering documents.

| Document | Purpose |
|----------|---------|
| README.md | Project overview |
| PROJECT_ROADMAP.md | Product evolution |
| CHANGELOG.md | Version history |
| PROJECT_METHODOLOGY.md | Development methodology |
| ENGINEERING_PLAYBOOK.md | Engineering standards |
| architecture/ | System architecture |
| releases/ | Release documentation |
| development/ | Implementation history |
| Knowledge_Engineering/ | Knowledge engineering design |
| adr/ | Architectural Decision Records |

---

# Getting Started

The project is fully functional for local development.

The application currently provides:

- Engineering document processing
- Semantic retrieval
- Knowledge Graph retrieval
- Evidence-backed AI reasoning
- Conversational engineering workspace
- Backend document registry
- Active engineering document selection

The next development milestone focuses on deploying the existing application to Microsoft Azure without introducing significant functional changes.

---

# License

MIT License