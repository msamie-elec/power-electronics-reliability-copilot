# ADR-004 — Evidence-First Knowledge Graph

## Status

Accepted

---

# Context

Enterprise AI systems must provide trustworthy and explainable answers.

Engineering knowledge should always be traceable to its source.

---

# Decision

Every engineering relationship introduced through document ingestion must be linked to supporting document evidence.

Seed data may be used during development, but production knowledge must always be evidence-backed.

---

# Rationale

This supports:

- Explainability
- Traceability
- Auditability
- GraphRAG
- Responsible AI

---

# Consequences

The ingestion pipeline becomes slightly more complex, but the resulting knowledge graph is significantly more trustworthy and suitable for enterprise use.