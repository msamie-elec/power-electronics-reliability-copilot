This is the point where the project starts becoming particularly interesting.

Up to Sprint 5.9 we've focused on **building** the engineering knowledge graph. From now on, the focus shifts to **using** that graph. This is where the system begins to behave like an engineering assistant rather than simply a document processing pipeline.

## Sprint 5.10 — Graph Retrieval Services

### Objective

Develop the retrieval layer that allows the Engineering Copilot to query Neo4j and retrieve engineering knowledge in a structured, explainable way.

This sprint sits between graph construction (Sprint 5.9) and GraphRAG (Sprint 5.11).

---

# Architecture

```
                Neo4j
                  │
                  │
      Graph Retrieval Service
                  │
        ┌─────────┴─────────┐
        │                   │
   REST API             Future GraphRAG
        │                   │
     Swagger          Engineering Copilot
```

---

# Deliverables

Instead of a single large service, we'll build one coherent retrieval service exposing several useful operations.

## 1. Graph Retrieval Service

New file:

```
backend/app/services/graph_retrieval_service.py
```

Responsibilities:

* connect to Neo4j
* execute read-only queries
* return structured Python objects
* hide Cypher from the API layer

---

## 2. Retrieval API

New router:

```
backend/app/api/knowledge_graph_retrieval.py
```

---

## 3. Endpoints

### A. Get Entity

```
GET /knowledge-graph/entity/{name}
```

Example:

```
GET

/knowledge-graph/entity/IGBT Module
```

Returns

```json
{
    "canonicalName":"IGBT Module",
    "type":"Component",
    "aliases":[...],
    "description":"..."
}
```

---

### B. Get Neighbours

```
GET /knowledge-graph/entity/{name}/neighbors
```

Returns

```text
IGBT Module

↓

HAS_FAILURE_MODE

↓

Bond Wire Lift-off

↓

CAUSES

↓

Open Circuit
```

Useful later for GraphRAG.

---

### C. Relationship Lookup

```
GET /knowledge-graph/relationship
```

Example

```
source=IGBT Module

relation=HAS_FAILURE_MODE
```

Returns

all matching targets.

---

### D. Evidence Lookup

```
GET

/knowledge-graph/entity/{name}/evidence
```

Returns

```json
{
    "sourceDocuments":[...],
    "chunkIds":[...]
}
```

This is extremely important because later the Engineering Copilot can answer:

> "This conclusion is supported by three engineering references."

---

### E. Search

```
GET

/knowledge-graph/search?q=thermal
```

Returns matching entities

similar to

```
thermal cycling

thermal fatigue

thermal resistance

thermal runaway
```

We'll implement this initially with a case-insensitive `CONTAINS` query and later replace it with Neo4j full-text indexes.

---

# New folder after Sprint 5.10

```
services/

    graph_validation_service.py

    neo4j_population_service.py

    graph_retrieval_service.py   ← NEW
```

---

# Why this order?

Many tutorials jump directly from graph population to GraphRAG. I prefer introducing this retrieval layer because it gives us:

* a clean service abstraction
* independently testable Cypher queries
* reusable retrieval logic
* easier debugging
* a foundation for GraphRAG

Later, the LLM will never query Neo4j directly—it will call this service.

---

# Sprint 5.10 deliverables

| Step | Deliverable             | Status |
| ---- | ----------------------- | ------ |
| 1    | Graph Retrieval Service | ⬜      |
| 2    | Entity lookup           | ⬜      |
| 3    | Neighbour retrieval     | ⬜      |
| 4    | Relationship lookup     | ⬜      |
| 5    | Evidence lookup         | ⬜      |
| 6    | Search endpoint         | ⬜      |
| 7    | Swagger validation      | ⬜      |

---

## My recommendation

Let's implement this sprint one file at a time, as we did for Sprint 5.9:

1. **`graph_retrieval_service.py`** (the core service)
2. API router exposing all retrieval endpoints
3. Register the router in `main.py`
4. Test every endpoint in Swagger
5. Verify the Cypher queries directly in Neo4j

This approach keeps the architecture clean and gives us a solid retrieval layer that Sprint 5.11 (Hybrid GraphRAG) can build on without needing to change the API design.
