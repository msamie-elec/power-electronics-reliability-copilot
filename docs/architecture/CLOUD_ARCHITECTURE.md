# Cloud Architecture — Azure Deployment

## Status

**Planned for v0.6.0**

---

# Purpose

This document defines the target Azure cloud architecture for the Power Electronics Reliability Copilot.

The objective of Version **0.6.0 — Cloud-Native Azure Deployment** is to deploy the existing engineering application to Microsoft Azure without introducing major new AI functionality.

This architecture preserves the current system capabilities while introducing cloud-native deployment, secure configuration, managed storage, monitoring, and deployment readiness.

---

# Cloud Architecture Overview

```text
User
  │
  ▼
Azure Static Web Apps
React Frontend
  │
  ▼
Azure Container Apps
FastAPI Backend
  │
  ├───────────────► Azure OpenAI
  │
  ├───────────────► Azure Blob Storage
  │
  ├───────────────► Azure Key Vault
  │
  ├───────────────► Neo4j Aura
  │
  └───────────────► Azure Monitor / Application Insights
```

---

# Target Azure Services

| Capability              | Azure Service                            |
| ----------------------- | ---------------------------------------- |
| Frontend hosting        | Azure Static Web Apps                    |
| Backend hosting         | Azure Container Apps                     |
| LLM inference           | Azure OpenAI                             |
| Document storage        | Azure Blob Storage                       |
| Secrets management      | Azure Key Vault                          |
| Monitoring              | Azure Monitor                            |
| Application telemetry   | Application Insights                     |
| Knowledge Graph         | Neo4j Aura                               |
| Container image storage | Azure Container Registry later in v0.7.0 |

---

# Frontend Deployment

The React + TypeScript frontend will be deployed using **Azure Static Web Apps**.

Responsibilities:

* host the compiled frontend;
* serve the engineering workspace;
* call the deployed FastAPI backend;
* provide a lightweight cloud-hosted user interface.

---

# Backend Deployment

The FastAPI backend will be deployed using **Azure Container Apps**.

Responsibilities:

* expose the Engineering Copilot API;
* handle document upload and registry operations;
* perform evidence-backed reasoning;
* connect to Azure OpenAI;
* connect to Azure Blob Storage;
* connect to Neo4j Aura;
* provide API responses to the frontend.

Azure Container Apps is selected because it creates a clean bridge between v0.6.0 cloud deployment and v0.7.0 containerisation / production engineering.

---

# Azure OpenAI

Azure OpenAI will provide the LLM capability used by the Engineering Copilot.

The backend will use Azure-hosted model endpoints instead of local OpenAI API configuration.

Required configuration:

* Azure OpenAI endpoint
* deployment name
* API version
* API key or managed identity configuration

---

# Azure Blob Storage

Azure Blob Storage will store uploaded engineering documents.

Responsibilities:

* store uploaded PDF, TXT and CSV files;
* provide durable cloud storage;
* replace local-only uploaded document storage;
* support future production document management.

---

# Azure Key Vault

Azure Key Vault will manage sensitive configuration.

Secrets may include:

* Azure OpenAI keys;
* storage connection strings;
* Neo4j credentials;
* backend configuration values.

This avoids storing secrets directly in source code or local configuration files.

---

# Neo4j Aura

The existing Neo4j Aura knowledge graph remains the graph database.

The backend connects to Neo4j Aura through secure environment configuration.

Responsibilities:

* store engineering entities;
* store engineering relationships;
* support Knowledge Graph retrieval;
* support evidence-backed reasoning.

---

# Monitoring and Diagnostics

Azure Monitor and Application Insights will be used to observe the deployed application.

Monitoring will include:

* backend health;
* API request behaviour;
* application errors;
* latency;
* deployment verification;
* operational diagnostics.

---

# Environment Configuration

The cloud deployment will require environment-aware configuration.

Local development will continue to use local `.env` files.

Azure deployment will use:

* Azure Container Apps environment variables;
* Azure Key Vault;
* Azure Static Web Apps configuration;
* Azure service connection settings.

---

# Security Principles

The cloud deployment will follow these principles:

* no secrets committed to GitHub;
* HTTPS-only access;
* secrets managed through Azure Key Vault;
* least-privilege service access where possible;
* separation of local and cloud configuration;
* clear environment variable naming.

---

# Deployment Strategy

Version **0.6.0** will deploy the existing application in a controlled way.

The release will focus on:

* deploying the frontend;
* deploying the backend;
* connecting backend services to Azure;
* validating end-to-end cloud behaviour;
* documenting deployment configuration.

The purpose is not to redesign the application, but to make the current system cloud-hosted and operational.

---

# Out of Scope for v0.6.0

The following are intentionally deferred to Version **0.7.0**:

* Kubernetes;
* Azure Kubernetes Service;
* production CI/CD;
* advanced autoscaling;
* full container orchestration;
* load testing;
* production hardening;
* enterprise authentication.

---

# Success Criteria

Version **0.6.0** will be considered successful when:

* the React frontend is deployed to Azure;
* the FastAPI backend is deployed to Azure;
* the frontend can call the cloud backend;
* Azure OpenAI is used by the backend;
* engineering documents can be stored or prepared for Blob Storage;
* secrets are removed from local-only configuration;
* monitoring is available;
* the application works end-to-end in the cloud.

---

# Relationship to v0.7.0

Version **0.6.0** establishes the cloud deployment baseline.

Version **0.7.0** will build on this foundation by introducing production engineering and DevOps capabilities:

* Docker;
* Azure Container Registry;
* GitHub Actions;
* CI/CD;
* AKS;
* scaling;
* production monitoring;
* resource management.

---

# Summary

This cloud architecture moves the Power Electronics Reliability Copilot from a local engineering AI application into an Azure-hosted cloud solution.

It preserves the existing evidence-backed reasoning workflow while introducing cloud deployment, managed storage, secure configuration and monitoring.

This provides the foundation for the production engineering work planned in Version **0.7.0**.

