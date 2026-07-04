# Sprint 5.9 — Neo4j Population

## Sprint Objective

Sprint 5.9 converts graph-ready JSON produced by Sprint 5.8B into a persistent Neo4j engineering knowledge graph.

The goal is to move from:

```text
Chunks → LLM Knowledge Extraction → Graph-ready JSON
````

to:

```text
Graph-ready JSON → Neo4j Nodes + Relationships
```

This sprint belongs to the Evidence Knowledge Pipeline, not the temporary user investigation pipeline.

---

## Architectural Context

Sprint 5.9 consumes files from:

```text
backend/knowledge_graph/
```

Example:

```text
backend/knowledge_graph/DOC-B3198A5.json
```

These files contain:

* extracted engineering entities
* extracted engineering relationships
* canonical names
* descriptions
* aliases
* evidence chunk IDs
* source document metadata

The population service writes this knowledge into Neo4j using `MERGE` so the graph can be incrementally expanded without creating duplicate nodes.

---

## Sprint 5.9A — Neo4j Population Service

### Status

✅ Implemented locally in VS Code.

### File Added

```text
backend/app/services/neo4j_population_service.py
```

### Capability

The service:

* reads graph-ready JSON from `backend/knowledge_graph/`
* loads entities and relationships
* MERGEs entity nodes into Neo4j using `canonicalName`
* MERGEs relationships using normalized relationship types
* preserves source document IDs
* preserves evidence chunk IDs
* returns a population summary

### Node Model

Entities are stored as:

```cypher
(:EngineeringEntity)
```

with properties:

```text
canonicalName
name
type
description
aliases
sourceDocuments
evidenceChunkIds
createdAt
updatedAt
```

### Relationship Model

Relationships are created between `EngineeringEntity` nodes.

Example:

```cypher
(:EngineeringEntity {canonicalName: "power cycling"})
-[:INDUCES]->
(:EngineeringEntity {canonicalName: "wear out failures"})
```

Relationship properties include:

```text
description
sourceDocuments
evidenceChunkIds
createdAt
updatedAt
```

### Design Decision

Sprint 5.9A uses `canonicalName` for `MERGE`.

Stable entity IDs, confidence scores, richer source metadata and ontology-specific labels are postponed to later refinement sprints.

---

## Sprint 5.9B — Graph Population API

### Status

⏳ Next

### File to Add

```text
backend/app/api/graph_population.py
```

### File to Update

```text
backend/app/main.py
```

### Planned Endpoint

```http
POST /knowledge-graph/populate
```

### Request Body

```json
{
  "document_id": "DOC-B3198A5"
}
```

### Expected Response

```json
{
  "status": "success",
  "documentId": "DOC-B3198A5",
  "entitiesRead": 23,
  "relationshipsRead": 23,
  "entitiesMerged": 23,
  "relationshipsMerged": 23,
  "relationshipsSkipped": 0
}
```

### Purpose

Expose Neo4j population through Swagger/FastAPI so the workflow can be demonstrated end-to-end.

---

## Sprint 5.9C — Neo4j Validation

### Status

⏳ Planned

### Planned Capability

Add validation after graph population.

Validation should report:

* total `EngineeringEntity` nodes
* total relationships
* number of entities linked to the source document
* number of relationships linked to the source document
* skipped or invalid relationships
* missing source/target nodes if any

### Example Validation Queries

```cypher
MATCH (e:EngineeringEntity)
RETURN count(e) AS entityCount;
```

```cypher
MATCH ()-[r]->()
RETURN count(r) AS relationshipCount;
```

```cypher
MATCH (e:EngineeringEntity)
WHERE $documentId IN e.sourceDocuments
RETURN count(e) AS documentEntityCount;
```

---

## Sprint 5.9D — Manual Test and Demo Scenario

### Status

⏳ Planned

### Test Document

```text
DOC-B3198A5
```

### Test Flow

```text
1. Run Sprint 5.8B knowledge extraction
2. Confirm graph-ready JSON exists
3. Run Sprint 5.9B population endpoint
4. Check response summary
5. Open Neo4j Browser
6. Run validation queries
7. Capture screenshots for documentation
```

### Demo Cypher Query

```cypher
MATCH path = (a:EngineeringEntity)-[r]->(b:EngineeringEntity)
RETURN path
LIMIT 25;
```

---

## Sprint 5.9E — Documentation and Closeout

### Status

⏳ Planned

### Documentation Updates

Update:

```text
docs/CHANGELOG.md
docs/sprints/sprint5.9.md
README.md
```

Add screenshots showing:

* FastAPI `/knowledge-graph/populate`
* successful JSON response
* Neo4j populated graph
* example Cypher query result

---

## Definition of Done

Sprint 5.9 is complete when:

* graph-ready JSON can be loaded into Neo4j
* entities are merged by `canonicalName`
* relationships are created using normalized relationship types
* evidence chunk IDs are preserved
* source document IDs are preserved
* population endpoint works in Swagger
* validation queries confirm graph content
* sprint documentation is updated

---

## Out of Scope for Sprint 5.9

The following are intentionally postponed:

* stable entity IDs
* confidence thresholds
* page-level source citation
* full ontology-specific node labels
* hybrid FAISS + Neo4j retrieval
* LangGraph orchestration
* frontend graph visualization

These will be addressed in later sprints.

```


```
# Updates:
Then where do our current tasks fit?

Instead of creating new sprint numbers, we keep them inside Sprint 5.9.

Sprint 5.9 — Neo4j Population
Task 5.9A
Create Neo4jPopulationService
Read graph-ready JSON
MERGE entities

Status: ✅

Task 5.9B
MERGE relationships
REST API
Swagger endpoint
Populate graph

Status: ✅

Task 5.9C
Graph validation
Statistics
Duplicate detection
Integrity checks

Status: Next

Task 5.9D
Improve graph schema
Better labels
Provenance
Confidence
Stable IDs

Status: Planned

Why I think this is better

Now Version 0.5 tells a clear story:

Documents
      │
      ▼
Registration
      │
      ▼
Chunks
      │
      ▼
Embeddings
      │
      ▼
Retrieval
      │
      ▼
Knowledge Extraction
      │
      ▼
Neo4j Population
      │
      ▼
Hybrid Retrieval
      │
      ▼
Engineering Copilot
      │
      ▼
Evaluation
      │
      ▼
Release

Each sprint corresponds to a major architectural capability, while the A/B/C/D items are implementation tasks.



# I think that's the right decision.


# Next Step: Sprint 5.9C

Now we move from **building** the graph to **understanding** the graph.

This is an important distinction.

Until now we've been asking:

> Can we populate Neo4j?

From now on we'll ask:

> Is the populated graph correct?

That is exactly what engineering software should do.

---

# Sprint 5.9C — Graph Validation & Inspection

This sprint should **not** modify the graph.

Its responsibility is only to inspect it.

```
Knowledge Graph JSON
        │
        ▼
Neo4j Population
        │
        ▼
Neo4j Database
        │
        ▼
Graph Validation Service
        │
        ├── Statistics
        ├── Integrity
        ├── Duplicates
        ├── Missing Evidence
        └── Quality Report
```

Notice that this service is **read-only**.

---

# Sprint 5.9C.1 (our immediate task)

We'll start with something simple but useful.

## Graph Statistics Service

Create

```
backend/
└── app/
    └── services/
        graph_validation_service.py
```

Initially it will provide methods such as:

```python
get_node_count()

get_relationship_count()

get_node_labels()

get_relationship_types()

get_graph_summary()
```

These are all read-only Cypher queries.

---

# Then

We'll expose them through

```
GET /knowledge-graph/summary
```

Expected response:

```json
{
  "status": "success",
  "summary": {
    "nodes": 34,
    "relationships": 23,
    "nodeLabels": {
      "EngineeringEntity": 23,
      "Component": 1,
      "Material": 1,
      "FailureMode": 1
    },
    "relationshipTypes": {
      "CONTAINS": 1,
      "HAS_MATERIAL": 1,
      "AFFECTS": 1
    }
  }
}
```

---

# Why this is useful

Today we looked manually inside Neo4j.

Tomorrow we should be able to ask the backend:

```
GET /knowledge-graph/summary
```

and immediately know whether the graph looks healthy.

This will become especially valuable once you have **hundreds of documents** and **tens of thousands of nodes**, where manual inspection is no longer practical.

---

# Proposed implementation workflow

As we've been doing successfully, we'll build this in small, testable steps:

1. **Architecture discussion** ✅
2. **Implement `graph_validation_service.py`**
3. **Test the service directly**
4. **Add the REST API**
5. **Test in Swagger**
6. **Review the graph statistics together**
7. **Commit to GitHub**

This keeps every commit meaningful and ensures each sprint produces a working capability.

I also have one architectural idea I'd like us to introduce during this sprint: instead of treating validation as a collection of unrelated queries, we'll design it so it can eventually support **engineering quality metrics** (graph completeness, provenance coverage, ontology consistency, etc.). That will make it reusable not only for the Power Electronics project but also for the future Claristry knowledge graphs. I suggest we introduce that design gradually as we build the validation service.
