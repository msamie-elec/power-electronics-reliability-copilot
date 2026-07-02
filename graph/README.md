# Graph Module

## Purpose

The `graph` module contains all resources required to create, populate, validate and query the Neo4j knowledge graph used by the Power Electronics Reliability Copilot.

The graph implements the engineering ontology defined in the project documentation and serves as the foundation for future GraphRAG and AI reasoning capabilities.

---

# Module Structure

```
graph/
│
├── schema/
│   ├── constraints.cypher
│   ├── indexes.cypher
│   └── schema.cypher
│
├── seed/
│   ├── sample_data.json
│   └── seed_graph.cypher
│
├── queries/
│   ├── validation.cypher
│   ├── graph_statistics.cypher
│   └── engineering_queries.cypher
│
└── README.md
```

---

# Workflow

The recommended workflow is:

1. Apply graph constraints.
2. Create indexes.
3. Review the schema.
4. Load the seed dataset.
5. Validate the graph.
6. Execute engineering queries.

---

# Graph Lifecycle

Engineering Documents

↓

Knowledge Extraction

↓

Graph-ready JSON

↓

Neo4j Knowledge Graph

↓

Cypher Queries

↓

GraphRAG

↓

AI Engineering Assistant

---

# Related Documentation

- `docs/ontology/POWER_ELECTRONICS_RELIABILITY_ONTOLOGY.md`
- `docs/ontology/POWER_ELECTRONICS_GRAPH_SCHEMA.md`
- `docs/ontology/KNOWLEDGE_INGESTION_DESIGN.md`
- `docs/ontology/diagrams/`

---

# Current Version

v0.4 — Knowledge Graph Foundation