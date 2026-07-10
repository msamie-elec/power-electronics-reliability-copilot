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
- Azure cloud integration
- Secure secret management
- Observability and health diagnostics

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
- ✅ Automatic engineering document indexing after upload
- ✅ Azure Blob Storage integration
- ✅ Azure OpenAI integration
- ✅ Azure Key Vault integration
- ✅ Azure Monitor and Application Insights foundation
- ✅ Production-style health diagnostics
- ✅ Backend regression testing
- ✅ Frontend production build validation

---

# Key Capabilities

## Engineering Document Intelligence

- Upload engineering documents (PDF, TXT and CSV)
- Automatic document parsing
- Metadata registration
- Intelligent document chunking
- Structured engineering document management
- Automatic post-upload indexing

---

## Semantic Knowledge Retrieval

- Embedding generation
- FAISS vector indexing
- Semantic similarity search
- Retrieval-Augmented Generation
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

## Conversational Engineering Workspace

- Multi-turn engineering conversations
- Conversation-aware reasoning
- Backend conversation memory
- Active engineering document selection
- Backend document registry
- Structured engineering reports
- Interactive evidence panel
- Citation tracking
- Knowledge Graph summaries
- Engineering investigation workflow

---

## Cloud and Operations

- Azure Blob Storage document persistence
- Azure OpenAI provider support
- Azure Key Vault secret management
- Provider-based secret retrieval
- Azure Monitor and Application Insights resources
- `/health` lightweight health endpoint
- `/health/details` dependency diagnostics endpoint
- Azure infrastructure automation scripts
- Key Vault and monitoring validation scripts

---

## Software Engineering

- Modular FastAPI backend
- React + TypeScript frontend
- REST APIs
- Swagger/OpenAPI documentation
- Provider-based architecture
- Automated backend testing using Pytest
- Frontend production build validation
- Cloud-ready configuration

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
Azure OpenAI / OpenAI
      │
      ▼
Structured Engineering Response
```

---

# Cloud Architecture

```text
FastAPI Backend
      │
      ├── SecretService
      │       ├── LocalSecretProvider
      │       └── AzureKeyVaultSecretProvider
      │
      ├── DocumentStorageService
      │       ├── LocalStorageProvider
      │       └── AzureBlobStorageProvider
      │
      ├── AIProviderService
      │       ├── OpenAI
      │       └── Azure OpenAI
      │
      ├── Neo4j Aura
      │
      └── Health Diagnostics
              ├── Azure Key Vault
              ├── Azure Blob Storage
              ├── Azure OpenAI
              └── Neo4j
```

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI |
| Knowledge Graph | Neo4j Aura |
| Graph Query Language | Cypher |
| Vector Store | FAISS |
| Embeddings | OpenAI / Azure OpenAI embeddings |
| LLM | OpenAI / Azure OpenAI GPT deployments |
| Cloud Storage | Azure Blob Storage |
| Secret Management | Azure Key Vault |
| Observability | Azure Monitor + Application Insights |
| Testing | Pytest |
| Cloud Platform | Microsoft Azure |
| Containerisation | Planned for v0.7.0 |
| Production Hosting | Planned for v0.7.0 |

---

# Repository Structure

```text
power-electronics-copilot/

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
├── infra/
│   └── azure/
│       ├── env/
│       ├── powershell/
│       └── tests/
│
├── docker/
│
├── documents/
│
├── docs/
│   ├── architecture/
│   ├── cloud/
│   ├── Knowledge_Engineering/
│   ├── releases/
│   ├── development/
│   ├── adr/
│   └── standards/
│
├── CHANGELOG.md
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
| v0.6.0 | Cloud-Native Azure Integration | ✅ Complete |
| v0.7.0 | Production Engineering and DevOps | Planned |
| v1.0.0 | Enterprise Power Electronics Reliability Copilot | Planned |

---

# Current Status

Version **v0.6.0** is complete.

The project now provides the core engineering intelligence platform together with Azure cloud integration, secure secret management, observability foundations and health diagnostics.

## Completed

The current implementation delivers:

- Engineering document ingestion
- Automatic document indexing
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
- Azure Blob Storage integration
- Azure OpenAI integration
- Azure Key Vault secret management
- Azure Monitor and Application Insights resources
- Health diagnostics for Azure services and Neo4j
- 25 automated backend regression tests
- Frontend production build validation

---

## Next Milestone

Development now transitions to **Version 0.7.0 — Production Engineering and DevOps**.

The objective of Version 0.7.0 is to move from cloud-integrated local execution toward production deployment and operational hardening.

Planned activities include:

- Docker containerisation
- Azure Container Apps backend deployment
- Azure Static Web Apps frontend deployment
- Managed Identity for Azure-hosted backend services
- Azure RBAC-based Blob Storage access
- Removal of Azure Storage connection string dependency
- Production environment configuration
- CI/CD workflow
- Production monitoring and diagnostics

---

# Validation

## Backend

From `backend`:

```powershell
pytest -v
```

Expected result:

```text
25 passed
```

## Frontend

From `frontend`:

```powershell
npm run build
```

Expected result:

```text
built
```

## Azure Key Vault

From repository root:

```powershell
.\infra\azure\powershell\05c-validate-keyvault.ps1
```

Expected result:

```text
Required secrets are present and accessible.
```

## Azure Monitoring

From repository root:

```powershell
.\infra\azure\powershell\06c-validate-monitoring.ps1
```

Expected result:

```text
Azure monitoring validation completed.
```

## Health Endpoints

Run the backend and check:

```text
http://localhost:8000/health
http://localhost:8000/health/details
```

Expected result:

- `/health` reports the service as healthy.
- `/health/details` reports Azure Key Vault, Azure Blob Storage and Neo4j as healthy, with Azure OpenAI configuration resolved.

---

# Documentation

The repository documentation is organised into dedicated engineering documents.

| Document | Purpose |
|----------|---------|
| README.md | Project overview |
| CHANGELOG.md | Version history |
| docs/releases/ | Release documentation |
| docs/cloud/ | Cloud validation and observability documentation |
| docs/architecture/ | System architecture |
| docs/Knowledge_Engineering/ | Knowledge engineering design |
| docs/development/ | Implementation history |
| docs/adr/ | Architectural Decision Records |
| docs/standards/ | Repository standards |
| infra/azure/README.md | Azure infrastructure workflow |

---

# Getting Started

The project is fully functional for local development with cloud-integrated services.

The application currently provides:

- Engineering document processing
- Semantic retrieval
- Knowledge Graph retrieval
- Evidence-backed AI reasoning
- Conversational engineering workspace
- Backend document registry
- Active engineering document selection
- Azure Blob Storage support
- Azure OpenAI support
- Azure Key Vault secret retrieval
- Health diagnostics

The next development milestone focuses on production deployment and operational hardening.

---

# License

MIT License
