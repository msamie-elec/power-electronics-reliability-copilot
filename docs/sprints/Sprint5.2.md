Yes, better to modify the frontend **later**, not now.

For now, v0.5 is backend pipeline work. The frontend should be updated when the backend workflow is stable, probably after:

```text
Sprint 5.3 — Embeddings
Sprint 5.4 — Knowledge Extraction
Sprint 5.5 — Graph Population
```

Then we can add a clean UI such as:

```text
Admin Knowledge Upload
Register Evidence Document
Create Chunks
Generate Embeddings
Extract Knowledge
Populate Graph
```

## Record for Sprint 5.2

Add this to your sprint/history notes:

````markdown
# Sprint 5.2 — Knowledge Chunk Pipeline

## Status

Completed.

## Objective

Create a backend pipeline for splitting approved engineering evidence documents into traceable chunks for the Knowledge Graph and GraphRAG workflow.

## Completed Work

- Created `knowledge_chunk_service.py`.
- Created `knowledge_chunks.py` API route.
- Added `/knowledge-chunks/create` endpoint.
- Added separate storage for knowledge chunks:

```text
backend/chunks/knowledge/
````

* Tested chunk creation using an approved evidence PDF stored in:

```text
backend/knowledge_base/reliability/Graph.pdf
```

* Successfully created chunks from registered evidence document:

```text
documentId: DOC-7E311A25
chunksCreated: 15
outputFile: chunks/knowledge/DOC-7E311A25.json
```

## Important Design Decision

The project now separates:

```text
User investigation documents
→ backend/uploads/
→ investigation workflow

Approved evidence documents
→ backend/knowledge_base/
→ knowledge workflow
```

Knowledge chunks are stored separately from investigation chunks:

```text
backend/chunks/investigation/
backend/chunks/knowledge/
```

## Known Follow-up

Swagger/API currently shows mixed naming between camelCase and snake_case in some outputs and inputs.

Current backend request model uses:

```json
{
  "document_id": "...",
  "file_path": "..."
}
```

Some responses still return:

```json
{
  "documentId": "...",
  "filePath": "..."
}
```

This should be standardised later before frontend integration.

Recommended future decision:

* Use `snake_case` internally in backend Python.
* Convert to `camelCase` only at the frontend/API boundary if needed.

## Frontend Update

Frontend integration is deferred.

The frontend should be updated later after the backend GraphRAG workflow is stable, likely after Sprints 5.3–5.5.

Planned future UI:

* Admin evidence document upload
* Register knowledge document
* Create knowledge chunks
* Generate embeddings
* Extract graph-ready knowledge
* Populate Neo4j

````
