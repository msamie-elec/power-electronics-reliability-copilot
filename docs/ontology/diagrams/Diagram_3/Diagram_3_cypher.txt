# Create
CREATE (`Bond Wire Lift-off`)-[:AFFECTS]->()-[:CONTAINS]->(`Bond Wire`)-[:EXPERIENCES]->(`Thermal Cycling`)<-[:ACCELERATES]-(),
()-[:INCREASES_RISK_OF]->(`Thermal Cycling`)-[:RESULTS_IN]->(`Bond Wire Lift-off`)-[:PRODUCES]->()-[:VERIFIED_BY]->(`Electrical Parameter Monitoring`)-[:RECOMMENDS]->(),
(`Bond Wire Lift-off`)<-[:SUPPORTS]-(`Engineering Document`)-[:SUPPORTS]->(`Thermal Cycling`),
(`Engineering Document`)-[:SUPPORTS]->(`Electrical Parameter Monitoring`),
(`Bond Wire`)-[:HAS_MATERIAL]->()

# Match
MATCH path0 = (`Bond Wire Lift-off`)-[:AFFECTS]->()-[:CONTAINS]->(`Bond Wire`)-[:EXPERIENCES]->(`Thermal Cycling`)<-[:ACCELERATES]-(),
path1 = ()-[:INCREASES_RISK_OF]->(`Thermal Cycling`)-[:RESULTS_IN]->(`Bond Wire Lift-off`)-[:PRODUCES]->()-[:VERIFIED_BY]->(`Electrical Parameter Monitoring`)-[:RECOMMENDS]->(),
path2 = (`Bond Wire Lift-off`)<-[:SUPPORTS]-(`Engineering Document`)-[:SUPPORTS]->(`Thermal Cycling`),
path3 = (`Engineering Document`)-[:SUPPORTS]->(`Electrical Parameter Monitoring`),
path4 = (`Bond Wire`)-[:HAS_MATERIAL]->()
RETURN path0, path1, path2, path3, path4

# Merge
MERGE (`Bond Wire Lift-off`)-[:AFFECTS]->()-[:CONTAINS]->(`Bond Wire`)-[:EXPERIENCES]->(`Thermal Cycling`)<-[:ACCELERATES]-()
MERGE ()-[:INCREASES_RISK_OF]->(`Thermal Cycling`)-[:RESULTS_IN]->(`Bond Wire Lift-off`)-[:PRODUCES]->()-[:VERIFIED_BY]->(`Electrical Parameter Monitoring`)-[:RECOMMENDS]->()
MERGE (`Bond Wire Lift-off`)<-[:SUPPORTS]-(`Engineering Document`)-[:SUPPORTS]->(`Thermal Cycling`)
MERGE (`Engineering Document`)-[:SUPPORTS]->(`Electrical Parameter Monitoring`)
MERGE (`Bond Wire`)-[:HAS_MATERIAL]->()