# Knowledge Graph Architecture

## Purpose

This document describes the Knowledge Graph architecture of the **Power Electronics Reliability Copilot**.

The Knowledge Graph provides the structured engineering knowledge layer of the system. It represents engineering entities, relationships, evidence links, and reliability concepts in Neo4j so that the platform can support explainable, evidence-backed engineering reasoning.

---

# Overview

The Knowledge Graph complements semantic document retrieval.

Semantic retrieval helps locate relevant document chunks based on similarity, while the Knowledge Graph represents explicit engineering relationships such as:

- components and their failure modes
- degradation mechanisms and symptoms
- tests and diagnostic evidence
- maintenance actions and reliability recommendations
- source documents and evidence traces

Together, semantic retrieval and graph retrieval provide the foundation for GraphRAG-style engineering reasoning.

---

# Design Principles

The Knowledge Graph architecture follows several principles.

## Ontology-first modelling

The graph is based on an explicit engineering ontology rather than arbitrary extracted text.

## Evidence traceability

Graph entities and relationships should remain traceable to source documents and evidence chunks wherever possible.

## Explainability

The graph should support interpretable engineering reasoning paths rather than opaque AI responses.

## Idempotent population

Graph population should use `MERGE`-based updates so that repeated ingestion does not create unnecessary duplicates.

## Modular integration

Knowledge extraction, graph population, graph validation, and graph retrieval are implemented as separate backend services.

---

# High-level Architecture

```text
Engineering Knowledge Documents
              │
              ▼
Document Registration
              │
              ▼
Chunking
              │
              ▼
Knowledge Extraction
              │
              ▼
Graph-ready JSON
              │
              ▼
Neo4j Population Service
              │
              ▼
Neo4j Engineering Knowledge Graph
              │
              ▼
Graph Retrieval Services
              │
              ▼
Evidence-backed AI Reasoning
```

---

# Knowledge Graph Layers

## 1. Ontology Layer

The ontology defines the engineering concepts represented in the graph.

It includes:

- entity categories
- relationship types
- property conventions
- modelling rules
- evidence linkage principles

The ontology is documented separately in the Knowledge Engineering documentation.

---

## 2. Graph Schema Layer

The Neo4j schema implements the ontology using labels, properties, constraints, indexes, and relationship types.

Typical graph concepts include:

- engineering components
- failure modes
- degradation mechanisms
- symptoms
- tests
- maintenance actions
- evidence documents

---

## 3. Population Layer

The population layer takes graph-ready JSON and writes it to Neo4j.

Responsibilities include:

- creating entities
- creating relationships
- applying consistent labels
- preserving properties
- avoiding duplicate nodes
- linking knowledge to evidence where available

Population is handled through a dedicated backend service rather than directly inside API routes.

---

## 4. Validation Layer

The validation layer checks graph quality.

Validation may include:

- duplicate entities
- orphan nodes
- missing evidence links
- missing relationship properties
- graph statistics
- schema consistency

This layer helps ensure that the graph remains reliable as more knowledge is added.

---

## 5. Retrieval Layer

The retrieval layer exposes graph knowledge to the rest of the platform.

Current graph retrieval capabilities include:

- graph summary
- entity lookup
- entity search
- neighbour retrieval
- relationship retrieval
- filtering by relationship type
- filtering by source or target entity
- evidence lookup for graph entities

These services support both direct API access and evidence-backed reasoning workflows.

---

# Entity Model

The graph represents engineering concepts as entities.

Common entity classes include:

| Entity Type | Description |
|------------|-------------|
| Component | Physical or functional engineering component |
| Failure Mode | Observable or classified failure condition |
| Failure Mechanism | Underlying degradation process |
| Symptom | Observable indication of a problem |
| Test Method | Diagnostic or validation method |
| Maintenance Action | Recommended inspection, repair, or mitigation action |
| Material | Material or physical layer involved in reliability behaviour |
| Evidence Document | Source document supporting extracted knowledge |

The model is extensible and can support additional power electronics reliability concepts as the project evolves.

---

# Relationship Model

Relationships capture engineering meaning between entities.

Typical relationships include:

| Relationship | Meaning |
|-------------|---------|
| HAS_FAILURE_MODE | Component may exhibit a failure mode |
| CAUSED_BY | Failure mode or symptom is caused by a mechanism |
| INDICATES | Symptom indicates a failure mode or mechanism |
| TESTED_BY | Entity can be assessed using a test method |
| MITIGATED_BY | Failure or mechanism can be reduced by an action |
| HAS_EVIDENCE | Entity or relationship is supported by evidence |
| RELATED_TO | General engineering association |
| PART_OF | Component or material belongs to a larger system |

Relationship naming should remain consistent, explicit, and engineering meaningful.

---

# Evidence Traceability

Evidence traceability is central to the architecture.

The graph should support links between:

```text
Engineering Entity
        │
        ▼
Relationship
        │
        ▼
Evidence Chunk
        │
        ▼
Source Document
```

This allows the Engineering Copilot to explain not only *what* it recommends, but also *why* the recommendation is supported.

---

# Graph-ready JSON

Knowledge extraction produces graph-ready JSON before Neo4j population.

A typical structure includes:

```json
{
  "entities": [
    {
      "name": "IGBT Module",
      "type": "Component",
      "description": "Power semiconductor module used for switching applications."
    }
  ],
  "relationships": [
    {
      "source": "IGBT Module",
      "relation": "HAS_FAILURE_MODE",
      "target": "Bond Wire Fatigue",
      "description": "IGBT modules may experience bond wire fatigue under thermal cycling."
    }
  ]
}
```

This intermediate representation separates knowledge extraction from graph persistence.

---

# Backend Services

The Knowledge Graph architecture is implemented through dedicated services.

| Service | Responsibility |
|--------|----------------|
| Knowledge Extraction Service | Extracts entities and relationships from text |
| Neo4j Population Service | Writes graph-ready knowledge into Neo4j |
| Graph Validation Service | Checks graph quality and consistency |
| Graph Retrieval Service | Retrieves entities, relationships, neighbours, evidence and summaries |
| Evidence Reasoning Service | Combines graph evidence with semantic evidence |

This separation improves maintainability and testing.

---

# API Layer

Knowledge Graph functionality is exposed through REST APIs.

Current API capabilities include:

```text
GET  /knowledge-graph/summary
GET  /knowledge-graph/entity/{name}
GET  /knowledge-graph/search
GET  /knowledge-graph/entity/{name}/neighbors
GET  /knowledge-graph/relationships
GET  /knowledge-graph/entity/{name}/evidence
POST /knowledge-graph/populate
```

These endpoints allow the graph to be inspected, validated, queried, and used by the reasoning engine.

---

# Role in Evidence-backed Reasoning

The Knowledge Graph provides structured context for the Engineering Copilot.

Example:

```text
Question:
Why does VCE(sat) increase during power cycling?

Semantic retrieval may provide:
- document chunks about junction temperature
- extracted text about bond wire degradation
- reliability study evidence

Graph retrieval may provide:
- IGBT Module → HAS_FAILURE_MODE → Bond Wire Fatigue
- Thermal Cycling → CAUSES → Bond Wire Fatigue
- Bond Wire Fatigue → INDICATES → Increased VCE(sat)
```

The reasoning layer combines both forms of evidence to generate a grounded engineering answer.

---

# Current Implementation Status

| Capability | Status |
|------------|--------|
| Engineering ontology | ✅ Implemented |
| Neo4j integration | ✅ Implemented |
| Graph schema | ✅ Implemented |
| Constraints and indexes | ✅ Implemented |
| Seed graph | ✅ Implemented |
| Knowledge extraction | ✅ Implemented |
| Graph-ready JSON | ✅ Implemented |
| Neo4j population service | ✅ Implemented |
| Graph validation service | ✅ Implemented |
| Graph retrieval service | ✅ Implemented |
| Knowledge Graph REST APIs | ✅ Implemented |
| Evidence-backed reasoning integration | ✅ Implemented |
| Frontend graph visualisation | ⏳ Planned |

---

# Future Enhancements

Planned improvements include:

- richer evidence linking between relationships and source chunks
- improved ontology governance
- graph visualisation in the frontend
- multi-hop reasoning paths
- graph-based ranking of evidence
- integration with conversational Engineering Copilot UI
- future LangGraph orchestration

---

# Related Documents

- `SYSTEM_ARCHITECTURE.md`
- `INGESTION_ARCHITECTURE.md`
- `RETRIEVAL_ARCHITECTURE.md`
- `AI_REASONING_ARCHITECTURE.md`
- `../Knowledge_Engineering/KNOWLEDGE_GRAPH_OVERVIEW.md`
- `../Knowledge_Engineering/ontology/POWER_ELECTRONICS_RELIABILITY_ONTOLOGY.md`
- `../Knowledge_Engineering/ontology/POWER_ELECTRONICS_GRAPH_SCHEMA.md`

---

# Version

Prepared for:

**Power Electronics Reliability Copilot**

Version **v0.5.0 — Evidence-backed Engineering Copilot**