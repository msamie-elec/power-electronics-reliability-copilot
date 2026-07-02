// =====================================================
// Power Electronics Reliability Copilot
// v0.4 – Seed Engineering Knowledge Graph
// =====================================================

//------------------------------------------------------
// Component
//------------------------------------------------------

MERGE (c:Component {componentId: "C001"})
SET
    c.name = "IGBT Module",
    c.category = "Power Semiconductor",
    c.manufacturer = "Infineon";


//------------------------------------------------------
// SubComponent
//------------------------------------------------------

MERGE (sc:SubComponent {subComponentId: "SC001"})
SET
    sc.name = "Bond Wire",
    sc.function = "Electrical Connection";


//------------------------------------------------------
// Material
//------------------------------------------------------

MERGE (m:Material {materialId: "MT001"})
SET
    m.name = "Aluminium",
    m.type = "Metal",
    m.conductivity = "High";


//------------------------------------------------------
// Operating Condition
//------------------------------------------------------

MERGE (oc:OperatingCondition {conditionId: "OC001"})
SET
    oc.name = "High Load Cycling";


//------------------------------------------------------
// Stress Factor
//------------------------------------------------------

MERGE (sf:StressFactor {stressId: "ST001"})
SET
    sf.name = "Junction Temperature Variation",
    sf.unit = "°C";


//------------------------------------------------------
// Failure Mechanism
//------------------------------------------------------

MERGE (fm:FailureMechanism {mechanismId: "M001"})
SET
    fm.name = "Thermal Cycling",
    fm.physics = "Thermomechanical Fatigue";


//------------------------------------------------------
// Failure Mode
//------------------------------------------------------

MERGE (f:FailureMode {failureId: "FM001"})
SET
    f.name = "Bond Wire Lift-off",
    f.severity = 9;


//------------------------------------------------------
// Symptom
//------------------------------------------------------

MERGE (s:Symptom {symptomId: "SY001"})
SET
    s.name = "Rising VCE(sat)",
    s.measurable = true;


//------------------------------------------------------
// Test Method
//------------------------------------------------------

MERGE (t:TestMethod {testId: "TM001"})
SET
    t.name = "Electrical Parameter Monitoring",
    t.equipment = "Power Analyzer";


//------------------------------------------------------
// Maintenance Action
//------------------------------------------------------

MERGE (a:MaintenanceAction {actionId: "MA001"})
SET
    a.name = "Inspect Thermal Interface Material",
    a.priority = "High";


//------------------------------------------------------
// Document Evidence
//------------------------------------------------------

MERGE (d:DocumentEvidence {chunkId: "DOC001"})
SET
    d.name = "Engineering Document";



//------------------------------------------------------
// Relationships
//------------------------------------------------------

MATCH
(c:Component {componentId:"C001"}),
(sc:SubComponent {subComponentId:"SC001"})
MERGE (c)-[:CONTAINS]->(sc);


MATCH
(sc:SubComponent {subComponentId:"SC001"}),
(m:Material {materialId:"MT001"})
MERGE (sc)-[:HAS_MATERIAL]->(m);


MATCH
(sc:SubComponent {subComponentId:"SC001"}),
(fm:FailureMechanism {mechanismId:"M001"})
MERGE (sc)-[:EXPERIENCES]->(fm);


MATCH
(sf:StressFactor {stressId:"ST001"}),
(fm:FailureMechanism {mechanismId:"M001"})
MERGE (sf)-[:ACCELERATES]->(fm);


MATCH
(oc:OperatingCondition {conditionId:"OC001"}),
(fm:FailureMechanism {mechanismId:"M001"})
MERGE (oc)-[:INCREASES_RISK_OF]->(fm);


MATCH
(fm:FailureMechanism {mechanismId:"M001"}),
(f:FailureMode {failureId:"FM001"})
MERGE (fm)-[:RESULTS_IN]->(f);


MATCH
(f:FailureMode {failureId:"FM001"}),
(c:Component {componentId:"C001"})
MERGE (f)-[:AFFECTS]->(c);


MATCH
(f:FailureMode {failureId:"FM001"}),
(s:Symptom {symptomId:"SY001"})
MERGE (f)-[:PRODUCES]->(s);


MATCH
(s:Symptom {symptomId:"SY001"}),
(t:TestMethod {testId:"TM001"})
MERGE (s)-[:VERIFIED_BY]->(t);


MATCH
(t:TestMethod {testId:"TM001"}),
(a:MaintenanceAction {actionId:"MA001"})
MERGE (t)-[:RECOMMENDS]->(a);


MATCH
(d:DocumentEvidence {chunkId:"DOC001"}),
(fm:FailureMechanism {mechanismId:"M001"})
MERGE (d)-[:SUPPORTS]->(fm);


MATCH
(d:DocumentEvidence {chunkId:"DOC001"}),
(f:FailureMode {failureId:"FM001"})
MERGE (d)-[:SUPPORTS]->(f);


MATCH
(d:DocumentEvidence {chunkId:"DOC001"}),
(t:TestMethod {testId:"TM001"})
MERGE (d)-[:SUPPORTS]->(t);
