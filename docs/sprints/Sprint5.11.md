# Sprint 5.11:
Sprint 5.11 — Evidence-backed AI Reasoning.

First capability to implement:

Hybrid Retrieval Context Builder

It should collect:

User question
    ↓
FAISS / semantic evidence
    +
Neo4j graph evidence
    +
future BM25 evidence
    ↓
structured reasoning context


# Also note:
Frozen Architecture Decision 1 — Two Independent Ingestion Pipelines

The project has two ingestion pipelines, each serving a different purpose.

Pipeline 1 — Investigation (User Upload)

Purpose:

User uploads documents during an investigation.
Documents are temporary.
They provide context for answering the current engineering question.
They do not modify the engineering knowledge graph.

Typical flow:

Upload
    ↓
Registration
    ↓
Chunking
    ↓
Embeddings
    ↓
BM25 + FAISS
    ↓
Retrieved Context
    ↓
LLM

Output:

temporary chunks
embeddings
retrieval context
Pipeline 2 — Knowledge Acquisition (Evidence)

Purpose:

Approved engineering references
Permanent engineering knowledge
Builds Neo4j

Flow:

Approved Evidence
       ↓
Registration
       ↓
Chunking
       ↓
Embeddings
       ↓
Knowledge Extraction
       ↓
Graph JSON
       ↓
Neo4j
       ↓
Evidence Links

Output:

graph entities
graph relationships
evidence traceability

This separation is one of the strongest architectural decisions in the project. It is how many enterprise AI systems distinguish operational data from trusted knowledge.

Frozen Architecture Decision 2 — Pipeline 1 still needs BM25

This is an important implementation gap.

According to your design:

Pipeline 1 should be

Upload
    ↓
Chunking
    ↓
Embeddings
    ↓
BM25 Index
    ↓
FAISS Index
    ↓
Hybrid Retrieval

Current implementation (v0.3 legacy):

Upload
    ↓
Chunking
    ↓
Embeddings
    ↓
FAISS

So BM25 is currently missing from the user-document ingestion pipeline.

That means user-uploaded documents are retrieved only semantically, without exact keyword matching for engineering identifiers (e.g. VCE(sat), IEC 60747, part numbers, symbols). This is precisely the gap your architecture document identifies.

Where this fits in the roadmap

I would record it as technical debt, not as a defect.

Area	Status
Investigation Pipeline	✅ Exists
Evidence Pipeline	✅ Exists
Neo4j	✅ Exists
Graph Retrieval	✅ Exists
Graph Validation	✅ Exists
Automated Tests	✅ Exists
BM25 for Investigation Pipeline	⏳ Planned
Hybrid Investigation Retrieval (BM25 + FAISS)	⏳ Planned