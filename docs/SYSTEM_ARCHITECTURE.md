# System Architecture

## Overview

Power Electronics Reliability Copilot is structured as a modular enterprise AI application.

The system is designed to evolve incrementally from a frontend prototype into a full-stack AI platform combining FastAPI, document ingestion, Retrieval-Augmented Generation, Neo4j knowledge graphs, LangGraph orchestration, and cloud-ready deployment.

## Current Architecture — v0.1.0

At v0.1.0, the system contains only the frontend prototype.

```text
User
 ↓
React + TypeScript Frontend
 ↓
Local UI State

```

## Target Architecture — v1.0.0
```text
React Frontend
 ↓
FastAPI Backend
 ↓
Document Storage
 ↓
LlamaIndex RAG Pipeline
 ↓
Vector Index + Neo4j Knowledge Graph
 ↓
LangGraph Workflow
 ↓
Evidence-Based Reliability Recommendation

```

## Main Modules
### Frontend

Responsible for user interaction, document upload, reliability questions, recommendations, evidence display, and graph context visualisation.

### Backend

Responsible for REST APIs, file upload, document management, RAG orchestration, and integration with graph and AI services.

### Graph

Responsible for modelling power electronics reliability knowledge, including components, symptoms, failure modes, evidence, and maintenance actions.

### Documents

Stores example datasheets, reliability notes, test reports, maintenance logs, and technical references used for ingestion.

### Docker

Will contain deployment assets for local and cloud execution.

## Architectural Principles
Keep services modular.
Separate frontend and backend responsibilities.
Store backend dependencies in an isolated virtual environment.
Use explicit APIs between frontend and backend.
Add AI functionality incrementally.
Keep recommendations grounded in evidence.
Preserve traceability between answers and source documents.