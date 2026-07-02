// =====================================================
// Power Electronics Reliability Copilot
// v0.4 – Graph Statistics
// =====================================================

// Total node count
MATCH (n)
RETURN "Total nodes" AS metric, count(n) AS value;

// Total relationship count
MATCH ()-[r]->()
RETURN "Total relationships" AS metric, count(r) AS value;

// Node count by label
MATCH (n)
UNWIND labels(n) AS label
RETURN label, count(n) AS count
ORDER BY label;

// Relationship count by type
MATCH ()-[r]->()
RETURN type(r) AS relationshipType, count(r) AS count
ORDER BY relationshipType;

// Full graph preview
MATCH (n)-[r]->(m)
RETURN n, r, m;