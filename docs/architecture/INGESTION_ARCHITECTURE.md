# Ingestion Architecture

## Purpose

This document describes the ingestion architecture adopted by the Power Electronics Reliability Copilot.

The project intentionally separates document ingestion into two independent pipelines because they serve different business objectives and have different processing requirements.

This architecture follows enterprise AI design principles by separating document retrieval from knowledge acquisition.

---

# Why Two Ingestion Pipelines?

Although both pipelines begin with engineering documents, they have different purposes.

The first pipeline supports day-to-day engineering assistance.

The second pipeline continuously builds and enriches the engineering knowledge base.

Keeping these responsibilities separate improves:

- scalability
- maintainability
- explainability
- security
- operational cost
- knowledge quality

---

# Pipeline 1 — User Document Pipeline

## Purpose

This pipeline processes documents uploaded by end users during normal system usage.

Examples include:

- inspection reports
- maintenance reports
- fault logs
- test reports
- customer documentation
- laboratory measurements
- project-specific engineering documents

These documents are treated as temporary working documents.

They provide contextual information for answering the current engineering question but do **not** automatically modify the trusted engineering knowledge graph.

---

## Processing Flow

```
User Upload
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
Hybrid Document Retrieval
(BM25 + Vector Search)
      │
      ▼
Retrieved Chunks
      │
      ▼
Engineering Answer
```

---

## Output

This pipeline produces:

- registered documents
- document metadata
- chunks
- embeddings
- temporary retrieval context

The resulting information is used only for the current engineering session.

---

# Pipeline 2 — Evidence Knowledge Pipeline

## Purpose

This pipeline processes trusted engineering references that contribute to the permanent engineering knowledge base.

Examples include:

- manufacturer application notes
- reliability handbooks
- peer-reviewed journal papers
- technical standards
- approved internal engineering documents
- maintenance procedures

Only approved documents should enter this pipeline.

---

## Processing Flow

```
Approved Engineering Document
          │
          ▼
Document Registration
          │
          ▼
Chunking
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
Neo4j Knowledge Graph
          │
          ▼
Evidence Links
```

---

## Output

This pipeline produces:

- graph entities
- graph relationships
- document evidence
- traceable engineering knowledge

Unlike the User Document Pipeline, this pipeline continuously enriches the enterprise knowledge graph.

---

# Retrieval Architecture

The retrieval strategy also differs.

## User Document Pipeline

Retrieval combines:

- BM25 keyword search
- Vector similarity search (FAISS)

The retrieved chunks are merged and supplied to the Large Language Model.

---

## Evidence Knowledge Pipeline

Retrieval combines:

- BM25 keyword search
- Vector similarity search
- Neo4j graph traversal

This provides explainable engineering reasoning supported by structured knowledge and trusted evidence.

---

# Why BM25?

Engineering documents contain many exact identifiers that semantic embeddings alone may not retrieve reliably.

Examples include:

- VCE(sat)
- ΔTj
- RthJC
- IEC 60747
- thermal cycling
- bond wire lift-off
- part numbers
- numerical limits
- engineering units

BM25 complements semantic retrieval by preserving exact technical terminology.

---

# Cost Considerations

The two pipelines have different computational costs.

## User Document Pipeline

Optimised for responsiveness.

Typical processing includes:

- parsing
- chunking
- embeddings
- BM25
- FAISS retrieval

This pipeline is expected to process the majority of uploaded documents.

---

## Evidence Knowledge Pipeline

Optimised for knowledge quality rather than speed.

Additional processing includes:

- LLM-assisted entity extraction
- relationship extraction
- graph population
- evidence linking
- graph validation

Since this pipeline updates the enterprise knowledge graph, it is expected to be executed less frequently and only on trusted documents.

---

# Orchestration

The user should not choose which pipeline to use.

Instead, an orchestration layer will route documents automatically.

```
Document Upload
        │
        ▼
Document Type
        │
        ├───────────────┐
        ▼               ▼
User Document     Approved Evidence
        │               │
        ▼               ▼
Pipeline 1       Pipeline 2
```

Future versions may implement this orchestration using LangGraph.

---

# Architectural Benefits

This design provides:

- separation of concerns
- reusable processing components
- lower operational cost
- explainable AI
- scalable knowledge acquisition
- trusted knowledge graph updates
- enterprise-grade maintainability

---

# Implementation Notes

The existing document ingestion pipeline developed in Version 0.3 should be reused wherever possible.

Version 0.5 extends this capability by introducing document registration, evidence tracking and knowledge graph integration rather than replacing the existing implementation.

---

# Future Work

The following enhancement has been identified.

## Hybrid Retrieval for User Documents

The original Version 0.3 retrieval pipeline relied primarily on semantic vector search.

This should be upgraded to include **BM25 keyword retrieval** alongside FAISS semantic retrieval.

Target architecture:

```
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
 Retrieved Chunks
       │
       ▼
 Large Language Model
```

This enhancement will improve retrieval of:

- technical terminology
- engineering symbols
- numerical values
- standards
- equations
- part numbers
- exact phrases

---

# Version

Prepared for:

**Power Electronics Reliability Copilot**

Version **v0.5 – Evidence-Centred GraphRAG**

## Updates:
## Physical Storage Layout

The system stores user investigation documents and approved engineering
knowledge separately.

### Investigation Documents

Location:

backend/uploads/

Purpose:

- Uploaded by end users
- Temporary investigation evidence
- Used for semantic retrieval (BM25 + FAISS)
- Not automatically added to the Knowledge Graph

### Engineering Knowledge Base

Location:

backend/knowledge_base/

Purpose:

- Curated engineering references
- Approved by administrators
- Used for Knowledge Extraction
- Populates the Neo4j Knowledge Graph
- Supports GraphRAG reasoning

Generated artefacts are stored separately:

backend/chunks/investigation/
backend/chunks/knowledge/

backend/embeddings/investigation/
backend/embeddings/knowledge/