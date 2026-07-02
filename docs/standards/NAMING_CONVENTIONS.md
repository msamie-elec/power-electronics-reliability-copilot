# Naming Conventions

## Purpose

Defines naming standards for the repository.

---

# Directories

Use lowercase.

Example

graph

backend

frontend

documents

---

# Markdown Files

Architecture documents

UPPER_CASE

Example

POWER_ELECTRONICS_GRAPH_SCHEMA.md

Implementation guides

Title_Case

Example

Knowledge_Ingestion_Design.md

---

# Cypher Files

snake_case

Example

constraints.cypher

seed_graph.cypher

engineering_queries.cypher

---

# Neo4j Labels

PascalCase

Examples

Component

FailureMechanism

DocumentEvidence

---

# Relationships

UPPER_SNAKE_CASE

Examples

CONTAINS

SUPPORTS

PRODUCES

RESULTS_IN

---

# Properties

camelCase

Examples

componentId

failureId

sourceDocument

chunkId

---

# Variables

Lower camelCase

Example

component

failureMode

stressFactor

testMethod

---

# IDs

Use prefixes.

Component

C001

SubComponent

SC001

Material

MT001

Failure Mechanism

M001

Failure Mode

FM001

Symptom

SY001

Test Method

TM001

Maintenance Action

MA001

Document Chunk

CH000001