# Create:
CREATE (`Failure Mode`:FailureMode {failureId: "FM001", name: "Bond Wire Lift-off", severity: 9})-[:AFFECTS]->(:Component {componentId: "C001", name: "IGBT Module", category: "Power Semiconductor", manufacturer: "Infineon"})-[:CONTAINS]->(`Sub-Component`:SubComponent {subComponentId: "SC001", name: "Bond Wire", material: "Aluminium", function: "Electrical connection"})-[:EXPERIENCES]->(`Failure Mechanism`:FailureMechanism {mechanismId: "M001", name: "Thermal Cycling", physics: "Thermomechanical fatigue"})<-[:ACCELERATES]-(:StressFactor {stressId: "ST001", name: "Junction Temperature Variation", unit: "°C"}),
(:OperatingCondition {conditionId: "OC001", loadType: "High Load Cycling", ambientTemperature: 45})-[:INCREASES_RISK_OF]->(`Failure Mechanism`)-[:RESULTS_IN]->(`Failure Mode`)-[:PRODUCES]->(:Symptom {symptomId: "SY001", name: "Rising VCE(sat)", measurable: "true"})-[:VERIFIED_BY]->(`Test Method`:TestMethod {testId: "TM001", name: "Electrical Parameter Monitoring", equipment: "Power Analyzer"})-[:RECOMMENDS]->(:MaintenanceAction {actionId: "MA001", name: "Inspect Thermal Interface Material", priority: "High"}),
(`Failure Mode`)<-[:SUPPORTS]-(`Document Evidence`:DocumentEvidence {chunkId: " <chunkId>", documentId: "<documentId>", page: "<pageNumber>"})-[:SUPPORTS]->(`Failure Mechanism`),
(`Document Evidence`)-[:SUPPORTS]->(`Test Method`),
(`Sub-Component`)-[:HAS_MATERIAL]->(:Material {materialId: "MT001", name: "Aluminium", type: "Metal", conductivity: "High"})

# Match:
MATCH path0 = (`Failure Mode`:FailureMode {failureId: "FM001", name: "Bond Wire Lift-off", severity: 9})-[:AFFECTS]->(:Component {componentId: "C001", name: "IGBT Module", category: "Power Semiconductor", manufacturer: "Infineon"})-[:CONTAINS]->(`Sub-Component`:SubComponent {subComponentId: "SC001", name: "Bond Wire", material: "Aluminium", function: "Electrical connection"})-[:EXPERIENCES]->(`Failure Mechanism`:FailureMechanism {mechanismId: "M001", name: "Thermal Cycling", physics: "Thermomechanical fatigue"})<-[:ACCELERATES]-(:StressFactor {stressId: "ST001", name: "Junction Temperature Variation", unit: "°C"}),
path1 = (:OperatingCondition {conditionId: "OC001", loadType: "High Load Cycling", ambientTemperature: 45})-[:INCREASES_RISK_OF]->(`Failure Mechanism`)-[:RESULTS_IN]->(`Failure Mode`)-[:PRODUCES]->(:Symptom {symptomId: "SY001", name: "Rising VCE(sat)", measurable: "true"})-[:VERIFIED_BY]->(`Test Method`:TestMethod {testId: "TM001", name: "Electrical Parameter Monitoring", equipment: "Power Analyzer"})-[:RECOMMENDS]->(:MaintenanceAction {actionId: "MA001", name: "Inspect Thermal Interface Material", priority: "High"}),
path2 = (`Failure Mode`)<-[:SUPPORTS]-(`Document Evidence`:DocumentEvidence {chunkId: " <chunkId>", documentId: "<documentId>", page: "<pageNumber>"})-[:SUPPORTS]->(`Failure Mechanism`),
path3 = (`Document Evidence`)-[:SUPPORTS]->(`Test Method`),
path4 = (`Sub-Component`)-[:HAS_MATERIAL]->(:Material {materialId: "MT001", name: "Aluminium", type: "Metal", conductivity: "High"})
RETURN path0, path1, path2, path3, path4

# Merge:
MERGE (`Failure Mode`:FailureMode {failureId: "FM001", name: "Bond Wire Lift-off", severity: 9})-[:AFFECTS]->(:Component {componentId: "C001", name: "IGBT Module", category: "Power Semiconductor", manufacturer: "Infineon"})-[:CONTAINS]->(`Sub-Component`:SubComponent {subComponentId: "SC001", name: "Bond Wire", material: "Aluminium", function: "Electrical connection"})-[:EXPERIENCES]->(`Failure Mechanism`:FailureMechanism {mechanismId: "M001", name: "Thermal Cycling", physics: "Thermomechanical fatigue"})<-[:ACCELERATES]-(:StressFactor {stressId: "ST001", name: "Junction Temperature Variation", unit: "°C"})
MERGE (:OperatingCondition {conditionId: "OC001", loadType: "High Load Cycling", ambientTemperature: 45})-[:INCREASES_RISK_OF]->(`Failure Mechanism`)-[:RESULTS_IN]->(`Failure Mode`)-[:PRODUCES]->(:Symptom {symptomId: "SY001", name: "Rising VCE(sat)", measurable: "true"})-[:VERIFIED_BY]->(`Test Method`:TestMethod {testId: "TM001", name: "Electrical Parameter Monitoring", equipment: "Power Analyzer"})-[:RECOMMENDS]->(:MaintenanceAction {actionId: "MA001", name: "Inspect Thermal Interface Material", priority: "High"})
MERGE (`Failure Mode`)<-[:SUPPORTS]-(`Document Evidence`:DocumentEvidence {chunkId: " <chunkId>", documentId: "<documentId>", page: "<pageNumber>"})-[:SUPPORTS]->(`Failure Mechanism`)
MERGE (`Document Evidence`)-[:SUPPORTS]->(`Test Method`)
MERGE (`Sub-Component`)-[:HAS_MATERIAL]->(:Material {materialId: "MT001", name: "Aluminium", type: "Metal", conductivity: "High"})


