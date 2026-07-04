"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.9 — Graph Validation Service
===========================================================================

Purpose:
    Provides read-only inspection and validation of the Neo4j Engineering
    Knowledge Graph.

This service does NOT modify the graph.
"""

from app.config import NEO4J_DATABASE
from app.services.neo4j_service import Neo4jService
from datetime import datetime, timezone
from app.config import NEO4J_DATABASE

class GraphValidationService:
    """Read-only service for graph statistics and validation."""

    def __init__(self):
        self.neo4j = Neo4jService()

    def get_total_nodes(self) -> int:
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run("""
                MATCH (n)
                RETURN count(n) AS total
            """)
            return result.single()["total"]

    def get_total_relationships(self) -> int:
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run("""
                MATCH ()-[r]->()
                RETURN count(r) AS total
            """)
            return result.single()["total"]

    def get_node_labels(self):
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run("""
                MATCH (n)
                UNWIND labels(n) AS label
                RETURN label, count(*) AS count
                ORDER BY count DESC
            """)

            return {
                record["label"]: record["count"]
                for record in result
            }

    def get_relationship_types(self):
        with self.neo4j.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) AS type,
                       count(*) AS count
                ORDER BY count DESC
            """)

            return {
                record["type"]: record["count"]
                for record in result
            }

    def get_graph_summary(self):
        """Return an overall summary of the knowledge graph."""

        total_nodes = self.get_total_nodes()
        total_relationships = self.get_total_relationships()

        graph_status = "Healthy"

        if total_nodes == 0:
            graph_status = "Empty"
        elif total_relationships == 0:
            graph_status = "NoRelationships"

        return {
            "database": NEO4J_DATABASE,
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "graphStatus": graph_status,
            "totalNodes": total_nodes,
            "totalRelationships": total_relationships,
            "nodeLabels": self.get_node_labels(),
            "relationshipTypes": self.get_relationship_types(),
        }

    def close(self):
        self.neo4j.close()


graph_validation_service = GraphValidationService()