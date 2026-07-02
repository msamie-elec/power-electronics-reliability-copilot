//======================================================
// Power Electronics Reliability Copilot
// v0.4 - Graph Validation
//======================================================


//------------------------------------------------------
// Total nodes
//------------------------------------------------------

MATCH (n)
RETURN count(n) AS totalNodes;


//------------------------------------------------------
// Total relationships
//------------------------------------------------------

MATCH ()-[r]->()
RETURN count(r) AS totalRelationships;


//------------------------------------------------------
// Nodes by label
//------------------------------------------------------

MATCH (n)
UNWIND labels(n) AS label
RETURN
label,
count(*) AS total
ORDER BY label;


//------------------------------------------------------
// Relationships by type
//------------------------------------------------------

MATCH ()-[r]->()
RETURN
type(r) AS relationship,
count(*) AS total
ORDER BY relationship;


//------------------------------------------------------
// Nodes without relationships
//------------------------------------------------------

MATCH (n)
WHERE NOT (n)--()
RETURN n;


//------------------------------------------------------
// Duplicate IDs
//------------------------------------------------------

MATCH (n)

UNWIND keys(n) AS property

WITH
property,
n[property] AS value,
collect(n) AS nodes

WHERE property ENDS WITH "Id"

AND size(nodes) > 1

RETURN
property,
value,
size(nodes);



//------------------------------------------------------
// Missing ID properties
//------------------------------------------------------

MATCH (n)

WHERE
(
n:Component AND n.componentId IS NULL
)
OR
(
n:SubComponent AND n.subComponentId IS NULL
)
OR
(
n:Material AND n.materialId IS NULL
)
OR
(
n:OperatingCondition AND n.conditionId IS NULL
)
OR
(
n:StressFactor AND n.stressId IS NULL
)
OR
(
n:FailureMechanism AND n.mechanismId IS NULL
)
OR
(
n:FailureMode AND n.failureId IS NULL
)
OR
(
n:Symptom AND n.symptomId IS NULL
)
OR
(
n:TestMethod AND n.testId IS NULL
)
OR
(
n:MaintenanceAction AND n.actionId IS NULL
)
OR
(
n:DocumentEvidence AND n.chunkId IS NULL
)

RETURN n;


//------------------------------------------------------
// Nodes missing name
//------------------------------------------------------

MATCH (n)

WHERE n.name IS NULL

AND NOT n:DocumentEvidence

RETURN n;