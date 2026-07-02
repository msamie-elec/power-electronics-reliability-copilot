// =====================================================
// Power Electronics Reliability Copilot
// v0.4 – Engineering Query Library
// =====================================================


//------------------------------------------------------
// 1. Show complete graph
//------------------------------------------------------

MATCH (n)-[r]->(m)
RETURN n, r, m;


//------------------------------------------------------
// 2. Find sub-components of a component
//------------------------------------------------------

MATCH (c:Component {name: "IGBT Module"})-[:CONTAINS]->(sc:SubComponent)
RETURN c.name AS component, sc.name AS subComponent;


//------------------------------------------------------
// 3. Find material of a sub-component
//------------------------------------------------------

MATCH (sc:SubComponent {name: "Bond Wire"})-[:HAS_MATERIAL]->(m:Material)
RETURN sc.name AS subComponent, m.name AS material;


//------------------------------------------------------
// 4. Find failure mechanisms affecting a sub-component
//------------------------------------------------------

MATCH (sc:SubComponent {name: "Bond Wire"})-[:EXPERIENCES]->(fm:FailureMechanism)
RETURN sc.name AS subComponent, fm.name AS failureMechanism;


//------------------------------------------------------
// 5. Find stress factors accelerating a failure mechanism
//------------------------------------------------------

MATCH (sf:StressFactor)-[:ACCELERATES]->(fm:FailureMechanism {name: "Thermal Cycling"})
RETURN sf.name AS stressFactor, fm.name AS failureMechanism;


//------------------------------------------------------
// 6. Find operating conditions increasing failure risk
//------------------------------------------------------

MATCH (oc:OperatingCondition)-[:INCREASES_RISK_OF]->(fm:FailureMechanism {name: "Thermal Cycling"})
RETURN oc.name AS operatingCondition, fm.name AS failureMechanism;


//------------------------------------------------------
// 7. Find failure modes caused by a failure mechanism
//------------------------------------------------------

MATCH (fm:FailureMechanism {name: "Thermal Cycling"})-[:RESULTS_IN]->(f:FailureMode)
RETURN fm.name AS failureMechanism, f.name AS failureMode;


//------------------------------------------------------
// 8. Find symptoms produced by a failure mode
//------------------------------------------------------

MATCH (f:FailureMode {name: "Bond Wire Lift-off"})-[:PRODUCES]->(s:Symptom)
RETURN f.name AS failureMode, s.name AS symptom;


//------------------------------------------------------
// 9. Find test methods verifying a symptom
//------------------------------------------------------

MATCH (s:Symptom {name: "Rising VCE(sat)"})-[:VERIFIED_BY]->(t:TestMethod)
RETURN s.name AS symptom, t.name AS testMethod;


//------------------------------------------------------
// 10. Find maintenance actions recommended by a test method
//------------------------------------------------------

MATCH (t:TestMethod {name: "Electrical Parameter Monitoring"})-[:RECOMMENDS]->(a:MaintenanceAction)
RETURN t.name AS testMethod, a.name AS maintenanceAction;


//------------------------------------------------------
// 11. Find evidence supporting a failure mechanism
//------------------------------------------------------

MATCH (d:DocumentEvidence)-[:SUPPORTS]->(fm:FailureMechanism {name: "Thermal Cycling"})
RETURN d.name AS documentEvidence, fm.name AS supportedConcept;


//------------------------------------------------------
// 12. Find evidence supporting a failure mode
//------------------------------------------------------

MATCH (d:DocumentEvidence)-[:SUPPORTS]->(f:FailureMode {name: "Bond Wire Lift-off"})
RETURN d.name AS documentEvidence, f.name AS supportedConcept;


//------------------------------------------------------
// 13. Find complete diagnostic reasoning path
//------------------------------------------------------

MATCH path =
(c:Component {name: "IGBT Module"})-[:CONTAINS]->(sc:SubComponent)
-[:EXPERIENCES]->(fm:FailureMechanism)
-[:RESULTS_IN]->(f:FailureMode)
-[:PRODUCES]->(s:Symptom)
-[:VERIFIED_BY]->(t:TestMethod)
-[:RECOMMENDS]->(a:MaintenanceAction)
RETURN path;


//------------------------------------------------------
// 14. Find complete risk-to-maintenance path
//------------------------------------------------------

MATCH path =
(oc:OperatingCondition)-[:INCREASES_RISK_OF]->(fm:FailureMechanism)
-[:RESULTS_IN]->(f:FailureMode)
-[:PRODUCES]->(s:Symptom)
-[:VERIFIED_BY]->(t:TestMethod)
-[:RECOMMENDS]->(a:MaintenanceAction)
RETURN path;


//------------------------------------------------------
// 15. Find all concepts supported by engineering evidence
//------------------------------------------------------

MATCH (d:DocumentEvidence)-[:SUPPORTS]->(n)
RETURN d.name AS evidence, labels(n) AS supportedLabel, n.name AS supportedConcept;