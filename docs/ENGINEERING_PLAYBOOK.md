# Engineering Playbook

## Purpose

The Engineering Playbook defines the engineering conventions, development standards, and software practices followed throughout the Power Electronics Reliability Copilot project.

Its purpose is to ensure that new functionality is implemented consistently, remains maintainable, and aligns with the overall system architecture.

This document complements the project methodology by describing the practical engineering standards applied during development.

---

# Engineering Principles

Development follows a number of fundamental engineering principles.

- Build modular software.
- Keep components loosely coupled.
- Separate responsibilities clearly.
- Prefer simple solutions over unnecessary complexity.
- Extend existing architecture rather than redesigning it.
- Maintain backward compatibility whenever practical.
- Keep documentation aligned with implementation.
- Validate new functionality through testing.

---

# Repository Organisation

The repository is organised into independent functional areas.

```text
backend/
frontend/
graph/
documents/
docker/
docs/
```

Each directory has a clearly defined responsibility and should evolve independently.

---

# Backend Architecture

Backend services follow a layered architecture.

```text
API Layer
      │
      ▼
Service Layer
      │
      ▼
Processing Layer
      │
      ▼
Persistence Layer
```

Responsibilities are separated as follows.

| Layer | Responsibility |
|---------|----------------|
| API | HTTP endpoints |
| Service | Business logic |
| Processing | AI, graph and retrieval workflows |
| Persistence | Files, vector store, graph database |

Business logic should remain inside services rather than API routes.

---

# API Design

REST APIs follow consistent conventions.

- Resource-oriented endpoints
- JSON request and response bodies
- Appropriate HTTP status codes
- Structured error responses
- OpenAPI documentation
- Request validation
- Response validation

API endpoints should remain lightweight and delegate processing to service classes.

---

# Service Design

Each service should have a single responsibility.

Examples include:

- Document Service
- Retrieval Service
- Knowledge Graph Service
- Evidence Reasoning Service
- Engineering Copilot Service

Services should avoid direct dependencies on unrelated components.

---

# Knowledge Graph Standards

Engineering knowledge is represented using Neo4j.

Development principles include:

- meaningful node labels
- consistent relationship naming
- graph validation
- ontology-first modelling
- idempotent graph population using MERGE
- evidence traceability

Graph schema changes should preserve existing engineering knowledge wherever practical.

---

# Retrieval Standards

Retrieval should prioritise engineering evidence rather than AI generation.

Preferred workflow:

```text
Question
     │
     ▼
Semantic Retrieval
     │
     ▼
Knowledge Graph Retrieval
     │
     ▼
Evidence Assembly
     │
     ▼
LLM Reasoning
```

The language model should reason over retrieved evidence rather than generate unsupported information.

---

# Prompt Engineering

Prompt templates are stored separately from application logic.

Benefits include:

- reuse
- consistency
- maintainability
- version control

Prompt construction should remain deterministic whenever practical.

---

# Testing Standards

Backend functionality should be accompanied by automated tests.

Testing includes:

- API tests
- service tests
- retrieval validation
- graph validation
- evidence reasoning validation
- negative test cases

Tests should never expose:

- API keys
- credentials
- environment variables
- confidential engineering data

Security is considered part of testing.

---

# Documentation Standards

Documentation evolves alongside implementation.

The repository separates documentation into dedicated categories.

| Document | Purpose |
|----------|---------|
| README | Project overview |
| Roadmap | Product evolution |
| Methodology | Engineering process |
| Playbook | Engineering standards |
| Architecture | System design |
| Releases | Version history |
| Development | Implementation history |

Documentation should explain engineering decisions rather than duplicate source code.

---

# Naming Conventions

Development follows consistent naming conventions.

Examples include:

- descriptive class names
- descriptive service names
- meaningful endpoint names
- clear variable names
- explicit function names

Abbreviations should be avoided unless widely recognised within the engineering domain.

---

# Security Principles

Engineering software should minimise unnecessary exposure of information.

Examples include:

- never commit secrets
- never expose credentials
- avoid logging confidential data
- validate user input
- use environment variables for configuration
- avoid revealing internal implementation details through API responses

Security reviews should accompany significant architectural changes.

---

# Versioning

Development follows release-based versioning.

Each release:

- introduces one major capability;
- remains stable;
- is fully documented;
- provides a foundation for the following release.

---

# Continuous Improvement

The playbook evolves throughout the project.

New engineering practices may be incorporated as the platform grows, provided they improve software quality without compromising architectural consistency.

---

# Summary

The Engineering Playbook provides a common set of engineering standards that guide development across the project.

Following these conventions promotes consistency, maintainability, explainability, and long-term scalability while allowing the platform to evolve through successive engineering releases.