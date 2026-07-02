## Diagram 2 — Neo4j Graph Schema

**Purpose**

This diagram illustrates how the conceptual engineering ontology is implemented as a Neo4j graph schema.

Unlike Diagram 1, which focuses on engineering concepts and their semantic relationships, Diagram 2 shows the database implementation by representing each concept as a Neo4j node label together with its key properties, unique identifiers, and relationship types.

The example property values shown in the diagram are illustrative and demonstrate the expected schema structure rather than production data. Placeholder values (e.g., `<documentId>`, `<chunkId>`) indicate fields that will be populated automatically when real engineering documents are ingested into the knowledge graph.

This schema forms the foundation for the engineering knowledge graph implemented in Neo4j and will be populated with real instances during Sprint 4.4.


Diagram 2 Caption:
Diagram 2 illustrates how the engineering ontology is implemented as labelled nodes with properties, identifiers and relationships in Neo4j.