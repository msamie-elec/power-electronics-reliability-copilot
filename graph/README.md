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

# Execution Order

Execute the Cypher scripts in the following order when creating a new database.

```
1. schema/constraints.cypher
2. schema/indexes.cypher
3. schema/schema.cypher
4. seed/seed_graph.cypher
5. queries/validation.cypher
6. queries/graph_statistics.cypher
7. queries/engineering_queries.cypher
```

This sequence ensures that constraints and indexes are created before loading data, the graph is validated after population, and engineering queries are executed against a verified knowledge graph.

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

# Current Graph Status

The current engineering knowledge graph contains a small seed dataset used to validate the ontology, schema and query library.

### Graph Statistics

| Item | Count |
|------|------:|
| Nodes | 11 |
| Relationships | 13 |

### Node Labels

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
- DocumentEvidence

### Relationship Types

- CONTAINS
- HAS_MATERIAL
- EXPERIENCES
- ACCELERATES
- INCREASES_RISK_OF
- RESULTS_IN
- PRODUCES
- VERIFIED_BY
- RECOMMENDS
- SUPPORTS
- AFFECTS

---

# Graph Lifecycle

```
Engineering Documents
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
Cypher Queries
          │
          ▼
GraphRAG
          │
          ▼
AI Engineering Assistant
```

---

# Future Expansion

The current implementation represents the **Knowledge Graph Foundation (v0.4)**.

Future releases will extend this module with:

- Automated PDF ingestion
- Document parsing
- Knowledge extraction pipelines
- Document chunking
- Embedding generation
- Vector indexing
- GraphRAG integration
- LLM-powered reasoning
- Engineering assistant APIs
- Multi-document knowledge fusion

---

# Related Documentation

### Ontology

- `docs/ontology/POWER_ELECTRONICS_RELIABILITY_ONTOLOGY.md`

### Neo4j Schema

- `docs/ontology/POWER_ELECTRONICS_GRAPH_SCHEMA.md`

### Knowledge Ingestion

- `docs/ontology/KNOWLEDGE_INGESTION_DESIGN.md`

### Ontology Diagrams

- `docs/ontology/diagrams/`

---

# Version

**Current Version**

```
v0.4
Knowledge Graph Foundation
```

This module provides the foundational graph architecture upon which future GraphRAG and AI reasoning capabilities will be built.