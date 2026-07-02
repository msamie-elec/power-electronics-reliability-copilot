# ADR-003 — Use MERGE Instead of CREATE

## Status

Accepted

---

# Context

Knowledge graphs evolve over time through repeated imports.

---

# Decision

Use MERGE as the default Cypher command when creating nodes and relationships.

---

# Rationale

MERGE

- avoids duplicate nodes
- supports incremental imports
- enables repeatable deployment

---

# Consequences

Slightly slower than CREATE for very large initial imports, but considerably safer and more maintainable for long-term graph evolution.