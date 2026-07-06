# Diagram 1 — Conceptual Engineering Ontology

## Purpose

Diagram 1 presents the conceptual engineering ontology for the Power Electronics Reliability Copilot.

The purpose of this diagram is to show the main engineering concepts in the reliability domain and how they are semantically connected before any database-specific implementation details are introduced.

This diagram answers the question:

> What engineering concepts exist in the domain, and how are they related?

It does not show Neo4j labels, properties, indexes, constraints, or real engineering instances. Those are introduced later in Diagram 2 and Diagram 3.

---

## Role in the Design Process

The conceptual ontology acts as the bridge between unstructured engineering knowledge and a structured knowledge graph.

Engineering documents describe reliability problems in natural language. The ontology converts that knowledge into a controlled set of concepts and relationships that can later be implemented in Neo4j.

The design flow is:

```text
Engineering knowledge
        ↓
Conceptual ontology
        ↓
Neo4j graph schema
        ↓
Populated knowledge graph
        ↓
GraphRAG and AI reasoning
````

---

## What the Diagram Represents

The diagram represents the reliability domain using the following concept groups:

### Physical Structure

* Component
* Sub-Component
* Material

These concepts describe the physical structure of a power electronics system.

### Operational and Stress Context

* Operating Condition
* Stress Factor

These concepts describe the conditions that increase the likelihood or rate of degradation.

### Reliability and Failure Behaviour

* Failure Mechanism
* Failure Mode
* Symptom

These concepts describe how degradation develops, how it appears as a failure, and how it becomes observable.

### Diagnosis and Maintenance

* Test Method
* Maintenance Action

These concepts describe how faults are verified and what corrective actions may be recommended.

### Evidence Layer

* Document Evidence

This concept represents engineering evidence extracted from documents, reports, manuals, datasheets, or research literature.

---

## Knowledge Representation

The diagram shows how engineering knowledge is represented as a network of connected concepts.

For example:

```text
Component
    CONTAINS
Sub-Component

Sub-Component
    EXPERIENCES
Failure Mechanism

Failure Mechanism
    RESULTS_IN
Failure Mode

Failure Mode
    PRODUCES
Symptom

Symptom
    VERIFIED_BY
Test Method

Test Method
    RECOMMENDS
Maintenance Action
```

This structure allows engineering knowledge to be represented as explicit, traceable relationships rather than isolated text.

---

## Evidence-Based Reasoning

The `Document Evidence` concept is included to show that engineering claims should be supported by source evidence.

For example, document evidence may support:

* a failure mechanism,
* a failure mode,
* a diagnostic test method.

This is important for future GraphRAG development because AI-generated answers should be grounded in both graph relationships and supporting source documents.

---

## Alignment with Neo4j

Diagram 1 is database-independent, but it directly informs the Neo4j implementation.

Each conceptual node in Diagram 1 later becomes a Neo4j node label in Diagram 2.

For example:

| Conceptual Diagram | Neo4j Schema              |
| ------------------ | ------------------------- |
| Component          | `Component` label         |
| Sub-Component      | `SubComponent` label      |
| Failure Mechanism  | `FailureMechanism` label  |
| Failure Mode       | `FailureMode` label       |
| Symptom            | `Symptom` label           |
| Test Method        | `TestMethod` label        |
| Maintenance Action | `MaintenanceAction` label |
| Document Evidence  | `DocumentEvidence` label  |

Similarly, each conceptual relationship becomes a Neo4j relationship type.

For example:

| Conceptual Relationship | Neo4j Relationship Type |
| ----------------------- | ----------------------- |
| CONTAINS                | `CONTAINS`              |
| HAS_MATERIAL            | `HAS_MATERIAL`          |
| EXPERIENCES             | `EXPERIENCES`           |
| RESULTS_IN              | `RESULTS_IN`            |
| PRODUCES                | `PRODUCES`              |
| VERIFIED_BY             | `VERIFIED_BY`           |
| RECOMMENDS              | `RECOMMENDS`            |
| SUPPORTS                | `SUPPORTS`              |

Therefore, Diagram 1 provides the conceptual foundation for the Neo4j graph schema.

---

## Why This Diagram Matters

This diagram is important because it separates engineering meaning from implementation details.

Without this conceptual layer, the project could become a collection of nodes and relationships without a clear engineering rationale.

With this ontology, the graph has a clear purpose:

* represent engineering knowledge explicitly,
* support reliability diagnosis,
* connect failures to causes, symptoms, tests, and maintenance,
* link engineering claims to evidence,
* prepare the system for GraphRAG and AI reasoning.

---

## Relationship to Other Diagrams

This diagram is the first of three modelling views.

| Diagram                                         | Purpose                                                           |
| ----------------------------------------------- | ----------------------------------------------------------------- |
| Diagram 1 — Conceptual Engineering Ontology     | Shows engineering concepts and semantic relationships             |
| Diagram 2 — Neo4j Graph Schema                  | Shows labels, properties, constraints, and implementation details |
| Diagram 3 — Engineering Knowledge Graph Example | Shows real engineering instances populated into the graph         |

Together, these diagrams represent the full modelling path from engineering knowledge to an enterprise AI-ready knowledge graph.

```
