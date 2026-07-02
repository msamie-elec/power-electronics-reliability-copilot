# ADR-002 — Ontology-First Design

## Status

Accepted

---

# Context

Knowledge graphs become difficult to maintain if nodes and relationships are created without a shared conceptual model.

---

# Decision

Always define the ontology before implementing the Neo4j schema.

---

# Rationale

Benefits include:

- Consistency
- Reusability
- Easier maintenance
- Better documentation
- Simpler GraphRAG integration

---

# Consequences

The design phase requires additional effort but significantly reduces technical debt later in the project.