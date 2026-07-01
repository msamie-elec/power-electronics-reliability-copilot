from neo4j import GraphDatabase

from app.config import (
    NEO4J_DATABASE,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USERNAME,
)


class Neo4jService:
    def __init__(self) -> None:
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        )

    def close(self) -> None:
        self.driver.close()

    def test_connection(self) -> dict:
        with self.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run("RETURN 1 AS result")
            record = result.single()

            return {
                "status": "connected",
                "database": NEO4J_DATABASE,
                "result": record["result"] if record else None,
            }


def test_neo4j_connection() -> dict:
    service = Neo4jService()

    try:
        return service.test_connection()
    finally:
        service.close()