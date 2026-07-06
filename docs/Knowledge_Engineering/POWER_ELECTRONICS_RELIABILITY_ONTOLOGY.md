# Power Electronics Reliability Ontology

## Sprint 4.2 — Ontology Design

## Purpose

This document defines the first knowledge graph ontology for the Power Electronics Reliability Copilot.

The ontology describes the engineering concepts, relationships, and properties required to support reliability diagnosis, GraphRAG, and explainable AI recommendations.

---

POWER_ELECTRONICS_RELIABILITY_ONTOLOGY.md

1. Purpose
2. Scope
3. Design Principles
4. Core Node Labels
5. Core Relationships
6. Node Properties
7. Relationship Properties
8. Naming Conventions
9. Example Graph
10. MVP Scope
11. Future Extensions
12. Design Decisions
13. Sprint 4.2 Success Criteria
14. References

Delievered in twp steps:
Step 1: Nodes and Relationships (sections 1 to 6)
Step 2: Node Properties (sections 7 to 8)
Steps 3: Additional Details (sections 9 to 14)

---
# Step 1: Nodes and Relationships (sections 1 to 6)
# 1. Core Node Labels

| Node Label | Purpose | Example |
|---|---|---|
| `Component` | Main engineering component or system element | IGBT Module |
| `SubComponent` | Smaller part inside a component | Bond Wire |
| `FailureMode` | Observable way a component fails | Bond Wire Fatigue |
| `FailureMechanism` | Physical process causing degradation | Thermal Cycling |
| `StressFactor` | Stress that contributes to degradation | Junction Temperature Variation |
| `Symptom` | Observable sign of failure | Rising VCE(sat) |
| `TestMethod` | Test or diagnostic method | Electrical Parameter Monitoring |
| `MaintenanceAction` | Recommended inspection or corrective action | Inspect Thermal Interface Material |
| `Material` | Material involved in failure behaviour | Solder Layer |
| `OperatingCondition` | Usage or mission condition | High Load Cycling |
| `DocumentEvidence` | Source evidence from documents or chunks | Reliability Handbook Chunk |

---

# 2. Core Relationships

| Relationship | From | To | Meaning |
|---|---|---|---|
| `HAS_SUBCOMPONENT` | `Component` | `SubComponent` | Component contains a smaller part |
| `HAS_FAILURE_MODE` | `Component` | `FailureMode` | Component can fail in this way |
| `CAUSED_BY` | `FailureMode` | `FailureMechanism` | Failure mode is caused by a mechanism |
| `TRIGGERED_BY` | `FailureMechanism` | `StressFactor` | Stress contributes to the mechanism |
| `OBSERVED_AS` | `FailureMode` | `Symptom` | Failure appears as a symptom |
| `DETECTED_BY` | `Symptom` | `TestMethod` | Test can detect the symptom |
| `MITIGATED_BY` | `FailureMode` | `MaintenanceAction` | Action reduces or addresses the failure |
| `AFFECTS` | `StressFactor` | `Component` | Stress affects a component |
| `INVOLVES_MATERIAL` | `FailureMechanism` | `Material` | Mechanism involves a material |
| `OPERATES_UNDER` | `Component` | `OperatingCondition` | Component operates under a condition |
| `SUPPORTED_BY` | `FailureMode` | `DocumentEvidence` | Evidence supports the diagnosis |

---

# 3. Initial MVP Scope

The first ontology focuses on IGBT power module reliability.

## Included Concepts

- IGBT module
- Bond wire
- Solder layer
- Thermal interface material
- Thermal cycling
- Junction temperature variation
- Bond wire fatigue
- Solder fatigue
- Rising VCE(sat)
- Temperature warning
- Electrical parameter monitoring
- Thermal inspection
- Maintenance action
- Document evidence

---

# 4. Example Graph Sketch

```text
Component: IGBT Module
    ├── HAS_SUBCOMPONENT → SubComponent: Bond Wire
    ├── HAS_SUBCOMPONENT → SubComponent: Solder Layer
    ├── HAS_FAILURE_MODE → FailureMode: Bond Wire Fatigue
    │       ├── CAUSED_BY → FailureMechanism: Thermal Cycling
    │       │       └── TRIGGERED_BY → StressFactor: Junction Temperature Variation
    │       ├── OBSERVED_AS → Symptom: Rising VCE(sat)
    │       ├── DETECTED_BY → TestMethod: Electrical Parameter Monitoring
    │       ├── MITIGATED_BY → MaintenanceAction: Inspect Thermal Interface Material
    │       └── SUPPORTED_BY → DocumentEvidence: Reliability Handbook Chunk
    └── OPERATES_UNDER → OperatingCondition: High Load Cycling
```

---

# 5. Naming Conventions

| Element            | Convention                 | Example          |
| ------------------ | -------------------------- | ---------------- |
| Node labels        | CamelCase                  | `FailureMode`    |
| Relationship types | UPPERCASE_WITH_UNDERSCORES | `CAUSED_BY`      |
| Properties         | lowerCamelCase             | `sourceDocument` |

---

# 6. Sprint 4.2 Success Criteria

Sprint 4.2 is complete when:

* Core node labels are defined.
* Core relationships are defined.
* MVP IGBT reliability scope is agreed.
* Example graph sketch is documented.
* Ontology is ready for Arrows.app visual modelling.
* Ontology is ready for Cypher seed data in Sprint 4.3.

```

This is the **Markdown ontology table**. Next we can refine the node properties table before moving to Arrows.app.
```

---

# Step 2 — Node Properties
The ontology we created defines what entities exist. The next step defines what information each entity stores.

This is equivalent to designing tables and columns in a relational database—but much richer because everything is connected.

Add the following section to your ontology document.

---

# 7. Node Properties

## Component

| Property      | Type    | Description             | Example                |
| ------------- | ------- | ----------------------- | ---------------------- |
| componentId   | String  | Unique identifier       | C001                   |
| name          | String  | Component name          | IGBT Module            |
| category      | String  | Component category      | Power Semiconductor    |
| manufacturer  | String  | Manufacturer            | Infineon               |
| voltageRating | Integer | Rated voltage (V)       | 1200                   |
| currentRating | Integer | Rated current (A)       | 600                    |
| description   | String  | Engineering description | High-power IGBT module |

---

## SubComponent

| Property       | Type   | Description          | Example               |
| -------------- | ------ | -------------------- | --------------------- |
| subComponentId | String | Unique identifier    | SC001                 |
| name           | String | Name                 | Bond Wire             |
| material       | String | Material             | Aluminium             |
| function       | String | Engineering function | Electrical connection |

---

## FailureMode

| Property    | Type    | Description           | Example                             |
| ----------- | ------- | --------------------- | ----------------------------------- |
| failureId   | String  | Unique identifier     | FM001                               |
| name        | String  | Failure mode          | Bond Wire Fatigue                   |
| severity    | Integer | Severity (1–10)       | 9                                   |
| probability | Float   | Estimated probability | 0.73                                |
| description | String  | Description           | Fatigue crack develops in bond wire |

---

## FailureMechanism

| Property    | Type   | Description                    | Example                            |
| ----------- | ------ | ------------------------------ | ---------------------------------- |
| mechanismId | String | Unique identifier              | M001                               |
| name        | String | Mechanism                      | Thermal Cycling                    |
| physics     | String | Underlying physical phenomenon | Thermomechanical fatigue           |
| description | String | Description                    | Repeated expansion and contraction |

---

## StressFactor

| Property     | Type   | Description       | Example                        |
| ------------ | ------ | ----------------- | ------------------------------ |
| stressId     | String | Unique identifier | ST001                          |
| name         | String | Stress factor     | Junction Temperature Variation |
| unit         | String | Engineering unit  | °C                             |
| typicalRange | String | Operating range   | 40–150 °C                      |

---

## Symptom

| Property    | Type    | Description       | Example                                          |
| ----------- | ------- | ----------------- | ------------------------------------------------ |
| symptomId   | String  | Unique identifier | SY001                                            |
| name        | String  | Symptom           | Rising VCE(sat)                                  |
| measurable  | Boolean | Can be measured   | True                                             |
| description | String  | Description       | Increase in collector-emitter saturation voltage |

---

## TestMethod

| Property  | Type   | Description        | Example                         |
| --------- | ------ | ------------------ | ------------------------------- |
| testId    | String | Unique identifier  | TM001                           |
| name      | String | Test name          | Electrical Parameter Monitoring |
| equipment | String | Equipment required | Power Analyzer                  |
| duration  | String | Typical duration   | 30 min                          |

---

## MaintenanceAction

| Property | Type   | Description          | Example                            |
| -------- | ------ | -------------------- | ---------------------------------- |
| actionId | String | Unique identifier    | MA001                              |
| name     | String | Maintenance action   | Inspect Thermal Interface Material |
| priority | String | Priority             | High                               |
| interval | String | Recommended interval | Every 12 months                    |

---

## Material

| Property     | Type   | Description                     | Example |
| ------------ | ------ | ------------------------------- | ------- |
| materialId   | String | Unique identifier               | MT001   |
| name         | String | Material                        | Solder  |
| type         | String | Material type                   | SAC305  |
| conductivity | String | Thermal/electrical conductivity | High    |

---

## OperatingCondition

| Property           | Type    | Description              | Example           |
| ------------------ | ------- | ------------------------ | ----------------- |
| conditionId        | String  | Unique identifier        | OC001             |
| loadType           | String  | Operating load           | High Load Cycling |
| ambientTemperature | Integer | Ambient temperature (°C) | 45                |
| switchingFrequency | Integer | Frequency (Hz)           | 10000             |

---

## DocumentEvidence

| Property       | Type    | Description                | Example                                     |
| -------------- | ------- | -------------------------- | ------------------------------------------- |
| chunkId        | String  | Chunk identifier           | doc_graph_chunk_000020                      |
| sourceDocument | String  | Source file                | Graph.pdf                                   |
| page           | Integer | Page number                | 12                                          |
| score          | Float   | Retrieval similarity score | 0.84                                        |
| text           | String  | Evidence text              | Thermal cycling causes bond wire fatigue... |

---

# 8. Relationship Properties

Unlike relational databases, relationships in Neo4j can also have their own properties.

| Relationship | Property       | Example    |
| ------------ | -------------- | ---------- |
| CAUSED_BY    | confidence     | 0.94       |
| CAUSED_BY    | evidenceCount  | 12         |
| TRIGGERED_BY | threshold      | ΔTj > 60°C |
| DETECTED_BY  | accuracy       | 92%        |
| SUPPORTED_BY | retrievalScore | 0.86       |
| MITIGATED_BY | effectiveness  | High       |

---

# Why this matters

Most tutorials stop at creating nodes and relationships. For a production-quality engineering knowledge graph, we also model the metadata associated with both nodes and relationships. This allows the graph to support richer queries, ranking, and explainable reasoning.

For example, instead of simply stating:

```
Bond Wire Fatigue
    CAUSED_BY
Thermal Cycling
```

we can capture additional context:

```
Bond Wire Fatigue
        |
        | CAUSED_BY
        | confidence = 0.94
        | evidenceCount = 12
        |
Thermal Cycling
```

This becomes valuable later when the AI needs to answer questions such as:

* "What is the most likely failure mechanism?"
* "How strong is the evidence?"
* "Which maintenance action has the highest effectiveness?"

These properties allow the graph to rank, filter, and explain its recommendations rather than simply listing connected nodes.

---

## What comes next

With the ontology and properties defined, the next deliverable is the **visual ontology diagram** in **Arrows.app**. We'll produce a professional graph model showing all node types, relationship types, and their connections. This diagram will become the blueprint for implementing the Neo4j schema and seed data in Sprint 4.3.


# Section 3:

### Why keep everything together?

This document is essentially the **requirements specification** for your graph database.

Later, when someone asks:

> "Why did you create a `FailureMechanism` node instead of storing it as a property?"

or

> "Why is `Thermal Cycling` a node?"

the answer is documented here.

This is exactly how enterprise architecture documents are maintained.

---

## I would also add three sections that most tutorials don't include

### 11. Future Extensions

Document what is intentionally **out of scope** for Sprint 4.2.

For example:

```markdown
## Future Extensions

The ontology will later be expanded to include:

- Converter Topologies
- Power Electronics Systems
- Cooling Systems
- Failure History
- Maintenance Records
- Sensor Measurements
- Inspection Images
- Operating Profiles
- Engineers
- Manufacturing Defects
- Simulation Results
- Reliability Standards
```

This shows reviewers that the MVP is deliberately scoped rather than incomplete.

---

### 12. Design Decisions

This is one of the most valuable sections.

For example:

```markdown
## Design Decisions

### Why is Thermal Cycling a node?

Thermal Cycling is represented as a node because multiple failure modes may share the same degradation mechanism.

### Why DocumentEvidence is a node?

Document evidence is represented separately to enable GraphRAG and explainable AI, allowing retrieved chunks to be linked directly to engineering concepts.

### Why relationships have properties?

Relationship properties store confidence scores, retrieval scores, and evidence counts, enabling explainable engineering recommendations.

### Why Component and SubComponent are separated?

This supports hierarchical graph traversal and reuse across multiple products.
```

This demonstrates architectural thinking, which interviewers value highly.

---

### 14. References

Keep a record of the sources that informed your ontology.

For example:

```markdown
## References

- Neo4j Graph Data Modeling Guidelines
- Neo4j GraphAcademy
- IEC Reliability Standards
- IEEE Power Electronics Society
- OpenAI GraphRAG Concepts
- LlamaIndex Documentation
- Enterprise Reliability Engineering Literature
```

---

## The final document

This serves as the **master design document** for the required knowledge graph.

It won't just be documentation—it will become the specification that drives:

* the Arrows.app diagram,
* the Neo4j schema,
* the Cypher seed scripts,
* the GraphRAG integration,
* and eventually the LangGraph agent.

That means **every subsequent graph-related artifact will trace back to this document**, making it one of the most important files in your repository.


# Updates:
The next step is to add the missing **Design Principles**, **Future Extensions**, and **Design Decisions** sections into the same ontology file.

Add this after the **Purpose** section.

````markdown
---

# 2. Scope

This ontology focuses on the first MVP knowledge graph for power electronics reliability diagnosis.

The initial graph is centred on IGBT power module reliability because IGBT modules are common, technically rich, and strongly linked to reliability mechanisms such as thermal cycling, bond wire fatigue, solder fatigue, junction temperature variation, and cooling degradation.

The ontology is intentionally limited in Sprint 4.2 so that it can be converted into a clear Neo4j graph model in Sprint 4.3.

---

# 3. Design Principles

## 3.1 Engineering Concepts Should Be Explicit Nodes

Important engineering concepts should be represented as graph nodes rather than hidden inside text fields.

For example:

```text
Thermal Cycling
Bond Wire Fatigue
Junction Temperature Variation
Rising VCE(sat)
````

These should become nodes because they can participate in multiple relationships.

---

## 3.2 Relationships Should Explain Engineering Logic

Relationships should describe meaningful engineering connections.

For example:

```text
Bond Wire Fatigue CAUSED_BY Thermal Cycling
Thermal Cycling TRIGGERED_BY Junction Temperature Variation
Bond Wire Fatigue OBSERVED_AS Rising VCE(sat)
```

The graph should not only store information; it should explain how concepts are connected.

---

## 3.3 Evidence Should Be Traceable

Every important diagnosis should be linked back to evidence.

This is important for explainable AI and future GraphRAG.

```text
FailureMode SUPPORTED_BY DocumentEvidence
```

---

## 3.4 Start Small and Expand Incrementally

The first ontology should not attempt to model all of power electronics.

Sprint 4.2 focuses on a small but meaningful reliability domain:

```text
IGBT Module → Thermal Cycling → Bond Wire Fatigue → Symptom → Test → Maintenance
```

This makes the graph easier to test, query, and extend.

---

## 3.5 The Ontology Should Support Future GraphRAG

The ontology is designed so that future GraphRAG can combine:

```text
Vector retrieval
+
Graph traversal
+
LLM reasoning
```

This means the graph must support both technical relationships and document evidence links.

````

Then add this near the end, before **Success Criteria**.

```markdown
---

# 11. Future Extensions

The following concepts are intentionally out of scope for the first MVP but may be added in future versions.

| Future Node Type | Purpose |
|---|---|
| `PowerConverter` | Represents inverter, rectifier, DC-DC converter, or drive system |
| `Topology` | Represents converter topology such as NPC, ANPC, two-level inverter |
| `CoolingSystem` | Represents liquid cooling, forced air cooling, heat sink systems |
| `Sensor` | Represents physical sensors used for monitoring |
| `MaintenanceRecord` | Represents real maintenance history |
| `InspectionImage` | Represents image-based evidence |
| `SimulationResult` | Represents simulation or digital twin output |
| `ReliabilityMetric` | Represents MTBF, FIT rate, lifetime estimate, thermal cycle count |
| `Standard` | Represents engineering standards or reliability guidelines |
| `Manufacturer` | Represents component manufacturer |
| `OperatingProfile` | Represents mission profile or duty cycle |
| `Environment` | Represents humidity, vibration, dust, ambient temperature |

---

# 12. Design Decisions

## 12.1 Why is `Thermal Cycling` a node?

`Thermal Cycling` is represented as a node because it can cause or contribute to multiple failure modes, including bond wire fatigue, solder fatigue, and thermal interface degradation.

If thermal cycling were only stored as text, the graph could not easily find all failures linked to it.

---

## 12.2 Why is `DocumentEvidence` a node?

`DocumentEvidence` is represented as a node so that engineering conclusions can be traced back to source documents, chunks, pages, and retrieval scores.

This supports explainable AI and future GraphRAG.

---

## 12.3 Why separate `FailureMode` and `FailureMechanism`?

A failure mode describes how the failure appears.

A failure mechanism describes the physical process causing it.

For example:

```text
FailureMode: Bond Wire Fatigue
FailureMechanism: Thermal Cycling
````

This separation improves engineering clarity and supports better diagnostic reasoning.

---

## 12.4 Why separate `Component` and `SubComponent`?

A power electronics component often contains smaller reliability-critical parts.

For example:

```text
IGBT Module
    HAS_SUBCOMPONENT
Bond Wire
```

This allows the graph to represent internal component structure.

---

## 12.5 Why do relationships have properties?

Relationship properties allow the graph to store confidence, evidence strength, thresholds, and effectiveness.

For example:

```text
Bond Wire Fatigue CAUSED_BY Thermal Cycling
confidence = 0.94
evidenceCount = 12
```

This enables ranking, filtering, and explainable recommendations.

---

## 12.6 Why start with IGBT modules?

IGBT modules are a strong MVP focus because they are widely used in power electronics and have well-known reliability mechanisms.

Starting with this domain provides a realistic but manageable graph model.

```

Finally add:

---
```

# 13. References

- Neo4j Graph Data Modeling concepts
- Neo4j GraphAcademy modelling guidance
- Power electronics reliability literature
- IGBT module reliability concepts
- Retrieval-Augmented Generation architecture
- GraphRAG architecture principles
````

This completes the ontology document as a proper design specification.
