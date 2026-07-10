from neo4j import GraphDatabase

from app.config import (
    NEO4J_DATABASE,
    NEO4J_URI,
    NEO4J_USERNAME,
)
from app.services.secrets.secret_service import secret_service


class Neo4jService:
    def __init__(self) -> None:
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, self._get_password()),
        )

    @staticmethod
    def _get_password() -> str:
        try:
            return secret_service.get_secret(
                "neo4j-password",
                fallback_env="NEO4J_PASSWORD",
            )
        except KeyError as exc:
            raise ValueError("NEO4J_PASSWORD must be configured.") from exc

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
