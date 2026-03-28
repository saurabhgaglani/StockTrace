import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )
    return _driver

def get_dependency_path(entity: str, ticker: str) -> list[str]:
    """Return ordered node names from entity to company ticker."""
    driver = get_driver()
    db = os.getenv("NEO4J_DATABASE")
    with driver.session(database=db) as session:
        result = session.run(
            """
            MATCH path = (a {name: $entity})-[*1..8]-(b:Company {ticker: $ticker})
            RETURN [n IN nodes(path) | coalesce(n.name, n.ticker)] AS names
            ORDER BY length(path) ASC
            LIMIT 1
            """,
            entity=entity, ticker=ticker
        )
        record = result.single()
        return record["names"] if record else []
