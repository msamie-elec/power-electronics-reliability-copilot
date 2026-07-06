# Knowledge Graph Overview

## Purpose

This document provides a high-level overview of the Knowledge Engineering subsystem within the **Power Electronics Reliability Copilot**.

The Knowledge Graph is a core component of the platform's evidence-backed AI architecture. It transforms engineering knowledge extracted from technical documents into structured, interconnected information that supports explainable reasoning, engineering diagnostics, and intelligent retrieval.

Rather than replacing semantic document retrieval, the Knowledge Graph complements it by representing explicit engineering relationships that cannot be inferred reliably through vector similarity alone.

This document serves as the entry point for all Knowledge Engineering documentation.

---

# Why Knowledge Engineering?

Engineering knowledge is highly interconnected.

A reliability engineer rarely investigates isolated facts. Instead, engineering decisions require understanding relationships between:

- components
- materials
- operating conditions
- degradation mechanisms
- failure modes
- symptoms
- diagnostic tests
- maintenance actions
- supporting evidence

Traditional document retrieval provides relevant text passages but does not explicitly model these relationships.

The Knowledge Graph addresses this limitation by organising engineering knowledge into a structured graph that can be queried, traversed, and combined with semantic retrieval.

---

# Knowledge Engineering within the System

The Knowledge Graph forms the structured knowledge layer of the overall platform.

```text
Engineering Documents
          │
          ▼
Document Processing
          │
          ▼
Knowledge Extraction
          │
          ▼
Graph-ready JSON
          │
          ▼
Neo4j Knowledge Graph
          │
          ▼
Knowledge Graph Retrieval
          │
          ▼
Evidence-backed AI Reasoning
```

Semantic retrieval and graph retrieval work together to provide reliable engineering evidence for the AI reasoning layer.

---

# Knowledge Engineering Workflow

The Knowledge Engineering subsystem follows a staged workflow.

```text
Engineering Documents
          │
          ▼
Knowledge Extraction
          │
          ▼
Graph-ready JSON
          │
          ▼
Neo4j Population
          │
          ▼
Graph Validation
          │
          ▼
Knowledge Graph Retrieval
          │
          ▼
Evidence-backed AI Reasoning
```

Each stage has a clearly defined responsibility and is implemented as an independent backend component.

---

# Knowledge Engineering Components

The subsystem consists of several complementary components.

## Engineering Ontology

Defines the engineering concepts represented within the platform.

Examples include:

- components
- materials
- degradation mechanisms
- failure modes
- symptoms
- diagnostic methods
- maintenance actions

The ontology provides a common vocabulary for knowledge extraction and graph modelling.

---

## Graph Schema

The graph schema translates the ontology into an implementation within Neo4j.

It defines:

- node labels
- relationship types
- properties
- constraints
- indexes

The schema ensures that engineering knowledge is represented consistently across the platform.

---

## Knowledge Extraction

Knowledge extraction converts engineering documents into structured engineering knowledge.

Large Language Models identify:

- engineering entities
- engineering relationships
- supporting descriptions

The extracted information is converted into graph-ready JSON before population into Neo4j.

---

## Knowledge Graph Population

The population layer imports extracted knowledge into Neo4j.

Responsibilities include:

- creating entities
- creating relationships
- preserving engineering properties
- preventing duplicate nodes through MERGE operations

This process allows the graph to grow incrementally as new engineering knowledge becomes available.

---

## Graph Validation

Validation ensures that the Knowledge Graph remains consistent and reliable.

Typical validation activities include:

- duplicate detection
- orphan node identification
- relationship validation
- graph statistics
- schema consistency checks

---

## Knowledge Graph Retrieval

The graph retrieval layer exposes engineering knowledge through REST APIs.

Current capabilities include:

- graph summary
- entity lookup
- relationship retrieval
- neighbour exploration
- engineering evidence lookup

These services support both manual graph exploration and AI reasoning.

---

## Evidence-backed AI Reasoning

The Knowledge Graph provides structured context for the Engineering Copilot.

Rather than relying solely on semantic similarity, the reasoning engine combines:

- retrieved document evidence
- graph entities
- graph relationships
- engineering reasoning rules

This enables more transparent and explainable engineering responses.

---

# Relationship to the Overall Architecture

Within the complete system architecture, the Knowledge Graph operates alongside semantic retrieval.

```text
Engineering Documents
          │
          ▼
Document Processing
          │
    ┌─────┴─────┐
    ▼           ▼
FAISS       Neo4j Knowledge Graph
(Vector)     (Structured Knowledge)
    │           │
    └─────┬─────┘
          ▼
Hybrid Retrieval
          │
          ▼
Evidence-backed AI Reasoning
          │
          ▼
Engineering Copilot
```

This hybrid architecture combines the strengths of vector search and graph-based reasoning.

---

# Documentation Map

The Knowledge Engineering documentation is organised into dedicated documents, each with a single responsibility.

| Document | Purpose |
|----------|---------|
| **KNOWLEDGE_GRAPH_OVERVIEW.md** | Introduction to the Knowledge Engineering subsystem |
| **KNOWLEDGE_GRAPH_ARCHITECTURE.md** | Architecture of the Knowledge Graph services and components |
| **POWER_ELECTRONICS_RELIABILITY_ONTOLOGY.md** | Engineering ontology and modelling concepts |
| **POWER_ELECTRONICS_GRAPH_SCHEMA.md** | Neo4j graph schema, labels, relationships, and constraints |
| **KNOWLEDGE_INGESTION_DESIGN.md** | Knowledge extraction and graph population workflow |
| **ONTOLOGY_DESIGN_GUIDE.md** | Principles and guidelines for ontology development |

This structure separates high-level concepts from implementation details and helps keep the documentation maintainable.

---

# Current Implementation Status

The current implementation includes:

- ✅ Engineering ontology
- ✅ Graph schema
- ✅ Knowledge extraction
- ✅ Graph-ready JSON generation
- ✅ Neo4j population service
- ✅ Graph validation
- ✅ Knowledge Graph retrieval APIs
- ✅ Evidence-backed AI reasoning integration

These capabilities establish the Knowledge Engineering foundation for the Engineering Copilot.

---

# Future Evolution

The Knowledge Graph will continue to evolve alongside the platform.

Planned enhancements include:

- richer engineering ontologies
- expanded evidence linking
- multi-hop graph reasoning
- graph visualisation within the frontend
- tighter integration with conversational AI
- advanced GraphRAG workflows
- agent-assisted knowledge refinement

The modular design allows these capabilities to be introduced incrementally while maintaining compatibility with the existing architecture.

---

# Related Documents

### Architecture

- `../architecture/SYSTEM_ARCHITECTURE.md`
- `../architecture/KNOWLEDGE_GRAPH_ARCHITECTURE.md`
- `../architecture/INGESTION_ARCHITECTURE.md`
- `../architecture/RETRIEVAL_ARCHITECTURE.md`
- `../architecture/AI_REASONING_ARCHITECTURE.md`

### Knowledge Engineering

- `ontology/POWER_ELECTRONICS_RELIABILITY_ONTOLOGY.md`
- `ontology/POWER_ELECTRONICS_GRAPH_SCHEMA.md`
- `ontology/references/KNOWLEDGE_INGESTION_DESIGN.md`
- `ontology/guides/ONTOLOGY_DESIGN_GUIDE.md`

---

# Version

Prepared for:

**Power Electronics Reliability Copilot**

Version **v0.5.0 — Evidence-backed Engineering Copilot**