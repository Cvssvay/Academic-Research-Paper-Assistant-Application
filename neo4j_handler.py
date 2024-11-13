# neo4j_handler.py
from neo4j import GraphDatabase
from config import CONFIG

class Neo4jHandler:
    def __init__(self):
        """Initialize the Neo4j database connection."""
        self.driver = GraphDatabase.driver(
            CONFIG["neo4j"]["uri"],
            auth=(CONFIG["neo4j"]["username"], CONFIG["neo4j"]["password"])
        )

    def store_paper(self, title, content, publish_date):
        """Store a paper in the Neo4j database."""
        with self.driver.session() as session:
            session.run(
                "CREATE (p:Paper {title: $title, content: $content, publish_date: $publish_date})",
                title=title, content=content, publish_date=publish_date
            )

    def close(self):
        """Close the connection to the Neo4j database."""
        self.driver.close()
