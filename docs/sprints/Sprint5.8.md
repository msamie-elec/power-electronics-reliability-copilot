# This is where the project starts becoming a true AI knowledge engineering platform rather than just a RAG system.

## Sprint 5.8 — Knowledge Extraction

The objective is to transform retrieved document chunks into **structured engineering knowledge**.

Current pipeline:

```text
Engineering PDF
      │
      ▼
LlamaIndex
      │
      ▼
Document Registration
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
FAISS Index
      │
      ▼
Semantic Search
```

After Sprint 5.8:

```text
Engineering PDF
      │
      ▼
LlamaIndex
      │
      ▼
Chunks
      │
      ▼
LLM Knowledge Extraction
      │
      ▼
Graph-ready JSON
```

---

# What are we extracting?

We are **not** asking the LLM to answer questions.

We are asking it to **read engineering text and identify knowledge**.

For example, from this paragraph:

> Thermal cycling causes solder fatigue in IGBT modules. Increased junction temperature accelerates crack propagation.

we want:

```json
{
  "entities": [
    {
      "type": "FailureMechanism",
      "name": "Thermal Cycling"
    },
    {
      "type": "Material",
      "name": "Solder"
    },
    {
      "type": "Component",
      "name": "IGBT Module"
    },
    {
      "type": "FailureMode",
      "name": "Solder Fatigue"
    },
    {
      "type": "Parameter",
      "name": "Junction Temperature"
    }
  ],
  "relationships": [
    {
      "source": "Thermal Cycling",
      "relation": "CAUSES",
      "target": "Solder Fatigue"
    },
    {
      "source": "Solder Fatigue",
      "relation": "OCCURS_IN",
      "target": "IGBT Module"
    },
    {
      "source": "Junction Temperature",
      "relation": "ACCELERATES",
      "target": "Crack Propagation"
    }
  ]
}
```

That is exactly the structure Neo4j likes.

---

# We should keep the extraction generic

Don't hard-code power electronics terms.

Instead define a general schema such as:

```text
Entity
------
name
type
description
evidence

Relationship
------------
source
relation
target
confidence
evidence
```

This makes the extractor reusable later for:

* Mechanical engineering
* Civil engineering
* Mathematics
* Education (Claristry)
* Healthcare

---

# Folder structure

Create:

```
backend/
└── app/
    ├── services/
    │     knowledge_extraction_service.py
    │
    ├── api/
    │     knowledge_extraction.py
    │
    └── models/
          knowledge_extraction.py
```

---

# Outputs

Store extracted knowledge separately from chunks.

```
knowledge_graph/

    DOC-2ED1BD7F.json

```

Example:

```
knowledge_graph/

    DOC-2ED1BD7F.json
```

Inside:

```json
{
  "documentId": "...",
  "entities": [],
  "relationships": [],
  "metadata": {}
}
```

This becomes the input to the Neo4j population service in Sprint 5.9.

---

# Should we use GPT or not?

This is an important architectural decision.

### Option 1 — Rule-based extraction

Pros:

* Free
* Fast
* Deterministic

Cons:

* Poor quality
* Brittle
* Hard to extend

---

### Option 2 — spaCy / NER

Pros:

* Fast

Cons:

* Engineering vocabulary is limited.
* Misses many domain-specific relationships.

---

### Option 3 — GPT-4.1 / GPT-5 (recommended)

Pros:

* Excellent extraction quality.
* Understands engineering language.
* Can infer relationships.
* Easily adapted by changing prompts.

Cons:

* API cost.

Given your long-term goals and the fact that this project is also meant to demonstrate enterprise AI architecture, I recommend **Option 3**. It aligns with the technologies employers are looking for and produces much higher-quality graph data.

---

## Sprint 5.8 plan

We'll build it in four small steps:

1. **Knowledge Extraction Service** — Reads chunk files and calls the LLM.
2. **Structured Prompt** — Instructs the LLM to return valid JSON with entities and relationships.
3. **JSON Validation** — Parse and validate the returned structure before saving.
4. **Knowledge Extraction API** — Expose `/knowledge-extraction/run` and save the graph-ready JSON.

After that, Sprint 5.9 (Neo4j population) becomes straightforward: it simply reads the JSON and creates or updates graph nodes and relationships using `MERGE`. This separation keeps extraction and graph persistence cleanly decoupled, which is a common enterprise design pattern.


# updates:
Sprint 5.8A ✅
Rule-based extraction

↓

Sprint 5.8B
LLM extraction

↓

Sprint 5.9
Neo4j population

↓

Sprint 5.10
Hybrid Retrieval

↓

Sprint 5.11
Engineering Agent

Model choice: gpt-4.1-mini or cheaper mini/nano model

# Sprint 5.8B — LLM Knowledge Extraction

We are going to replace only the extraction logic, while leaving the rest of the pipeline unchanged.

Currently:

Chunks
   │
   ▼
Regex Extraction
   │
   ▼
Graph JSON

We'll change it to:

Chunks
   │
   ▼
GPT-4.1-mini
   │
   ▼
Validated Graph JSON

Everything downstream (Neo4j, GraphRAG, Hybrid Retrieval) stays exactly the same.


# Updates:
Sprint 5.8 goal:
Chunks → GPT-4.1-mini → graph-ready JSON → saved in knowledge_graph/