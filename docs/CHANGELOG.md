# Changelog

All notable changes to the Power Electronics Reliability Copilot are documented in this file.

The project follows a release-based engineering methodology. Each release introduces a major architectural capability while preserving a stable and testable platform.

For implementation details, architectural decisions and engineering discussions, refer to:

- `PROJECT_ROADMAP.md`
- `PROJECT_METHODOLOGY.md`
- `ENGINEERING_PLAYBOOK.md`
- `development/v0.5_IMPLEMENTATION_LOG.md`

---

# [Unreleased]

## Current Focus

## v0.6.0 Progress — Azure Cloud Deployment

### Added

- Azure Blob Storage provider integration for uploaded engineering documents.
- Azure infrastructure automation under `infra/azure/powershell`.
- Secure local Azure configuration under `infra/azure/env`.
- Idempotent deployment scripts for resource group, storage, Key Vault, backend placeholder, frontend placeholder and complete deployment.
- Azure cleanup script for cost-controlled development.
- Azure infrastructure test suite under `infra/azure/tests`.
- Storage connection validation test.
- Blob upload validation test.
- Blob list validation test.
- Blob download validation test.
- Full Azure infrastructure test runner.

### Validated

- Azure CLI login with tenant-specific authentication.
- Resource Group creation.
- Storage Account creation.
- Blob Container creation.
- Key Vault creation.
- Frontend upload to Azure Blob Storage.
- Uploaded PDF confirmed in Azure Blob Storage.
- Azure Blob upload/list/download tests passing.

### Security and Cost Control

- Secrets are excluded from Git.
- Connection strings are retrieved securely and not printed by scripts.
- Local Azure configuration is excluded from Git.
- Cleanup script removes the development resource group after experiments.

### Next

- Azure OpenAI resource creation.
- Chat model deployment.
- Embedding model deployment.
- Backend configuration switch from OpenAI to Azure OpenAI.

## v0.6.0 — Azure Cloud Deployment (Progress)

## Current Focus

**Version 0.6.0 — Azure Cloud Deployment**

Current work focuses on moving the local engineering application towards Azure cloud deployment while preserving the existing evidence-backed reasoning workflow.

Progress completed:

- Cloud-ready backend configuration added.
- AI provider abstraction introduced for OpenAI and future Azure OpenAI support.
- Document storage provider abstraction introduced.
- Local storage and Azure Blob Storage providers implemented.
- Azure CLI deployment scripts added under `infra/azure/powershell`.
- Secure local Azure configuration added under `infra/azure/env`.
- Azure Resource Group automation added.
- Azure Storage Account and Blob Container automation added.
- Azure Key Vault automation scaffold added.
- Deployment wrapper scripts added for cloud foundation, backend, frontend and complete deployment.
- Cleanup script added to remove Azure resources after experiments and control cloud cost.
- Azure Blob Storage integration tested successfully with frontend upload.
- Uploaded engineering document confirmed in Azure Blob Storage.

Next work:

- Azure OpenAI resource creation and model deployment.
- Azure Key Vault secret integration.
- Backend deployment to Azure Container Apps.
- Frontend deployment to Azure Static Web Apps.
- Azure Monitor and Application Insights.
- End-to-end cloud validation.


### v0.6.0 — Azure Cloud Deployment

✅ Cloud configuration
✅ AI provider abstraction
✅ Storage provider abstraction
✅ Azure CLI login working
✅ Resource Group created
✅ Azure Storage Account created
✅ Blob Container created
✅ Key Vault created
✅ Azure deployment scripts working
✅ 10-deploy-complete.ps1 working

Next:
➡️ Connect backend upload to live Azure Blob Storage
➡️ Azure OpenAI resource + deployments
➡️ Key Vault secret storage
➡️ Azure Container Apps backend deployment
➡️ Azure Static Web Apps frontend deployment
➡️ Azure Monitor / Application Insights
➡️ End-to-end cloud validation

###

✅ Cloud configuration (done)
✅ AI provider abstraction (done)
Azure Blob Storage integration

Previously:

file_service
      │
      ▼
write_bytes()

Now:

file_service
      │
      ▼
DocumentStorageService
      │
      ▼
Storage Provider
      │
      ├── Local Storage   ✓
      └── Azure Blob      (later)

Azure Container Apps deployment
Azure Static Web Apps
Azure Monitor & Application Insights
Azure Key Vault
End-to-end deployment
GitHub Actions (v0.7.0)
AKS / Kubernetes (v0.7.0)

**Version 0.6.0 — Azure Cloud Deployment**

Current work focuses on:

- Azure deployment preparation
- Cloud configuration
- Azure OpenAI integration
- Cloud storage planning
- Deployment documentation
- Preparing the project for scalable hosted use
---

# [v0.5.2] — Professional Engineering Workspace

**Status:** ✅ Completed

---

## Added

### Conversation Memory

- Backend conversation history support
- Context-aware follow-up questions
- Conversation history passed into engineering reasoning prompts
- Local handling for previous-question requests
- Copy selected answer functionality
- Markdown conversation export

---

### Document Registry

- Document Registry Service
- `/documents` registry endpoint returning frontend-ready document records
- Stable document identifiers
- Pipeline-compatible document ID mapping
- Active engineering document display
- Document selection from the frontend UI

---

### Workspace Refinement

- Active document selection persisted in local storage
- Selected document shown in the conversation header
- Improved conversation memory status display
- Cleaner document registry panel
- Improved frontend integration with backend document metadata

---

## Fixed

- Neo4j `DateTime` serialization issue in graph/evidence responses
- JSON-safe evidence preparation for frontend/API responses
- Backend response stability for graph metadata

---

## Testing

Validated:

- Active document selection
- Document selection persistence after refresh
- Context-aware follow-up questions
- Previous-question listing
- Engineering Copilot API integration
- Frontend production build
- Backend regression suite

Current regression status:

- Backend regression tests: **20 / 20 passing**
- Frontend production build: **Passing**

---

## Changed

- Frontend no longer relies on manually entering `DOC-B3198A5`.
- Engineering Copilot requests now use the selected active document.
- Document handling moved toward a registry-based workflow.
- v0.5.2 scope was simplified to complete the end-to-end MVP before Azure deployment.

---

## Internal Milestones

| Task | Capability | Status |
|------|------------|--------|
| 5.2.1 | Conversation Memory Foundation | ✅ |
| 5.2.2 | JSON-safe Evidence Serialization | ✅ |
| 5.2.3 | Document Registry Integration | ✅ |
| 5.2.4 | Active Document Selection | ✅ |
| 5.2.5 | Final Workspace Validation | ✅ |

Version 0.5.2 completes the professional engineering workspace refinement before cloud deployment.

---

# [v0.5.1] — Conversational Engineering Copilot

**Status:** ✅ Completed

---

## Added

### Conversational Engineering Workspace

- Three-panel engineering workspace
- Modern conversational engineering interface
- Multi-turn engineering conversations
- Conversation history
- Clear Conversation functionality
- Active answer selection
- Collapsible engineering responses
- Question numbering
- Answer numbering
- Conversation timestamps

---

### Evidence Workspace

- Sticky Evidence panel
- Sticky Documents panel
- Evidence synchronisation with selected response
- Active evidence switching
- Evidence summary cards
- Question preview within Evidence panel
- Evidence statistics
- Citation summary
- Knowledge Graph summary
- Automatic evidence scrolling

---

### User Experience

- Responsive engineering dashboard
- Improved workspace layout
- Engineering report presentation
- Better navigation for long conversations
- Persistent engineering investigation workflow
- Improved frontend responsiveness
- Stable production build

---

### Frontend Integration

- Full integration with the Engineering Copilot API
- Structured rendering of engineering responses
- Session-based conversation management
- Improved evidence rendering
- Enhanced engineering report formatting

---

### Documentation

Updated project documentation including:

- README
- CHANGELOG
- Version 0.5.1 Release Notes
- Version 0.5.2 Planning
- Development documentation

---

## Changed

- Frontend redesigned into a conversational engineering workspace.
- Engineering responses now support multi-turn interaction.
- Evidence panel dynamically follows the selected engineering response.
- Conversation workflow redesigned for engineering investigations.
- Navigation significantly improved for long engineering sessions.
- Frontend architecture prepared for conversation-aware backend integration.

---

## Internal Milestones

| Task | Capability | Status |
|------|------------|--------|
| 5.1.1 | Conversational Workspace | ✅ |
| 5.1.2 | Multi-turn Conversation | ✅ |
| 5.1.3 | Conversation History | ✅ |
| 5.1.4 | Active Answer Selection | ✅ |
| 5.1.5 | Collapsible Responses | ✅ |
| 5.1.6 | Sticky Workspace Panels | ✅ |
| 5.1.7 | Evidence Synchronisation | ✅ |
| 5.1.8 | Improved Evidence Cards | ✅ |
| 5.1.9 | Question & Timestamp Metadata | ✅ |
| 5.1.10 | Workspace Refinement | ✅ |

Version 0.5.1 establishes the complete conversational engineering interface and prepares the project for context-aware engineering investigations in Version 0.5.2.

---

# [v0.5.0] — Evidence-backed Engineering Copilot

**Status:** ✅ Release Candidate (Backend Complete)

---

## Added

### Engineering Knowledge

- Engineering knowledge extraction
- Graph-ready JSON generation
- Entity extraction
- Relationship extraction
- Engineering ontology refinement
- Neo4j graph population
- Graph validation services

---

### Knowledge Graph Retrieval

- Knowledge Graph retrieval services
- Graph summary API
- Entity retrieval API
- Relationship retrieval API
- Knowledge graph search
- Relationship filtering
- Neighbour exploration
- Evidence retrieval

---

### Evidence-backed AI Reasoning

- Hybrid semantic and graph retrieval
- Engineering reasoning context builder
- Evidence ranking and deduplication
- Graph evidence preparation
- Prompt modularisation
- Evidence-backed reasoning
- Explainable engineering responses
- Confidence-aware recommendations

---

### Engineering Copilot

- Engineering Copilot service
- Engineering Copilot REST API
- Structured Pydantic response models
- Engineering metadata models
- Citation generation
- Typed API contracts
- End-to-end reasoning pipeline
- Swagger validation
- Backend integration

---

### Backend Quality Improvements

- Dedicated Evidence Preparation Service
- Dedicated Citation Service
- Custom project exceptions
- Structured logging
- Improved service separation
- Cleaner orchestration layer
- Improved maintainability
- Better API documentation

---

### Testing

Added automated validation for:

- Knowledge Graph Retrieval APIs
- Evidence-backed Reasoning APIs
- Engineering Copilot APIs
- Negative validation scenarios
- Backend regression testing

Current regression status:

- Knowledge Graph Retrieval: **10 / 10**
- Evidence-backed Reasoning: **5 / 5**
- Engineering Copilot: **5 / 5**

**Total: 20 / 20 automated backend tests passing**

---

### Documentation

Updated project documentation including:

- README
- CHANGELOG
- PROJECT_ROADMAP
- PROJECT_METHODOLOGY
- ENGINEERING_PLAYBOOK
- SYSTEM_ARCHITECTURE
- INGESTION_ARCHITECTURE
- KNOWLEDGE_GRAPH_ARCHITECTURE
- RETRIEVAL_ARCHITECTURE
- AI_REASONING_ARCHITECTURE
- Version 0.5 Implementation Log
- Version 0.5 Release Notes

---

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

---

## Internal Milestones

| Task | Capability | Status |
|------|------------|--------|
| 5.1 | Knowledge Document Registration | ✅ |
| 5.2 | Document Chunking | ✅ |
| 5.3 | Embedding Generation | ✅ |
| 5.4 | FAISS Vector Index | ✅ |
| 5.5 | Semantic Retrieval | ✅ |
| 5.6 | Retrieval Service | ✅ |
| 5.7 | Ingestion Pipeline | ✅ |
| 5.8 | Engineering Knowledge Extraction | ✅ |
| 5.9 | Knowledge Graph Population | ✅ |
| 5.10 | Knowledge Graph Retrieval | ✅ |
| 5.11 | Evidence-backed AI Reasoning | ✅ |
| 5.12 | Engineering Copilot Backend | ✅ |
| 5.13 | Backend Refinement & Release Preparation | ✅ |

Detailed implementation information is available in:

`development/v0.5_IMPLEMENTATION_LOG.md`

---

# [v0.4.0] — Knowledge Graph Foundation

**Status:** ✅ Released

## Added

### Engineering Ontology

- Engineering ontology design
- Node definitions
- Relationship definitions
- Property model
- Identifier strategy

### Neo4j Integration

- Neo4j graph database
- Constraints
- Indexes
- Graph schema
- Graph validation

### Knowledge Graph

- Engineering entity model
- Relationship model
- Seed dataset
- Cypher query library
- Graph inspection
- Graph statistics

### GraphRAG Preparation

- Graph-ready architecture
- Retrieval workflow
- Source tracking
- Chunk linkage
- Embedding strategy

### Documentation

- Architecture documentation
- Ontology documentation
- Repository structure
- ADR framework
- Standards

---

# [v0.3.0] — Engineering Knowledge Retrieval

**Status:** ✅ Released

## Added

### Document Processing

- PDF ingestion
- TXT ingestion
- CSV ingestion
- Automatic parsing
- Metadata generation

### Semantic Retrieval

- Document chunking
- Embedding generation
- FAISS indexing
- Semantic similarity search
- Retrieval-Augmented Generation
- Source attribution
- Confidence estimation

### AI Integration

- OpenAI integration
- Engineering prompt generation
- Evidence-backed responses

### Validation

- API testing
- End-to-end workflow validation
- Pytest integration

---

# [v0.2.0] — Backend Foundation

**Status:** ✅ Released

## Added

- FastAPI backend
- REST API architecture
- Document upload
- Document management
- Modular backend
- Swagger documentation

---

# [v0.1.0] — Frontend Prototype

**Status:** ✅ Released

## Added

- React application
- TypeScript
- Engineering dashboard
- Document upload interface
- AI response panel
- Evidence panel
- Initial Engineering Copilot interface

---

# Upcoming Releases

## v0.6.0 — Azure Cloud Deployment

Planned

- Azure deployment
- Azure OpenAI integration
- Cloud configuration
- Cloud storage
- Monitoring and logging

---

## v0.7.0 — Production Deployment

Planned

- Docker
- Kubernetes
- CI/CD
- Production deployment

---

## v1.0.0 — Enterprise AI Copilot

Planned

Production-ready Power Electronics Reliability Copilot featuring hybrid GraphRAG, explainable engineering reasoning, conversational interaction, cloud deployment and enterprise-grade architecture.