# Ingestion Architecture

## Overview

The Power Electronics Reliability Copilot uses two independent document ingestion pipelines designed to support different engineering objectives.

Although both pipelines begin with engineering documents, they serve fundamentally different purposes:

- **Investigation Document Pipeline** – processes user-uploaded documents for a specific engineering investigation.
- **Engineering Knowledge Pipeline** – processes trusted engineering references to build and continuously enrich the permanent Engineering Knowledge Graph.

This separation follows enterprise AI design principles by distinguishing temporary investigation evidence from curated engineering knowledge.

---

# Why Two Ingestion Pipelines?

Engineering documents do not all have the same role within the platform.

Some documents are uploaded by engineers to investigate a particular problem. Others represent trusted engineering knowledge that should become part of the platform's long-term knowledge base.

Keeping these responsibilities separate provides several advantages.

| Investigation Pipeline | Engineering Knowledge Pipeline |
|-------------------------|-------------------------------|
| Temporary investigation evidence | Permanent engineering knowledge |
| Supports one engineering investigation | Supports all future investigations |
| Fast processing | Higher-quality processing |
| Does not modify the Knowledge Graph | Updates the Knowledge Graph |
| User-uploaded documents | Curated engineering references |
| Optimised for responsiveness | Optimised for knowledge quality |

This separation improves:

- scalability
- maintainability
- explainability
- security
- operational efficiency
- knowledge quality

---

# Pipeline 1 — Investigation Document Pipeline

## Purpose

The Investigation Document Pipeline processes engineering documents uploaded by users during day-to-day engineering investigations.

Typical documents include:

- inspection reports
- maintenance reports
- fault logs
- laboratory measurements
- customer documentation
- project-specific engineering documents
- reliability investigation reports

These documents provide contextual information for answering engineering questions but **do not automatically modify the trusted Engineering Knowledge Graph**.

---

## Current Processing Workflow

```text
Investigation Document
          │
          ▼
Document Registration
          │
          ▼
Document Chunking
          │
          ▼
Embedding Generation
          │
          ▼
FAISS Semantic Retrieval
(Current)
          │
          ▼
Retrieved Evidence
          │
          ▼
Engineering Copilot
```

---

## Planned Retrieval Enhancement

Future releases will extend the retrieval workflow by introducing BM25 keyword retrieval.

```text
User Question
       │
       ▼
 BM25 Retrieval
       +
 FAISS Retrieval
       │
       ▼
 Merge & Rank
       │
       ▼
 Retrieved Evidence
       │
       ▼
 Engineering Copilot
```

The hybrid retrieval strategy improves retrieval of:

- technical terminology
- engineering symbols
- numerical values
- standards
- equations
- manufacturer part numbers
- exact engineering phrases

**Note**

At the current implementation stage, the Investigation Pipeline uses **FAISS semantic retrieval**. BM25 integration is planned for a future release.

---

## Output

The Investigation Pipeline produces:

- registered documents
- metadata
- document chunks
- embeddings
- temporary retrieval context

The generated information is used only for the current engineering investigation.

---

# Pipeline 2 — Engineering Knowledge Pipeline

## Purpose

The Engineering Knowledge Pipeline processes trusted engineering references that contribute to the permanent Engineering Knowledge Graph.

Typical sources include:

- manufacturer application notes
- reliability handbooks
- peer-reviewed journal papers
- technical standards
- approved internal engineering documentation
- maintenance procedures
- engineering design guides

Only curated and approved engineering documents should enter this pipeline.

---

## Current Processing Workflow

```text
Engineering Knowledge Document
               │
               ▼
Document Registration
               │
               ▼
Document Chunking
               │
               ▼
Embedding Generation
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
Engineering Knowledge Graph
               │
               ▼
Knowledge Graph Retrieval
               │
               ▼
Evidence-backed AI Reasoning
```

---

## Output

The Engineering Knowledge Pipeline produces:

- engineering entities
- engineering relationships
- graph-ready knowledge
- document evidence
- evidence traceability
- Engineering Knowledge Graph updates

Unlike the Investigation Pipeline, this pipeline continuously enriches the platform's permanent engineering knowledge.

---

# Retrieval Architecture

The retrieval strategy differs for each pipeline.

## Investigation Pipeline

Current implementation:

- FAISS semantic retrieval

Planned enhancement:

- BM25 keyword retrieval
- FAISS semantic retrieval
- Hybrid ranking

The retrieved evidence supports a single engineering investigation.

---

## Engineering Knowledge Pipeline

Current implementation combines:

- FAISS semantic retrieval
- Neo4j Knowledge Graph retrieval
- Engineering entity exploration
- Relationship retrieval
- Evidence retrieval

The retrieved evidence supports explainable engineering reasoning.

---

# Why Hybrid Retrieval?

Engineering documentation contains both semantic knowledge and exact technical terminology.

Semantic embeddings alone may not reliably retrieve:

- VCE(sat)
- ΔTj
- RthJC
- IEC 60747
- thermal cycling
- bond wire lift-off
- manufacturer part numbers
- numerical limits
- engineering units

Future BM25 integration will complement semantic retrieval by preserving exact engineering terminology while FAISS captures semantic similarity.

---

# Physical Storage Layout

The platform stores investigation documents and curated engineering knowledge separately.

```text
backend/

uploads/
    Investigation documents

knowledge_base/
    Curated engineering references

chunks/
    investigation/
    knowledge/

embeddings/
    investigation/
    knowledge/

metadata/
    investigation/
    knowledge/

graph/
    Neo4j resources
```

---

## Investigation Documents

Location

```text
backend/uploads/
```

Purpose

- Uploaded by end users
- Temporary engineering investigations
- Supports semantic retrieval
- Does not update the Knowledge Graph

---

## Engineering Knowledge Base

Location

```text
backend/knowledge_base/
```

Purpose

- Curated engineering references
- Trusted knowledge sources
- Supports knowledge extraction
- Populates the Engineering Knowledge Graph
- Enables evidence-backed reasoning

---

# Processing Cost

The two pipelines have different computational characteristics.

## Investigation Pipeline

Optimised for responsiveness.

Typical processing includes:

- parsing
- chunking
- embedding generation
- FAISS retrieval

This pipeline is expected to process the majority of uploaded documents.

---

## Engineering Knowledge Pipeline

Optimised for knowledge quality.

Additional processing includes:

- LLM-assisted knowledge extraction
- entity extraction
- relationship extraction
- graph population
- evidence linking
- graph validation

This pipeline executes less frequently but performs significantly more processing.

---

# Orchestration

Currently, the two pipelines are initiated independently depending on the document source.

Future versions will introduce automatic document routing.

```text
Document Upload
        │
        ▼
Document Classification
        │
 ┌──────┴──────┐
 ▼             ▼
Investigation   Engineering Knowledge
Document        Document
 ▼             ▼
Pipeline 1     Pipeline 2
```

Future orchestration may be implemented using LangGraph.

---

# Current Implementation Status

| Capability | Status |
|------------|--------|
| Document Registration | ✅ Implemented |
| Document Chunking | ✅ Implemented |
| Embedding Generation | ✅ Implemented |
| FAISS Retrieval | ✅ Implemented |
| Knowledge Extraction | ✅ Implemented |
| Graph-ready JSON | ✅ Implemented |
| Neo4j Population | ✅ Implemented |
| Knowledge Graph Retrieval | ✅ Implemented |
| Evidence-backed AI Reasoning | ✅ Implemented |
| Investigation BM25 Retrieval | ⏳ Planned |
| Automatic Pipeline Routing | ⏳ Planned |

---

# Architectural Benefits

This architecture provides:

- clear separation of responsibilities
- reusable processing services
- lower operational cost
- explainable AI reasoning
- scalable knowledge acquisition
- trusted Knowledge Graph updates
- modular software architecture
- enterprise-grade maintainability
- future extensibility

---

# Implementation Notes

The document ingestion pipeline introduced in Version 0.3 forms the foundation of both ingestion pipelines.

Version 0.5 extends this capability by introducing:

- engineering knowledge extraction
- graph-ready JSON generation
- Neo4j population
- Knowledge Graph retrieval
- evidence-backed reasoning

Rather than replacing the original ingestion workflow, Version 0.5 builds upon it through modular extensions.

---

# Related Architecture Documents

This document focuses on document ingestion.

Related architecture documents include:

- `SYSTEM_ARCHITECTURE.md`
- `KNOWLEDGE_GRAPH_ARCHITECTURE.md`
- `RETRIEVAL_ARCHITECTURE.md`
- `AI_REASONING_ARCHITECTURE.md`

---

# Version

**Power Electronics Reliability Copilot**

Prepared for **Version 0.5.0 — Evidence-backed Engineering Copilot**