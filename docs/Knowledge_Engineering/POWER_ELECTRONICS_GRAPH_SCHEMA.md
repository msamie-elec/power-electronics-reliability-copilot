# Power Electronics Graph Schema

**Project:** Power Electronics Reliability Copilot  
**Version:** v0.4.0 — Knowledge Graph Foundation  
**Sprint:** 4.3 — Graph Schema & Constraints

---

# 1. Purpose

This document translates the Power Electronics Reliability Ontology into a Neo4j graph database schema.

The ontology defines the engineering concepts.  
This schema defines how those concepts will be implemented in Neo4j.

---

# 2. Node Labels and Required Properties

| Node Label | Required Unique ID | Required Properties | Optional Properties |
|---|---|---|---|
| `Component` | `componentId` | `name`, `category` | `manufacturer`, `voltageRating`, `currentRating`, `description` |
| `SubComponent` | `subComponentId` | `name` | `material`, `function` |
| `Material` | `materialId` | `name` | `type`, `conductivity` |
| `FailureMode` | `failureId` | `name` | `severity`, `probability`, `description` |
| `FailureMechanism` | `mechanismId` | `name` | `physics`, `description` |
| `StressFactor` | `stressId` | `name` | `unit`, `typicalRange` |
| `Symptom` | `symptomId` | `name` | `measurable`, `description` |
| `TestMethod` | `testId` | `name` | `equipment`, `duration` |
| `MaintenanceAction` | `actionId` | `name` | `priority`, `interval` |
| `OperatingCondition` | `conditionId` | `loadType` | `ambientTemperature`, `switchingFrequency` |
| `DocumentEvidence` | `chunkId` | `sourceDocument`, `text` | `page`, `score` |

---

# 3. Relationship Schema

| Relationship | From | To | Required Properties | Optional Properties |
|---|---|---|---|---|
| `HAS_SUBCOMPONENT` | `Component` | `SubComponent` | — | — |
| `HAS_FAILURE_MODE` | `Component` | `FailureMode` | — | — |
| `CAUSED_BY` | `FailureMode` | `FailureMechanism` | — | `confidence`, `evidenceCount` |
| `TRIGGERED_BY` | `FailureMechanism` | `StressFactor` | — | `threshold`, `confidence` |
| `OBSERVED_AS` | `FailureMode` | `Symptom` | — | `confidence` |
| `DETECTED_BY` | `Symptom` | `TestMethod` | — | `accuracy` |
| `MITIGATED_BY` | `FailureMode` | `MaintenanceAction` | — | `effectiveness` |
| `AFFECTS` | `StressFactor` | `Component` | — | `confidence` |
| `INVOLVES_MATERIAL` | `FailureMechanism` | `Material` | — | — |
| `OPERATES_UNDER` | `Component` | `OperatingCondition` | — | — |
| `SUPPORTED_BY` | `FailureMode` | `DocumentEvidence` | — | `retrievalScore` |

---

# 4. Unique Constraints

The following constraints should be created in Neo4j.

```cypher
CREATE CONSTRAINT component_id_unique IF NOT EXISTS
FOR (n:Component)
REQUIRE n.componentId IS UNIQUE;

CREATE CONSTRAINT subcomponent_id_unique IF NOT EXISTS
FOR (n:SubComponent)
REQUIRE n.subComponentId IS UNIQUE;

CREATE CONSTRAINT material_id_unique IF NOT EXISTS
FOR (n:Material)
REQUIRE n.materialId IS UNIQUE;

CREATE CONSTRAINT failure_id_unique IF NOT EXISTS
FOR (n:FailureMode)
REQUIRE n.failureId IS UNIQUE;

CREATE CONSTRAINT mechanism_id_unique IF NOT EXISTS
FOR (n:FailureMechanism)
REQUIRE n.mechanismId IS UNIQUE;

CREATE CONSTRAINT stress_id_unique IF NOT EXISTS
FOR (n:StressFactor)
REQUIRE n.stressId IS UNIQUE;

CREATE CONSTRAINT symptom_id_unique IF NOT EXISTS
FOR (n:Symptom)
REQUIRE n.symptomId IS UNIQUE;

CREATE CONSTRAINT test_id_unique IF NOT EXISTS
FOR (n:TestMethod)
REQUIRE n.testId IS UNIQUE;

CREATE CONSTRAINT action_id_unique IF NOT EXISTS
FOR (n:MaintenanceAction)
REQUIRE n.actionId IS UNIQUE;

CREATE CONSTRAINT condition_id_unique IF NOT EXISTS
FOR (n:OperatingCondition)
REQUIRE n.conditionId IS UNIQUE;

CREATE CONSTRAINT evidence_chunk_id_unique IF NOT EXISTS
FOR (n:DocumentEvidence)
REQUIRE n.chunkId IS UNIQUE;
````

---

# 5. Recommended Indexes

```cypher
CREATE INDEX component_name_index IF NOT EXISTS
FOR (n:Component)
ON (n.name);

CREATE INDEX failure_mode_name_index IF NOT EXISTS
FOR (n:FailureMode)
ON (n.name);

CREATE INDEX failure_mechanism_name_index IF NOT EXISTS
FOR (n:FailureMechanism)
ON (n.name);

CREATE INDEX symptom_name_index IF NOT EXISTS
FOR (n:Symptom)
ON (n.name);

CREATE INDEX document_source_index IF NOT EXISTS
FOR (n:DocumentEvidence)
ON (n.sourceDocument);
```

---

# 6. MVP Instance Model

The first graph instance will represent the following engineering chain:

```text
IGBT Module
    HAS_SUBCOMPONENT → Bond Wire
    HAS_SUBCOMPONENT → Solder Layer
    HAS_FAILURE_MODE → Bond Wire Fatigue
        CAUSED_BY → Thermal Cycling
            TRIGGERED_BY → Junction Temperature Variation
        OBSERVED_AS → Rising VCE(sat)
        DETECTED_BY → Electrical Parameter Monitoring
        MITIGATED_BY → Inspect Thermal Interface Material
        SUPPORTED_BY → Reliability Handbook Chunk
```

---

# 7. Implementation Mapping

| Ontology Concept         | Neo4j Implementation                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------- |
| Engineering entity       | Node                                                                                  |
| Engineering relationship | Relationship                                                                          |
| Engineering metadata     | Node or relationship property                                                         |
| Evidence chunk           | `DocumentEvidence` node                                                               |
| Confidence score         | Relationship property                                                                 |
| Retrieval score          | `SUPPORTED_BY.retrievalScore`                                                         |
| Component hierarchy      | `HAS_SUBCOMPONENT`                                                                    |
| Failure diagnosis path   | Component → FailureMode → FailureMechanism → Symptom → TestMethod → MaintenanceAction |

---

# 8. Schema Validation Rules

Before graph data is inserted:

* Every node must have its required unique ID.
* Every node must have its required name or primary descriptor.
* Every relationship must connect valid node labels.
* Evidence nodes must include source document and text.
* Relationship confidence values should be numeric where used.
* Duplicate engineering concepts should be merged, not recreated.

---

# 9. Sprint 4.3 Success Criteria

Sprint 4.3 is complete when:

* Graph schema document is created.
* Node labels are mapped to Neo4j labels.
* Required properties are defined.
* Unique constraints are defined.
* Indexes are defined.
* First Cypher schema script is created.
* Schema script can be executed successfully in Neo4j.

````

Next we will create the actual Cypher file:

```text
backend/graph/schema.cypher
````
