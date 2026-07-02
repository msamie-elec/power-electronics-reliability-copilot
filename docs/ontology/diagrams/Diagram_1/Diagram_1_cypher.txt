# Create:
CREATE (`Failure Mode`)-[:AFFECTS]->()-[:CONTAINS]->(`Sub-Component`)-[:EXPERIENCES]->(`Failure Mechanism`)<-[:ACCELERATES]-(),
()-[:INCREASES_RISK_OF]->(`Failure Mechanism`)-[:RESULTS_IN]->(`Failure Mode`)-[:PRODUCES]->()-[:VERIFIED_BY]->(`Test Method`)-[:RECOMMENDS]->(),
(`Failure Mode`)<-[:SUPPORTS]-(`Document Evidence`)-[:SUPPORTS]->(`Failure Mechanism`),
(`Document Evidence`)-[:SUPPORTS]->(`Test Method`),
(`Sub-Component`)-[:HAS_MATERIAL]->()

# Match:
MATCH path0 = (`Failure Mode`)-[:AFFECTS]->()-[:CONTAINS]->(`Sub-Component`)-[:EXPERIENCES]->(`Failure Mechanism`)<-[:ACCELERATES]-(),
path1 = ()-[:INCREASES_RISK_OF]->(`Failure Mechanism`)-[:RESULTS_IN]->(`Failure Mode`)-[:PRODUCES]->()-[:VERIFIED_BY]->(`Test Method`)-[:RECOMMENDS]->(),
path2 = (`Failure Mode`)<-[:SUPPORTS]-(`Document Evidence`)-[:SUPPORTS]->(`Failure Mechanism`),
path3 = (`Document Evidence`)-[:SUPPORTS]->(`Test Method`),
path4 = (`Sub-Component`)-[:HAS_MATERIAL]->()
RETURN path0, path1, path2, path3, path4

# Merge:
MERGE (`Failure Mode`)-[:AFFECTS]->()-[:CONTAINS]->(`Sub-Component`)-[:EXPERIENCES]->(`Failure Mechanism`)<-[:ACCELERATES]-()
MERGE ()-[:INCREASES_RISK_OF]->(`Failure Mechanism`)-[:RESULTS_IN]->(`Failure Mode`)-[:PRODUCES]->()-[:VERIFIED_BY]->(`Test Method`)-[:RECOMMENDS]->()
MERGE (`Failure Mode`)<-[:SUPPORTS]-(`Document Evidence`)-[:SUPPORTS]->(`Failure Mechanism`)
MERGE (`Document Evidence`)-[:SUPPORTS]->(`Test Method`)
MERGE (`Sub-Component`)-[:HAS_MATERIAL]->()
