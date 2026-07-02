# ADR-001 — Why Neo4j?

## Status

Accepted

---

# Context

The project requires modelling engineering knowledge, failure propagation, evidence, maintenance actions and diagnostic reasoning.

Traditional relational databases are not optimised for traversing complex relationships between interconnected engineering entities.

---

# Decision

Use Neo4j as the primary graph database.

---

# Rationale

Neo4j provides:

- Native property graph model
- Efficient relationship traversal
- Cypher query language
- Excellent GraphRAG compatibility
- Strong ecosystem
- Enterprise adoption

---

# Alternatives Considered

- PostgreSQL
- MySQL
- MongoDB
- RDF triple stores

---

# Consequences

Positive

- Efficient graph traversal
- Explainable reasoning paths
- Excellent AI integration

Negative

- Additional technology to learn
- Separate persistence layer

---

# Related Documents

POWER_ELECTRONICS_GRAPH_SCHEMA.md

KNOWLEDGE_INGESTION_DESIGN.md

---

# Date

2026