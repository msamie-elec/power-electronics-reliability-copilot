# Changelog

Current Version: v0.3.0
All notable changes to this project will be documented in this file.

The format follows Keep a Changelog principles.

---
## v0.3.0_Engineering_Knowledge_Retrieval

## Sprint 3.4: Done
Sprint 3.4 is working. 

The /search endpoint is registered correctly. Swagger has generated the request body schema, which means:

✅ search.py is imported
✅ search.router is registered
✅ search_service.py imported successfully
✅ FastAPI recognises the endpoint

What have been built so far
v0.3.0 Intelligent Document Search

✓ Sprint 3.1
Document Chunking

✓ Sprint 3.2
Chunk Metadata

✓ Sprint 3.3
Embedding Generation

✓ Sprint 3.4
Semantic Search

Already completed:

upload PDFs
parse PDFs
convert to text
chunk text
attach metadata
generate embeddings
semantic retrieval

The pipeline is now:

PDF
   │
   ▼
Text Extraction
   │
   ▼
Chunking
   │
   ▼
Embeddings (384 dimensions)
   │
   ▼
Vector Database (JSON for now)
   │
   ▼
User Question
   │
   ▼
Question Embedding
   │
   ▼
Cosine Similarity
   │
   ▼
Top-k Relevant Chunks


## Sprints 3.1, 3.2, 3.3 done:
✅ backend/embeddings/ folder created
✅ Graph_embeddings.json generated
✅ /embeddings/generate endpoint working
✅ Response contains
embedding model
embedding dimension (384)
chunk metadata
embedding vectors
✅ HTTP 200 returned

This means Sprint 3.3 is successfully completed.

What we have achieved so far
Sprint 3.1

✔ PDF extraction

PDF
    ↓
Text
Sprint 3.2

✔ Intelligent chunking

PDF
    ↓
Text
    ↓
Chunks
Sprint 3.3

✔ Vector embeddings

PDF
    ↓
Text
    ↓
Chunks
    ↓
Embeddings

You have now built the complete preprocessing pipeline.

This is a major milestone because this is exactly how production RAG systems work.

Current architecture
Engineering PDF

      │

      ▼
PDF Parser

      │

      ▼
Extracted Text

      │

      ▼
Chunk Generator

      │

      ▼
Graph_chunks.json

      │

      ▼
SentenceTransformer

      │

      ▼
Graph_embeddings.json

That is already a solid backend pipeline.

## Sprint 3.3: Embedding Generation
We'll implement a proper vectorisation pipeline:

PDF
    ↓
Extract Text
    ↓
Chunk
    ↓
Generate Embeddings
    ↓
Store Embeddings
    ↓
FAISS Index
    ↓
Semantic Search

This is where the application evolves from a document manager into an actual AI retrieval system.

Sprint 3.3 enables asking questions like:

"What does the documentation say about bond wire fatigue?"

and the system will retrieve the most relevant chunks based on semantic similarity rather than simple keyword matching. That will be the first genuinely AI-powered capability in the project.


## Sprint 3.2.1
Updates the chunk JSON schema.
        Adds word_count.
        Adds created_at.
        Adds page_start and page_end (initially null).
        Improves the chunk_id naming convention.
        Creates an empty backend/embeddings/ folder with a .gitkeep file.
        Updates the Sprint 3.2 release notes to document the finalized chunk schema.

Therefore, Pipeline changed from:
PDF
   ↓
Text
   ↓
Chunks

to:
Why these fields?
Field	Why it matters
chunk_id	Unique identifier
source_document	Original uploaded PDF
source_text_file	Extracted text source
chunk_index	Preserve document order
page_start	Future GraphRAG citations
page_end	Future GraphRAG citations
character_count	Chunk statistics
word_count	Better diagnostics and chunk sizing
created_at	Versioning and debugging
text	Actual chunk content

The rpository now has a very logical data flow:
uploads/
        │
        ▼
documents/
        │
        ▼
metadata/
        │
        ▼
chunks/
        │
        ▼
embeddings/
        │
        ▼
Neo4j
        │
        ▼
GraphRAG

## Sprint 3.2 is complete
backend has evolved from:

Upload PDF

to

Upload PDF
        │
        ▼
uploads/
        │
        ▼
PDF Parser
        │
        ▼
documents/
        │
        ▼
Chunk Generator
        │
        ▼
chunks/

Each stage has a single responsibility:
| Folder    | Purpose                  |
| --------- | ------------------------ |
| uploads   | Original documents       |
| documents | Extracted text           |
| metadata  | Document metadata        |
| chunks    | AI-ready document chunks |






## Sprint 3.1 complete ✅

Completed features:

✅ PDF upload
✅ PDF parsing
✅ Text extraction
✅ TXT generation
✅ Metadata generation
✅ Automatic processing pipeline
✅ Modular parser service


## v0.2.0 - Backend API
Released: 30 June 2026

### Added

- FastAPI backend
- REST API architecture
- Swagger/OpenAPI documentation
- CORS configuration
- File upload endpoint
- Document listing endpoint
- Backend service layer
- Utility modules
- Frontend-backend integration
- Automatic upload refresh
- File metadata (size and upload date)

---

## v0.1.0 - Frontend Prototype
Released: 30 June 2026

### Added

- React + TypeScript + Vite frontend
- Enterprise dashboard layout
- Professional UI styling
- Engineering upload panel
- AI question panel
- Recommendation panel
- Evidence panel
- Knowledge graph preview
- Project documentation
- GitHub repository initialization
- MIT License
- Version roadmap
- Release documentation