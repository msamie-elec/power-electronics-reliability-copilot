# [Unreleased]

## Current Focus

Version **0.6.0 — Cloud-Native Azure Deployment** is currently in progress.

The application has successfully transitioned to a cloud-aware architecture with Azure Blob Storage and Azure OpenAI integration. Current work focuses on completing Azure infrastructure deployment and production readiness while preserving the evidence-backed engineering workflow.

---

# [0.6.0] – In Progress

## Overview

Version **0.6.0** transitions the Power Electronics Reliability Copilot from a locally executed engineering application into a cloud-native AI engineering platform running on Microsoft Azure.

In addition to Azure integration, this release introduces a fully automated engineering knowledge ingestion pipeline. Newly uploaded engineering documents are automatically processed into searchable semantic knowledge without requiring manual chunking, embedding generation or FAISS indexing.

---

## Added

### Cloud Architecture

- Cloud-aware application configuration.
- AI provider abstraction supporting OpenAI and Azure OpenAI.
- Storage provider abstraction supporting Local Storage and Azure Blob Storage.
- Azure Blob Storage provider integration.
- Azure deployment automation scripts.
- Azure infrastructure validation scripts.

### Azure Services

- Azure Resource Group deployment.
- Azure Storage Account deployment.
- Azure Blob Container deployment.
- Azure Key Vault deployment scaffold.
- Azure OpenAI integration.
- GPT-5 Mini deployment.
- text-embedding-3-small deployment.

### Automated Engineering Knowledge Pipeline

- Automatic engineering document registration.
- Automatic deterministic document ID generation.
- Automatic PDF processing after upload.
- Automatic engineering knowledge chunk generation.
- Automatic semantic embedding generation.
- Automatic FAISS vector index generation.
- Automatic vector mapping generation.
- Automatic semantic retrieval preparation.

Every uploaded engineering document is now immediately available for semantic search and evidence-backed reasoning.

### Engineering Copilot

- Support for newly uploaded engineering documents.
- Automatic semantic retrieval for dynamically uploaded documents.
- Improved evidence preparation.
- Improved citation generation.
- Multi-turn engineering conversations using Azure OpenAI.

---

## Changed

### Architecture

- Introduced a dedicated Document ID Service.
- Removed duplicated document identifier generation logic.
- Unified document identity across:
  - Upload Service
  - Document Registry
  - Knowledge Pipeline
  - Semantic Retrieval
  - Engineering Copilot
- Improved separation of responsibilities between storage, upload, indexing and retrieval services.
- Refactored upload workflow to automatically build engineering knowledge assets.

### Storage

- Upload workflow now uses the Document Storage Service abstraction.
- Azure Blob Storage replaces direct filesystem storage when configured.
- Local storage remains fully supported for development.

---

## Fixed

- Fixed Engineering Copilot returning **404 Document Not Found** for newly uploaded engineering documents.
- Fixed inconsistent document identifiers across backend services.
- Fixed semantic retrieval failures for previously unseen engineering documents.
- Fixed missing FAISS indexes after document upload.
- Fixed evidence retrieval pipeline for dynamically uploaded documents.
- Fixed Azure Blob Storage authentication configuration.
- Fixed Azure OpenAI deployment configuration.
- Fixed Azure OpenAI rate-limit configuration during development.

---

## Validation

Successfully validated:

- Azure CLI authentication
- Azure Resource Group deployment
- Azure Storage Account deployment
- Azure Blob Container deployment
- Azure Blob upload
- Azure Blob listing
- Azure Blob download
- Automatic engineering document registration
- Automatic PDF parsing
- Automatic knowledge chunk generation
- Automatic embedding generation
- Automatic FAISS index generation
- Automatic semantic retrieval
- Azure OpenAI engineering reasoning
- Evidence-backed engineering responses
- Citation generation
- Multi-turn Engineering Copilot conversations

---

## Current Remaining Work

- Azure Key Vault secret integration
- Azure Container Apps backend deployment
- Azure Static Web Apps frontend deployment
- Azure Monitor
- Azure Application Insights
- End-to-end cloud validation

---

## Technical Impact

Version **0.6.0** establishes the project's first fully automated engineering knowledge ingestion pipeline.

The Engineering Copilot can now ingest an engineering document, automatically generate its semantic knowledge representation, build searchable vector indexes, and immediately answer engineering questions using evidence-backed Retrieval-Augmented Generation powered by Azure OpenAI.

This release also introduces the cloud-native architecture that forms the foundation for future production deployment.