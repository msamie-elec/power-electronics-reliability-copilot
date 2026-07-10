# Changelog

All notable changes to the Power Electronics Reliability Copilot project are documented in this file.

The project follows a release-based engineering methodology. Each release introduces a major architectural capability while preserving a stable and testable platform.

---

# [Unreleased]

## Current Focus

Development now transitions to **v0.7.0 — Production Engineering and DevOps**.

Version **v0.7.0** will focus on production hosting, containerisation, managed identity, Azure Container Apps backend deployment, Azure Static Web Apps frontend deployment, CI/CD, and production operational hardening.

## Planned v0.7.0 Priorities

- Docker containerisation.
- Azure Container Apps backend deployment.
- Azure Static Web Apps frontend deployment.
- Managed Identity for Azure-hosted backend services.
- Replace Azure Storage connection strings with Managed Identity and Azure RBAC for Blob Storage access.
- Production environment configuration.
- CI/CD deployment workflow.
- Production observability and alerting.
- End-to-end cloud deployment validation.

---

# [0.6.0] — Cloud-Native Azure Integration

**Status:** ✅ Completed  
**Release Theme:** Cloud-native Azure integration, secure secret management, automated ingestion, observability and release validation.

## Overview

Version **0.6.0** transitions the Power Electronics Reliability Copilot from a local engineering AI application into a cloud-integrated architecture built around Microsoft Azure services.

This release introduces Azure Blob Storage, Azure OpenAI, Azure Key Vault, Azure Monitor, Application Insights, provider-based configuration management, automated engineering knowledge indexing for newly uploaded documents, and production-style health diagnostics.

Frontend and backend cloud hosting are intentionally deferred to **v0.7.0**, where Docker, Azure Container Apps, Azure Static Web Apps, Managed Identity and CI/CD will become the main focus.

## v0.6.0 Milestone Summary

| Milestone | Status | Focus |
|----------|--------|-------|
| v0.6.0-01 | ✅ Completed | Secret Provider Architecture |
| v0.6.0-02 | ✅ Completed | Secret Service Integration |
| v0.6.0-03 | ✅ Completed | Azure Key Vault Integration |
| v0.6.0-04 | ✅ Completed | Azure Monitor, Application Insights and Health Diagnostics |
| v0.6.0-05 | ✅ Completed | Documentation, Release Validation and GitHub Tag Preparation |

---

## v0.6.0-01 — Secret Provider Architecture

**Status:** ✅ Completed

### Added

- Enterprise Secret Provider architecture.
- `BaseSecretProvider` abstraction.
- `LocalSecretProvider` implementation.
- `AzureKeyVaultSecretProvider` skeleton.
- `SecretService` factory entry point.
- Dedicated `backend/app/services/secrets/` package.

### Architecture Impact

- Introduced a provider-based approach for secrets matching the existing AI Provider and Storage Provider architecture.
- Prepared the application to support both local `.env` development and cloud-managed secrets.
- Isolated secret retrieval from business logic and infrastructure services.

### Validation

- Secret provider architecture added without changing existing application behaviour.
- Backend compatibility preserved.

---

## v0.6.0-02 — Secret Service Integration

**Status:** ✅ Completed

### Added

- Secret retrieval support inside cloud-facing services.
- Local fallback mapping for Azure-safe secret names.
- Provider-independent secret access for backend services.

### Changed

- Azure OpenAI now retrieves credentials through `SecretService`.
- Azure Blob Storage now retrieves credentials through `SecretService`.
- Neo4j now retrieves credentials through `SecretService`.
- Reduced direct use of sensitive environment variables inside cloud service implementations.
- Improved separation between infrastructure configuration and application secrets.

### Fixed

- Confirmed Neo4j authentication after correcting local credential configuration.
- Improved reliability of local secret resolution.

### Validation

- Backend regression suite passed after Secret Service integration.
- Regression status: **25 / 25 backend tests passed**.

---

## v0.6.0-03 — Azure Key Vault Integration

**Status:** ✅ Completed

### Added

- Azure Key Vault integration using Azure SDK.
- Real Azure Key Vault secret retrieval through `AzureKeyVaultSecretProvider`.
- Azure RBAC-based Key Vault authorization.
- `Key Vault Secrets Officer` role assignment for local secret import.
- Automated Key Vault secret import script:
  - `infra/azure/powershell/05b-import-keyvault-secrets.ps1`
- Automated Key Vault validation script:
  - `infra/azure/powershell/05c-validate-keyvault.ps1`
- Local-only secret file workflow:
  - `infra/azure/env/azure.secrets.local.env`

### Managed Secrets

Required secrets now managed through Azure Key Vault:

- `azure-openai-api-key`
- `azure-storage-connection-string`
- `neo4j-password`

Optional secret:

- `openai-api-key`

### Changed

- Backend can run with `SECRET_PROVIDER=azure_key_vault`.
- Azure OpenAI, Azure Blob Storage and Neo4j credentials can now be removed from local `.env` files.
- Local development fallback remains supported through `SECRET_PROVIDER=local`.
- Cloud secret management now follows the provider-based architecture.

### Validation

Successfully validated:

- Azure Key Vault creation.
- Azure RBAC role assignment.
- Secure import of required secrets.
- Key Vault validation without printing secret values.
- Azure OpenAI authentication through Key Vault.
- Azure Blob Storage authentication through Key Vault.
- Neo4j authentication through Key Vault.
- Backend execution with Key Vault-based secrets.
- Regression status: **25 / 25 backend tests passed**.

---

## v0.6.0-04 — Observability and Health Diagnostics

**Status:** ✅ Completed

### Added

- Azure Monitor foundation.
- Log Analytics Workspace automation:
  - `infra/azure/powershell/06a-create-log-analytics.ps1`
- Application Insights automation:
  - `infra/azure/powershell/06b-create-application-insights.ps1`
- Monitoring validation automation:
  - `infra/azure/powershell/06c-validate-monitoring.ps1`
- Application Insights connection string stored securely in Azure Key Vault:
  - `applicationinsights-connection-string`
- Backend telemetry configuration module.
- Backend structured logging configuration module.
- Production-style health diagnostics service.
- Enhanced `/health` endpoint for lightweight status checks.
- New `/health/details` endpoint for dependency diagnostics.

### Health Diagnostics

The detailed health endpoint validates:

- Azure Key Vault reachability.
- Azure Blob Storage account and container reachability.
- Azure OpenAI configuration and credential resolution.
- Neo4j database connectivity.
- Active AI, storage, secret and graph providers.
- Dependency latency in milliseconds.
- Application uptime.
- Application version and environment.

### Validation

Successfully validated:

- Log Analytics Workspace creation.
- Application Insights creation.
- Application Insights connection string stored in Key Vault.
- Monitoring validation script execution.
- `/health` lightweight endpoint.
- `/health/details` dependency diagnostics endpoint.
- Azure Blob Storage health after connection string refresh.
- Azure Key Vault health.
- Azure OpenAI configuration health.
- Neo4j connectivity health.
- Swagger/OpenAPI version updated to `0.6.0-dev`.
- Regression status: **25 / 25 backend tests passed**.
- Frontend production build passed.

---

## v0.6.0-05 — Documentation and Release Validation

**Status:** ✅ Completed

### Added

- v0.6.0 release notes:
  - `docs/releases/v0.6.0_RELEASE_NOTES.md`
- Observability validation documentation:
  - `docs/cloud/OBSERVABILITY_VALIDATION.md`
- v0.6.0-04 implementation notes:
  - `docs/cloud/v0.6.0-04_IMPLEMENTATION_NOTES.md`
- Updated Azure infrastructure documentation.
- Updated root README for cloud-native v0.6.0 capabilities.
- Updated release roadmap for v0.7.0 production deployment and Managed Identity.

### Validation

Final release validation completed:

- Backend regression test suite: **25 / 25 tests passed**.
- Frontend production build: **Passed**.
- Key Vault validation: **Passed**.
- Monitoring validation: **Passed**.
- `/health`: **healthy**.
- `/health/details`: **healthy**.

---

## Cloud Architecture

### Added

- Cloud-aware backend configuration.
- AI Provider abstraction supporting OpenAI and Azure OpenAI.
- Storage Provider abstraction supporting Local Storage and Azure Blob Storage.
- Document Storage Service abstraction.
- Azure Blob Storage Provider.
- Azure deployment automation under `infra/azure/powershell`.
- Secure Azure configuration under `infra/azure/env`.
- Azure cleanup script for cost-controlled development.

### Azure Services

- Azure CLI tenant-specific login automation.
- Azure Resource Group automation.
- Azure Storage Account automation.
- Azure Blob Container automation.
- Azure OpenAI resource and deployment workflow.
- Azure Key Vault automation.
- Azure Monitor and Application Insights automation.
- Azure infrastructure validation scripts.

### Validated Azure Services

- Azure CLI authentication.
- Resource Group creation.
- Storage Account creation.
- Blob Container creation.
- Key Vault creation.
- Log Analytics Workspace creation.
- Application Insights creation.
- Blob upload.
- Blob listing.
- Blob download.
- Azure OpenAI chat deployment.
- Azure OpenAI embedding deployment.
- Key Vault secret retrieval.
- Health diagnostics.

---

## Azure OpenAI Integration

### Added

- Azure OpenAI provider support.
- Azure OpenAI deployment configuration.
- GPT deployment support.
- `text-embedding-3-small` embedding deployment support.
- Azure OpenAI model discovery and deployment scripting.

### Changed

- Backend reasoning can switch between OpenAI and Azure OpenAI through configuration.
- AI Provider abstraction isolates provider-specific client creation.
- Azure OpenAI deployments are configured through environment settings and secret providers.

### Fixed

- Azure OpenAI request configuration for newer model deployments.
- Azure OpenAI deployment configuration during development.
- Azure OpenAI rate-limit and request parameter issues encountered during testing.

---

## Azure Blob Storage Integration

### Added

- Azure Blob Storage Provider for uploaded engineering documents.
- Azure Storage Account deployment automation.
- Blob Container deployment automation.
- Storage connection validation tests.
- Blob upload, list and download validation.

### Changed

- Upload workflow now uses `DocumentStorageService`.
- Local filesystem storage and Azure Blob Storage now share a provider-based interface.
- Azure Blob Storage replaces direct filesystem persistence when configured.
- Local processing copies are still preserved for parsing, chunking, embedding and indexing.

### Validation

- Frontend upload successfully stored documents in Azure Blob Storage.
- Uploaded PDFs confirmed in Azure Blob Storage.
- Azure Blob upload/list/download tests passed.

### Future Improvement

In **v0.7.0**, Azure Blob Storage authentication will be upgraded from connection-string based access to **Managed Identity + Azure RBAC**. This will remove the need to store or rotate Azure Storage connection strings and align Blob Storage access with production Azure identity practices.

---

## Automated Engineering Knowledge Pipeline

### Added

- Automatic engineering document registration after upload.
- Automatic deterministic document ID generation.
- Automatic PDF processing after upload.
- Automatic engineering knowledge chunk generation.
- Automatic semantic embedding generation.
- Automatic FAISS vector index generation.
- Automatic vector mapping generation.
- Automatic semantic retrieval preparation.
- Upload response metadata showing document ID, chunk count, embedding status and FAISS indexing status.

### Changed

- Newly uploaded engineering documents no longer require manual indexing.
- Engineering Copilot can answer questions against dynamically uploaded documents.
- Document identity is unified across upload, registry, knowledge pipeline, semantic retrieval and Engineering Copilot.
- Document ID generation moved into a dedicated Document ID Service.

### Fixed

- Fixed Engineering Copilot returning **404 Document Not Found** for newly uploaded documents.
- Fixed inconsistent document identifiers across frontend and backend services.
- Fixed mismatched identifiers between uploaded documents and retrieval indexes.
- Fixed missing semantic retrieval assets after upload.
- Fixed evidence retrieval pipeline for previously unseen engineering documents.

### Validation

Successfully validated:

- PDF text extraction.
- Engineering document registration.
- Automatic chunk generation.
- Automatic embedding generation.
- Automatic FAISS index generation.
- Semantic evidence retrieval.
- Azure OpenAI engineering reasoning.
- Evidence-backed engineering responses.
- Citation generation.
- Multi-turn Engineering Copilot conversations.

---

## Technical Impact

Version **0.6.0** establishes the cloud-native foundation of the Power Electronics Reliability Copilot.

Major architectural capabilities introduced include:

- Provider-based cloud architecture.
- Azure Blob Storage integration.
- Azure OpenAI integration.
- Enterprise Secret Provider architecture.
- Azure Key Vault secret management.
- Azure Monitor and Application Insights foundation.
- Production-style health diagnostics.
- Automated engineering knowledge ingestion.
- Automatic vector indexing.
- Evidence-backed Retrieval-Augmented Generation for newly uploaded documents.

The project is now prepared for production hosting, Managed Identity, CI/CD and full Azure deployment in v0.7.0.

---

# [0.5.2] — Professional Engineering Workspace

**Status:** ✅ Completed

## Overview

Version **0.5.2** completed the professional engineering workspace before cloud deployment. It introduced conversation-aware reasoning, backend conversation memory, document registry integration, active document selection and improved frontend-backend integration.

## Added

### Conversation Memory

- Backend conversation history support.
- Context-aware follow-up questions.
- Conversation history passed into engineering reasoning prompts.
- Local handling for previous-question requests.
- Copy selected answer functionality.
- Markdown conversation export.

### Document Registry

- Document Registry Service.
- `/documents` registry endpoint returning frontend-ready document records.
- Stable document identifiers.
- Pipeline-compatible document ID mapping.
- Active engineering document display.
- Document selection from the frontend UI.

### Workspace Refinement

- Active document selection persisted in local storage.
- Selected document shown in the conversation header.
- Improved conversation memory status display.
- Cleaner document registry panel.
- Improved frontend integration with backend document metadata.

## Changed

- Frontend no longer relies on manually entering a fixed document ID.
- Engineering Copilot requests now use the selected active document.
- Document handling moved toward a registry-based workflow.
- v0.5.2 scope was simplified to complete the end-to-end MVP before Azure deployment.

## Fixed

- Neo4j `DateTime` serialization issue in graph/evidence responses.
- JSON-safe evidence preparation for frontend/API responses.
- Backend response stability for graph metadata.

## Validation

- Active document selection validated.
- Document selection persistence after refresh validated.
- Context-aware follow-up questions validated.
- Previous-question listing validated.
- Engineering Copilot API integration validated.
- Frontend production build passed.
- Backend regression suite passed.

## Regression Status

- Backend regression tests: **20 / 20 passing**.
- Frontend production build: **Passing**.

## Internal Milestones

| Task | Capability | Status |
|------|------------|--------|
| 5.2.1 | Conversation Memory Foundation | ✅ Completed |
| 5.2.2 | JSON-safe Evidence Serialization | ✅ Completed |
| 5.2.3 | Document Registry Integration | ✅ Completed |
| 5.2.4 | Active Document Selection | ✅ Completed |
| 5.2.5 | Final Workspace Validation | ✅ Completed |

---

# [0.5.1] — Conversational Engineering Copilot

**Status:** ✅ Completed

## Overview

Version **0.5.1** introduced the modern conversational Engineering Copilot workspace. It focused on frontend workflow, multi-turn conversation display, evidence synchronisation and engineering investigation usability.

## Added

### Conversational Engineering Workspace

- Three-panel engineering workspace.
- Modern conversational engineering interface.
- Multi-turn engineering conversations.
- Conversation history.
- Clear Conversation functionality.
- Active answer selection.
- Collapsible engineering responses.
- Question numbering.
- Answer numbering.
- Conversation timestamps.

### Evidence Workspace

- Sticky Evidence panel.
- Sticky Documents panel.
- Evidence synchronisation with selected response.
- Active evidence switching.
- Evidence summary cards.
- Question preview within Evidence panel.
- Evidence statistics.
- Citation summary.
- Knowledge Graph summary.
- Automatic evidence scrolling.

### User Experience

- Responsive engineering dashboard.
- Improved workspace layout.
- Engineering report presentation.
- Better navigation for long conversations.
- Persistent engineering investigation workflow.
- Improved frontend responsiveness.
- Stable production build.

### Frontend Integration

- Full integration with the Engineering Copilot API.
- Structured rendering of engineering responses.
- Session-based conversation management.
- Improved evidence rendering.
- Enhanced engineering report formatting.

## Changed

- Frontend redesigned into a conversational engineering workspace.
- Engineering responses now support multi-turn interaction.
- Evidence panel dynamically follows the selected engineering response.
- Conversation workflow redesigned for engineering investigations.
- Navigation improved for long engineering sessions.
- Frontend prepared for conversation-aware backend integration.

## Internal Milestones

| Task | Capability | Status |
|------|------------|--------|
| 5.1.1 | Conversational Workspace | ✅ Completed |
| 5.1.2 | Multi-turn Conversation | ✅ Completed |
| 5.1.3 | Conversation History | ✅ Completed |
| 5.1.4 | Active Answer Selection | ✅ Completed |
| 5.1.5 | Collapsible Responses | ✅ Completed |
| 5.1.6 | Sticky Workspace Panels | ✅ Completed |
| 5.1.7 | Evidence Synchronisation | ✅ Completed |
| 5.1.8 | Improved Evidence Cards | ✅ Completed |
| 5.1.9 | Question and Timestamp Metadata | ✅ Completed |
| 5.1.10 | Workspace Refinement | ✅ Completed |

---

# [0.5.0] — Evidence-backed Engineering Copilot

**Status:** ✅ Backend Complete / Release Candidate

## Overview

Version **0.5.0** transformed the project from a semantic RAG prototype into an evidence-backed engineering AI platform. It integrated document processing, structured engineering knowledge extraction, Neo4j graph population, hybrid retrieval and explainable AI reasoning into a unified backend.

## Added

### Engineering Knowledge

- Engineering knowledge extraction.
- Graph-ready JSON generation.
- Entity extraction.
- Relationship extraction.
- Engineering ontology refinement.
- Neo4j graph population.
- Graph validation services.

### Knowledge Graph Retrieval

- Knowledge Graph retrieval services.
- Graph summary API.
- Entity retrieval API.
- Relationship retrieval API.
- Knowledge graph search.
- Relationship filtering.
- Neighbour exploration.
- Evidence retrieval.

### Evidence-backed AI Reasoning

- Hybrid semantic and graph retrieval.
- Engineering reasoning context builder.
- Evidence ranking and deduplication.
- Graph evidence preparation.
- Prompt modularisation.
- Evidence-backed reasoning.
- Explainable engineering responses.
- Confidence-aware recommendations.

### Engineering Copilot Backend

- Engineering Copilot service.
- Engineering Copilot REST API.
- Structured Pydantic response models.
- Engineering metadata models.
- Citation generation.
- Typed API contracts.
- End-to-end reasoning pipeline.
- Swagger validation.
- Backend integration.

### Backend Quality Improvements

- Dedicated Evidence Preparation Service.
- Dedicated Citation Service.
- Custom project exceptions.
- Structured logging.
- Improved service separation.
- Cleaner orchestration layer.
- Improved maintainability.
- Better API documentation.

## Changed

- Engineering Copilot now returns structured response models instead of untyped dictionaries.
- Prompt construction moved into dedicated prompt modules.
- Evidence preparation extracted into dedicated services.
- Citation generation separated from reasoning logic.
- Backend services further modularised.
- Evidence-backed reasoning standardised across APIs.
- Logging introduced throughout the reasoning pipeline.
- Custom exception hierarchy introduced.
- Documentation reorganised into permanent and historical sections.

## Testing

Added automated validation for:

- Knowledge Graph Retrieval APIs.
- Evidence-backed Reasoning APIs.
- Engineering Copilot APIs.
- Negative validation scenarios.
- Backend regression testing.

## Regression Status

- Knowledge Graph Retrieval: **10 / 10**.
- Evidence-backed Reasoning: **5 / 5**.
- Engineering Copilot: **5 / 5**.
- Total backend tests: **20 / 20 passing**.

## Internal Milestones

| Task | Capability | Status |
|------|------------|--------|
| 5.1 | Knowledge Document Registration | ✅ Completed |
| 5.2 | Document Chunking | ✅ Completed |
| 5.3 | Embedding Generation | ✅ Completed |
| 5.4 | FAISS Vector Index | ✅ Completed |
| 5.5 | Semantic Retrieval | ✅ Completed |
| 5.6 | Retrieval Service | ✅ Completed |
| 5.7 | Ingestion Pipeline | ✅ Completed |
| 5.8 | Engineering Knowledge Extraction | ✅ Completed |
| 5.9 | Knowledge Graph Population | ✅ Completed |
| 5.10 | Knowledge Graph Retrieval | ✅ Completed |
| 5.11 | Evidence-backed AI Reasoning | ✅ Completed |
| 5.12 | Engineering Copilot Backend | ✅ Completed |
| 5.13 | Backend Refinement and Release Preparation | ✅ Completed |

---

# [0.4.0] — Knowledge Graph Foundation

**Status:** ✅ Released

## Overview

Version **0.4.0** established the Knowledge Graph foundation for the project. It introduced Neo4j Aura, an engineering ontology, graph schema, constraints, indexes, seed data, validation queries and GraphRAG preparation.

## Added

### Neo4j Integration

- Dedicated Neo4j Aura database for the Power Electronics project.
- Secure environment configuration for Neo4j.
- Neo4j Python driver integration.
- Graph Service.
- `/graph/health` API endpoint.
- FastAPI-to-Neo4j connectivity validation.

### Engineering Ontology

- Engineering ontology design.
- Node definitions.
- Relationship definitions.
- Property model.
- Identifier strategy.
- Conceptual ontology diagrams.
- Neo4j graph schema diagrams.
- Engineering knowledge graph example diagrams.

### Knowledge Graph Implementation

- Neo4j graph schema.
- Unique constraints.
- Search indexes.
- Seed engineering data.
- Connected engineering knowledge graph.
- Reusable Cypher query library.
- Graph statistics queries.
- Graph validation queries.

### GraphRAG Preparation

- Graph-ready architecture.
- Knowledge ingestion design.
- Source tracking model.
- Chunk linkage design.
- Evidence-first graph modelling.
- Future GraphRAG retrieval workflow.

## Validation

Successfully validated:

- FastAPI-to-Neo4j connectivity.
- `RETURN 1` graph query.
- Constraint execution.
- Index execution.
- Schema execution.
- Seed graph execution.
- Graph statistics.
- Graph validation.

## Graph Statistics

| Item | Result |
|------|--------|
| Nodes | 11 |
| Relationships | 13 |
| Labels | 11 |
| Validation | Passed |

## Internal Milestones

| Sprint | Capability | Status |
|--------|------------|--------|
| 4.1 | Neo4j Integration | ✅ Completed |
| 4.3 | Ontology and Schema | ✅ Completed |
| 4.3.1 | Ontology Diagrams | ✅ Completed |
| 4.3.2 | Knowledge Ingestion Design | ✅ Completed |
| 4.4 | Neo4j Schema | ✅ Completed |
| 4.4.1 | Constraints and Indexes | ✅ Completed |
| 4.4.2 | Seed Engineering Graph | ✅ Completed |
| 4.5 | Graph Validation | ✅ Completed |
| 4.6-4.8 | Final v0.4 Implementation Work | ✅ Completed |

---

# [0.3.0] — Engineering Knowledge Retrieval

**Status:** ✅ Released / Release Candidate Completed

## Overview

Version **0.3.0** introduced the first major AI capability: engineering document ingestion, semantic retrieval and Retrieval-Augmented Generation. The application became capable of parsing uploaded engineering documentation, retrieving relevant evidence and generating grounded engineering answers.

## Added

### Document Processing

- PDF ingestion.
- TXT ingestion.
- CSV ingestion.
- Automatic parsing.
- PDF text extraction.
- TXT generation.
- Metadata generation.

### Intelligent Chunking

- Document chunk generation.
- Chunk metadata.
- Word counts.
- Chunk identifiers.
- Timestamp metadata.

### Embedding Generation

- Sentence Transformer embeddings.
- Embedding persistence.
- Embedding metadata.

### Semantic Retrieval

- FAISS indexing.
- Cosine similarity search.
- Top-k retrieval.
- Search API.
- Semantic similarity search.
- Retrieval-Augmented Generation.
- Source attribution.
- Confidence estimation.

### AI Integration

- OpenAI integration.
- Engineering prompt generation.
- Grounded engineering answers.
- Evidence-backed responses.

### Frontend Integration

- Frontend RAG integration.
- Evidence display.
- Confidence display.
- Source attribution.

### Testing and Release Preparation

- Pytest integration.
- API tests.
- TestClient configuration.
- Backend validation.
- End-to-end workflow validation.
- Invalid input handling.
- File type validation.
- Empty question validation.
- Upload workflow improvements.
- Documentation updates.

## Internal Milestones

| Sprint | Capability | Status |
|--------|------------|--------|
| 3.1 | Document Processing | ✅ Completed |
| 3.2 | Intelligent Chunking | ✅ Completed |
| 3.3 | Embedding Generation | ✅ Completed |
| 3.4 | Semantic Search | ✅ Completed |
| 3.5 | Engineering Retrieval | ✅ Completed |
| 3.6 | Frontend Integration | ✅ Completed |
| 3.7 | LLM Integration | ✅ Completed |
| 3.8 | Testing and Release Preparation | ✅ Completed |

---

# [0.2.0] — Backend Foundation

**Status:** ✅ Released  
**Released:** 30 June 2026

## Overview

Version **0.2.0** established the FastAPI backend foundation and connected the React frontend to real backend services.

## Added

- FastAPI backend.
- REST API architecture.
- Swagger/OpenAPI documentation.
- CORS configuration.
- File upload endpoint.
- Document listing endpoint.
- Service layer.
- API routing.
- Configuration module.
- Utility modules.
- Frontend integration.
- Automatic upload refresh.
- Engineering document management.
- Modular backend structure.

## Technical Impact

This release established a working backend communicating successfully with the frontend and prepared the project for document parsing and Retrieval-Augmented Generation in v0.3.0.

---

# [0.1.0] — Frontend Prototype

**Status:** ✅ Released  
**Released:** 30 June 2026

## Overview

Version **0.1.0** created the first interactive frontend prototype for the Power Electronics Reliability Copilot. The goal was to validate the intended user workflow and establish the visual structure of the application before implementing backend storage, RAG, graph reasoning or AI functionality.

## Added

- React application.
- TypeScript configuration.
- Vite development environment.
- Dashboard layout.
- Engineering dashboard UI.
- Document upload interface.
- Uploaded filename display using React state.
- Reliability question panel.
- AI recommendation panel.
- Evidence panel.
- Graph context panel.
- Initial Engineering Copilot interface.
- Dedicated frontend folder.
- Prepared backend, graph, documents, docker, architecture and docs folders.
- Initial project documentation.

## Current Limitations at Release

- Uploaded files were not yet stored permanently.
- Upload functionality existed only in frontend state.
- No FastAPI backend integration.
- No document ingestion.
- No RAG pipeline.
- No Neo4j knowledge graph.
- No LangGraph orchestration.

## Technical Impact

This release established the user-facing foundation of the project and defined the intended workflow for uploading technical resources, asking reliability questions, reviewing AI recommendations, inspecting evidence and visualising graph context.

---

# Upcoming Releases

## v0.7.0 — Production Engineering and DevOps

**Status:** Planned

Planned capabilities:

- Docker containerisation.
- Azure Container Apps backend deployment.
- Azure Static Web Apps frontend deployment.
- Managed Identity for Azure-hosted backend services.
- Azure RBAC-based Blob Storage access.
- Removal of Azure Storage connection string dependency.
- CI/CD pipelines.
- Production deployment automation.
- Production monitoring and diagnostics.
- Operational reliability improvements.

## v1.0.0 — Enterprise AI Copilot

**Status:** Planned

Target milestone:

A production-ready Power Electronics Reliability Copilot featuring hybrid GraphRAG, explainable engineering reasoning, conversational interaction, cloud deployment and enterprise-grade architecture.
