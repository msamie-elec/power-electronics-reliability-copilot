# Diagram 3 — Engineering Knowledge Graph Example

## Purpose

Diagram 3 shows an example of a populated engineering knowledge graph.

Unlike Diagram 1, which defines the conceptual ontology, and Diagram 2, which defines the Neo4j graph schema, Diagram 3 demonstrates how real engineering entities can be represented as connected graph instances.

This diagram answers the question:

> What does the knowledge graph look like after engineering knowledge has been added?

---

## What the Diagram Represents

The diagram models a small IGBT reliability scenario.

It shows how an IGBT module is connected to its internal bond wire, how the bond wire is associated with aluminium material, how operating and stress conditions contribute to thermal cycling, and how thermal cycling may lead to bond wire lift-off.

The graph then continues through observable symptoms, diagnostic methods, maintenance actions, and supporting engineering evidence.

---

## Concept-to-Instance Mapping

| Diagram 1 Concept | Diagram 3 Instance |
|---|---|
| Component | IGBT Module |
| Sub-Component | Bond Wire |
| Material | Aluminium |
| Operating Condition | High Load Cycling |
| Stress Factor | Junction Temperature Variation |
| Failure Mechanism | Thermal Cycling |
| Failure Mode | Bond Wire Lift-off |
| Symptom | Rising VCE(sat) |
| Test Method | Electrical Parameter Monitoring |
| Maintenance Action | Inspect Thermal Interface Material |
| Document Evidence | Engineering Document |

---

## Knowledge Flow

The example graph follows the engineering reasoning chain:

```text
IGBT Module
    CONTAINS
Bond Wire
    HAS_MATERIAL
Aluminium

Bond Wire
    EXPERIENCES
Thermal Cycling

High Load Cycling
    INCREASES_RISK_OF
Thermal Cycling

Junction Temperature Variation
    ACCELERATES
Thermal Cycling

Thermal Cycling
    RESULTS_IN
Bond Wire Lift-off

Bond Wire Lift-off
    PRODUCES
Rising VCE(sat)

Rising VCE(sat)
    VERIFIED_BY
Electrical Parameter Monitoring

Electrical Parameter Monitoring
    RECOMMENDS
Inspect Thermal Interface Material
````

---

## Evidence Layer

The `Engineering Document` node represents the evidence source that supports selected engineering claims in the graph.

In this diagram it is intentionally generic. It does not represent a specific paper or handbook.

During later graph population and GraphRAG development, this node will be replaced by real evidence extracted from actual documents ingested into the system.

Example future evidence fields may include:

```text
documentId
chunkId
page
section
sourceTitle
```

---

## Why This Diagram Matters

This diagram demonstrates the transition from design to usable knowledge.

It shows how the ontology becomes a practical graph structure that can support engineering questions such as:

* What does the IGBT module contain?
* What material is the bond wire made from?
* What failure mechanism affects the bond wire?
* What failure mode results from thermal cycling?
* What symptom is produced by bond wire lift-off?
* What test method verifies the symptom?
* What maintenance action is recommended?
* What evidence supports the engineering claim?

These questions require graph traversal and are difficult to answer reliably using unstructured text alone.

---

## Alignment with Neo4j

Each node in Diagram 3 is an instance of a Neo4j label defined in Diagram 2.

For example:

| Diagram 3 Instance                 | Neo4j Label         |
| ---------------------------------- | ------------------- |
| IGBT Module                        | `Component`         |
| Bond Wire                          | `SubComponent`      |
| Aluminium                          | `Material`          |
| Thermal Cycling                    | `FailureMechanism`  |
| Bond Wire Lift-off                 | `FailureMode`       |
| Rising VCE(sat)                    | `Symptom`           |
| Electrical Parameter Monitoring    | `TestMethod`        |
| Inspect Thermal Interface Material | `MaintenanceAction` |
| Engineering Document               | `DocumentEvidence`  |

This makes Diagram 3 the instance-level view of the same ontology and schema.

---

## Relationship to the Sprint

Diagram 3 completes Sprint 4.3.1 by showing the third modelling layer:

| Diagram   | Modelling Level          | Purpose                                                        |
| --------- | ------------------------ | -------------------------------------------------------------- |
| Diagram 1 | Conceptual               | Defines engineering concepts and relationships                 |
| Diagram 2 | Logical / Schema         | Defines Neo4j labels, properties and relationship types        |
| Diagram 3 | Instance / Example Graph | Shows real engineering entities connected as a knowledge graph |

Together, the three diagrams provide a complete design path from engineering ontology to Neo4j implementation and example graph population.

```
```
