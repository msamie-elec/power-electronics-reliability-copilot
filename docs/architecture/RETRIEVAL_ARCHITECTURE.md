# Retrieval Architecture

## Purpose

This document describes the retrieval architecture implemented by the **Power Electronics Reliability Copilot**.

The retrieval layer is responsible for locating the most relevant engineering evidence from both unstructured engineering documents and the structured Engineering Knowledge Graph.

Rather than relying on a single retrieval technique, the platform adopts a **hybrid retrieval architecture** that combines semantic similarity search with graph-based knowledge retrieval to support evidence-backed engineering reasoning.

---

# Overview

The retrieval layer acts as the bridge between engineering knowledge storage and AI reasoning.

Its responsibilities include:

- retrieving relevant engineering document chunks
- exploring related engineering concepts within the Knowledge Graph
- assembling a structured reasoning context
- providing traceable evidence to the Engineering Copilot

This architecture ensures that every engineering response is grounded in retrieved evidence rather than relying solely on Large Language Model (LLM) knowledge.

---

# Design Principles

The retrieval architecture is based on the following principles.

### Evidence-first

Engineering recommendations should always be supported by retrieved evidence.

### Explainability

Every engineering conclusion should be traceable to source documents and Knowledge Graph relationships.

### Separation of Concerns

Document retrieval and graph retrieval remain independent services that can evolve separately.

### Extensibility

Additional retrieval mechanisms (for example BM25, Azure AI Search or graph embeddings) can be incorporated without redesigning the overall architecture.

---

# Retrieval Architecture

The current retrieval workflow is shown below.

```text
Engineering Question
          │
          ▼
Question Processing
          │
          ▼
 ┌────────┴─────────┐
 ▼                  ▼
Semantic Search   Graph Search
 (FAISS)            (Neo4j)
 ▼                  ▼
Relevant Chunks   Related Entities
 ▼                  ▼
Evidence Aggregation
          │
          ▼
Reasoning Context
          │
          ▼
Engineering Copilot
```

The retrieval layer combines complementary forms of engineering evidence before passing them to the reasoning engine.

---

# Retrieval Components

## Semantic Retrieval

Semantic retrieval identifies engineering document chunks that are conceptually similar to the user's question.

Current implementation:

- OpenAI embeddings
- FAISS vector index
- cosine similarity search
- configurable Top-K retrieval

Typical outputs include:

- engineering explanations
- technical procedures
- degradation mechanisms
- experimental observations

Semantic retrieval is particularly effective for natural language engineering questions.

---

## Knowledge Graph Retrieval

Knowledge Graph retrieval explores structured engineering knowledge stored within Neo4j.

Current implementation includes:

- entity lookup
- neighbouring entities
- relationship exploration
- evidence lookup
- graph summary
- graph traversal APIs

Graph retrieval captures relationships that are difficult to identify through semantic similarity alone.

Examples include:

- component dependencies
- failure propagation
- degradation mechanisms
- maintenance relationships

---

## Evidence Aggregation

The retrieval layer combines outputs from both retrieval mechanisms.

Inputs:

- semantic evidence
- graph entities
- graph relationships

Outputs:

- unified reasoning context
- supporting engineering evidence
- graph reasoning information

This aggregated context is passed directly to the AI reasoning layer.

---

# Current Retrieval Workflow

The current backend performs retrieval in the following sequence.

```text
Engineering Question
          │
          ▼
Semantic Retrieval
          │
          ▼
Retrieve Top-K Chunks
          │
          ▼
Knowledge Graph Retrieval
          │
          ▼
Retrieve Related Entities
          │
          ▼
Retrieve Relationships
          │
          ▼
Build Reasoning Context
          │
          ▼
Engineering Copilot
```

Each stage remains independently testable and reusable.

---

# Current Implementation

Version **0.5** currently provides:

## Semantic Retrieval

- document embeddings
- FAISS indexing
- semantic similarity search
- configurable retrieval depth

## Knowledge Graph Retrieval

- EngineeringEntity lookup
- neighbour retrieval
- relationship retrieval
- entity evidence retrieval
- graph summary service

## Reasoning Context

- semantic evidence collection
- graph evidence collection
- evidence aggregation
- structured reasoning context generation

---

# Future Evolution

The retrieval layer has been designed for incremental enhancement.

Planned improvements include:

## BM25 Hybrid Retrieval

Introduce keyword-based retrieval to complement semantic search.

Benefits include improved retrieval of:

- engineering symbols
- component identifiers
- standards
- equations
- numerical values
- part numbers

---

## Retrieval Ranking

Introduce evidence ranking based on:

- semantic similarity
- graph connectivity
- engineering importance
- evidence confidence

---

## Graph Traversal

Support multi-hop engineering reasoning through:

- degradation chains
- causal relationships
- maintenance workflows
- diagnostic pathways

---

## Cloud Search

Future versions may replace or extend FAISS with Azure AI Search to support:

- larger engineering document collections
- enterprise scalability
- cloud-native indexing

---

# Relationship to Other Architectures

This document focuses solely on retrieving engineering evidence.

It works together with the other architecture documents as follows:

- **System Architecture** describes the complete platform.
- **Ingestion Architecture** explains how engineering knowledge enters the platform.
- **Knowledge Graph Architecture** explains how engineering knowledge is modelled and stored.
- **AI Reasoning Architecture** explains how retrieved evidence is transformed into engineering recommendations.
- **Frontend Architecture** explains how engineers interact with the retrieval services.

Together these documents describe the complete engineering workflow from document ingestion to evidence-backed AI reasoning.

---

# Version

Prepared for:

**Power Electronics Reliability Copilot**

Version **v0.5.0 — Evidence-backed Engineering Copilot**