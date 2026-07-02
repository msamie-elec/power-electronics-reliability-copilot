# Chunking Strategy

## Purpose

This document defines the document chunking strategy for the Power Electronics Reliability Copilot.

Chunking is the process of dividing engineering documents into smaller, semantically meaningful sections before generating vector embeddings.

The objective is to maximise retrieval quality while preserving engineering context.

---

# Why Chunk Documents?

Large Language Models cannot efficiently retrieve information from entire documents.

Instead, documents are divided into smaller chunks that can be:

- embedded independently
- indexed efficiently
- retrieved semantically
- linked to engineering concepts

Each chunk becomes an individual unit of knowledge.

---

# Design Principles

The chunking strategy follows these principles:

- preserve engineering meaning
- avoid splitting technical explanations unnecessarily
- maintain traceability to the original document
- support future GraphRAG workflows
- minimise duplicated information
- produce chunks suitable for vector embeddings

---

# Preferred Chunk Boundaries

Chunks should be created at natural document boundaries whenever possible.

Examples include:

- section
- subsection
- paragraph
- engineering procedure
- failure analysis
- maintenance instruction
- inspection method
- design recommendation

Splitting should avoid breaking equations, tables or engineering reasoning.

---

# Chunk Metadata

Each chunk should contain metadata describing its origin.

Planned metadata includes:

| Field | Description |
|--------|-------------|
| chunkId | Unique chunk identifier |
| documentId | Source document identifier |
| sourceDocument | Original document name |
| section | Section heading |
| page | Page number (if available) |
| chunkIndex | Position within the document |
| text | Chunk content |

This metadata ensures complete traceability back to the original engineering source.

---

# Chunk Size

The exact chunk size will be determined during implementation.

General guidelines are:

- preserve complete engineering concepts
- avoid excessively small chunks
- avoid overly large chunks that dilute semantic meaning

The strategy may later be refined through experimentation and evaluation.

---

# Chunk Overlap

Neighbouring chunks may share a small overlap.

Benefits include:

- preserving context across boundaries
- improving semantic retrieval
- reducing information loss

The overlap size will be defined during implementation.

---

# Relationship to the Knowledge Graph

Document chunks do not replace the knowledge graph.

Instead, chunks complement it.

During ingestion, relevant chunks may be linked to engineering concepts such as:

- Component
- SubComponent
- Material
- OperatingCondition
- StressFactor
- FailureMechanism
- FailureMode
- Symptom
- TestMethod
- MaintenanceAction

These links enable hybrid retrieval using both graph traversal and semantic search.

---

# Chunk Lifecycle

```
Engineering Document
        │
        ▼
Document Loader
        │
        ▼
Chunk Creation
        │
        ▼
Metadata Assignment
        │
        ▼
Embedding Generation
        │
        ▼
Vector Store
        │
        ▼
Graph Linking
```

---

# Future Improvements

Future versions may introduce:

- adaptive chunking
- semantic chunking
- table-aware chunking
- figure-aware chunking
- OCR-aware chunking
- multilingual chunking

These enhancements can improve retrieval performance without changing the overall architecture.

---

# Version

Prepared for:

**Power Electronics Reliability Copilot**

Version **0.5 – GraphRAG Integration Preparation**