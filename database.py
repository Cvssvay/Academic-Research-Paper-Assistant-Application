# database.py
from neo4j import GraphDatabase
from config import CONFIG

class Neo4jHandler:
    def __init__(self):
        """Initialize the connection to the Neo4j database."""
        self.driver = GraphDatabase.driver(
            CONFIG["neo4j"]["uri"], 
            auth=(CONFIG["neo4j"]["username"], CONFIG["neo4j"]["password"])
        )
    
    def store_paper(self, title, content, publish_date):
        """Store a research paper in Neo4j."""
        with self.driver.session() as session:
            session.run(
                "CREATE (p:Paper {title: $title, content: $content, publish_date: $publish_date})",
                title=title, content=content, publish_date=publish_date
            )
    
    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()
