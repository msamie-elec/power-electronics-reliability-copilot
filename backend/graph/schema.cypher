// Power Electronics Reliability Copilot
// v0.4.0 — Knowledge Graph Foundation
// Sprint 4.3 — Graph Schema & Constraints

// ================================
// Unique Constraints
// ================================

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


// ================================
// Indexes
// ================================

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