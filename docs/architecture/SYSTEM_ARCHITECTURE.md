# System Architecture

## Overview

Power Electronics Reliability Copilot is a modular AI-powered engineering decision-support platform that combines document intelligence, semantic retrieval, structured engineering knowledge, and evidence-backed AI reasoning.

The platform is organised as a collection of loosely coupled services that together support the complete engineering workflow from document ingestion to explainable AI-assisted recommendations.

Each architectural layer has a clearly defined responsibility, enabling the platform to evolve incrementally while maintaining maintainability, extensibility, and testability.

---

# High-Level Architecture

```text
                 Engineering Documents
                         │
                         ▼
              Document Registration
                         │
                         ▼
               Document Processing
                         │
                         ▼
                   Chunk Generation
                         │
                         ▼
                 Embedding Generation
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      FAISS Vector Store      Knowledge Extraction
              │                     │
              │                     ▼
              │            Graph-ready JSON
              │                     │
              │                     ▼
              │              Neo4j Knowledge Graph
              │                     │
              └──────────┬──────────┘
                         ▼
                 Hybrid Retrieval Layer
                         │
                         ▼
           Evidence-backed AI Reasoning
                         │
                         ▼
              Engineering Copilot API
                         │
                         ▼
                React User Interface
```

---

# Architectural Layers

## 1. Presentation Layer

Responsible for user interaction.

Current responsibilities include:

- document upload
- document management
- engineering dashboard

Future versions will also provide:

- conversational engineering interface
- evidence visualisation
- knowledge graph exploration

Technology:

- React
- TypeScript
- Vite

---

## 2. API Layer

Responsible for exposing backend functionality through REST APIs.

Responsibilities include:

- request validation
- response formatting
- endpoint routing
- OpenAPI documentation

Technology:

- FastAPI

---

## 3. Service Layer

Implements the application's business logic.

Current services include:

- document services
- retrieval services
- graph services
- evidence reasoning services
- Engineering Copilot services

Each service follows the single-responsibility principle.

---

## 4. Knowledge Processing Layer

Transforms engineering documents into machine-readable knowledge.

Components include:

- document parsing
- chunk generation
- embedding generation
- engineering knowledge extraction

Outputs are consumed by both the vector store and the knowledge graph.

---

## 5. Knowledge Layer

Stores engineering knowledge in complementary forms.

### Semantic Knowledge

Stored within FAISS.

Purpose:

- semantic similarity retrieval

### Structured Knowledge

Stored within Neo4j.

Purpose:

- engineering entities
- engineering relationships
- evidence traceability

---

## 6. Reasoning Layer

Combines retrieved evidence into a unified reasoning context.

Responsibilities include:

- semantic retrieval
- graph retrieval
- evidence ranking
- reasoning context construction
- prompt generation
- engineering answer generation

---

## 7. AI Layer

Uses Large Language Models to generate engineering responses based exclusively on retrieved evidence.

Current implementation:

- OpenAI GPT-4.1

Future versions may support additional providers.

---

# Engineering Workflow

```text
Upload Document

↓

Register Document

↓

Parse Document

↓

Chunk Document

↓

Generate Embeddings

↓

Extract Engineering Knowledge

↓

Populate Knowledge Graph

↓

Retrieve Semantic Evidence

↓

Retrieve Graph Evidence

↓

Build Reasoning Context

↓

Generate Engineering Response
```

---

# Architectural Principles

The architecture follows several core principles.

## Modularity

Each component performs one primary function.

---

## Separation of Responsibilities

Processing, retrieval, reasoning, and presentation remain independent.

---

## Evidence-first AI

The language model reasons over retrieved evidence rather than raw documents.

---

## Explainability

Responses should be traceable to both document evidence and graph relationships.

---

## Extensibility

New retrieval engines, graph technologies, AI providers, and frontend capabilities should be introducible with minimal architectural disruption.

---

# Current Status

The platform currently provides:

- engineering document processing
- semantic retrieval
- engineering knowledge graph
- hybrid retrieval
- evidence-backed reasoning
- Engineering Copilot backend

The next architectural milestone is the conversational Engineering Copilot interface planned for Version 0.5.1.

---

# Related Architecture Documents

This document provides the system-level view.

More detailed information is available in:

- `INGESTION_ARCHITECTURE.md`
- `KNOWLEDGE_GRAPH_ARCHITECTURE.md`
- `RETRIEVAL_ARCHITECTURE.md`
- `AI_REASONING_ARCHITECTURE.md`