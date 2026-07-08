# Azure Deployment Mapping

## Status

Planned for Version 0.6.0

---

# Purpose

This document maps every major component of the current local application to its corresponding Azure service.

Rather than redesigning the application, Version 0.6.0 deploys the existing architecture to Microsoft Azure while preserving functionality and engineering workflows.

---

# Deployment Mapping

| Local Component | Azure Service |
|----------------|---------------|
| React Frontend | Azure Static Web Apps |
| FastAPI Backend | Azure Container Apps |
| OpenAI API | Azure OpenAI |
| Uploaded Documents | Azure Blob Storage |
| Neo4j Aura | Neo4j Aura (unchanged) |
| Environment Variables | Azure Key Vault + Container Apps |
| Backend Logs | Azure Monitor |
| Application Telemetry | Application Insights |

---

# Frontend

Repository

frontend/

↓

Azure Static Web Apps

Responsibilities

- Host React application
- Serve engineering workspace
- Call backend APIs

---

# Backend

Repository

backend/

↓

Azure Container Apps

Responsibilities

- Engineering Copilot API
- Knowledge Graph APIs
- Document APIs
- Retrieval APIs
- Evidence reasoning

---

# AI Services

Current

OpenAI API

↓

Azure OpenAI

Responsibilities

- GPT reasoning
- Embeddings
- Future model upgrades

---

# Document Storage

Current

backend/uploads/

↓

Azure Blob Storage

Responsibilities

- Uploaded engineering documents
- Future engineering datasets
- Durable storage

---

# Knowledge Graph

Current

Neo4j Aura

↓

Neo4j Aura

No migration required.

---

# Secrets

Current

.env

↓

Azure Key Vault

Secrets include

- Azure OpenAI
- Neo4j
- Blob Storage
- Future service credentials

---

# Monitoring

Current

Local console logging

↓

Azure Monitor

Application Insights

Provides

- request tracing
- error logging
- performance metrics
- deployment diagnostics

---

# Deployment Philosophy

Version 0.6.0 intentionally changes infrastructure rather than application functionality.

The objective is to demonstrate cloud engineering by deploying the existing engineering platform without redesigning its internal architecture.

---

# Relationship to Version 0.7.0

After deployment is complete, Version 0.7.0 introduces production engineering:

- Docker
- Azure Container Registry
- GitHub Actions
- Kubernetes
- CI/CD
- Production monitoring
- Resource optimisation

Version 0.6.0 therefore serves as the cloud foundation for production engineering.