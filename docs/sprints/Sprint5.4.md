# Plan update
To finish **v0.5.0 quickly**, I suggest this remaining sequence:

| Sprint  | Goal                 | Keep it simple                                      |
| ------- | -------------------- | --------------------------------------------------- |
| **5.4** | FAISS index          | Build index from `embeddings/knowledge/DOC-...json` |
| **5.5** | Semantic search      | Query FAISS and return matching chunks              |
| **5.6** | Knowledge extraction | Extract graph-ready JSON from chunks                |
| **5.7** | Neo4j population     | Load extracted entities/relationships               |
| **5.8** | Evaluation + notes   | Basic validation and release notes                  |

For LlamaIndex, we already used it in:

```text
SimpleDirectoryReader
SentenceSplitter
```

That is enough for v0.5. We can deepen LlamaIndex in v0.6 or v0.7. Otherwise we will slow down again.

Next step: **Sprint 5.4 — FAISS Index Pipeline**.

Create:

```text
backend/app/services/knowledge_faiss_service.py
backend/app/api/knowledge_faiss.py
```

This will:

```text
embeddings/knowledge/DOC-7E311A25.json
        ↓
FAISS index
        ↓
vector_store/knowledge/DOC-7E311A25.index
```

We’ll implement index creation first, then search.

# Update:
Sprint 5.4 is complete.

Confirmed:

{
  "status": "success",
  "documentId": "DOC-7E311A25",
  "vectorsIndexed": 15,
  "dimension": 384,
  "indexFile": "vector_store\\knowledge\\DOC-7E311A25.index",
  "mappingFile": "vector_store\\knowledge\\DOC-7E311A25_mapping.json"
}

You now have:

Knowledge PDF
↓
Register
↓
Chunk
↓
Embedding
↓
FAISS Index