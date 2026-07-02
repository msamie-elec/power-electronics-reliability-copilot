// Power Electronics Reliability Copilot
// v0.4 — Knowledge Graph Foundation
// Schema indexes

CREATE INDEX component_name_index IF NOT EXISTS
FOR (c:Component)
ON (c.name);

CREATE INDEX subcomponent_name_index IF NOT EXISTS
FOR (s:SubComponent)
ON (s.name);

CREATE INDEX material_name_index IF NOT EXISTS
FOR (m:Material)
ON (m.name);

CREATE INDEX operating_condition_name_index IF NOT EXISTS
FOR (o:OperatingCondition)
ON (o.name);

CREATE INDEX stress_factor_name_index IF NOT EXISTS
FOR (s:StressFactor)
ON (s.name);

CREATE INDEX failure_mechanism_name_index IF NOT EXISTS
FOR (m:FailureMechanism)
ON (m.name);

CREATE INDEX failure_mode_name_index IF NOT EXISTS
FOR (f:FailureMode)
ON (f.name);

CREATE INDEX symptom_name_index IF NOT EXISTS
FOR (s:Symptom)
ON (s.name);

CREATE INDEX test_method_name_index IF NOT EXISTS
FOR (t:TestMethod)
ON (t.name);

CREATE INDEX maintenance_action_name_index IF NOT EXISTS
FOR (a:MaintenanceAction)
ON (a.name);

CREATE INDEX document_source_index IF NOT EXISTS
FOR (d:DocumentEvidence)
ON (d.sourceDocument);