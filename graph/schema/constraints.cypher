// Power Electronics Reliability Copilot
// v0.4 — Knowledge Graph Foundation
// Schema constraints

CREATE CONSTRAINT component_id_unique IF NOT EXISTS
FOR (c:Component)
REQUIRE c.componentId IS UNIQUE;

CREATE CONSTRAINT subcomponent_id_unique IF NOT EXISTS
FOR (s:SubComponent)
REQUIRE s.subComponentId IS UNIQUE;

CREATE CONSTRAINT material_id_unique IF NOT EXISTS
FOR (m:Material)
REQUIRE m.materialId IS UNIQUE;

CREATE CONSTRAINT operating_condition_id_unique IF NOT EXISTS
FOR (o:OperatingCondition)
REQUIRE o.conditionId IS UNIQUE;

CREATE CONSTRAINT stress_factor_id_unique IF NOT EXISTS
FOR (s:StressFactor)
REQUIRE s.stressId IS UNIQUE;

CREATE CONSTRAINT failure_mechanism_id_unique IF NOT EXISTS
FOR (m:FailureMechanism)
REQUIRE m.mechanismId IS UNIQUE;

CREATE CONSTRAINT failure_mode_id_unique IF NOT EXISTS
FOR (f:FailureMode)
REQUIRE f.failureId IS UNIQUE;

CREATE CONSTRAINT symptom_id_unique IF NOT EXISTS
FOR (s:Symptom)
REQUIRE s.symptomId IS UNIQUE;

CREATE CONSTRAINT test_method_id_unique IF NOT EXISTS
FOR (t:TestMethod)
REQUIRE t.testId IS UNIQUE;

CREATE CONSTRAINT maintenance_action_id_unique IF NOT EXISTS
FOR (a:MaintenanceAction)
REQUIRE a.actionId IS UNIQUE;

CREATE CONSTRAINT document_evidence_chunk_id_unique IF NOT EXISTS
FOR (d:DocumentEvidence)
REQUIRE d.chunkId IS UNIQUE;