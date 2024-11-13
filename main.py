from neo4j import GraphDatabase

class Neo4jDatabase:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        """
        Initializes the connection to the Neo4j database.
        :param uri: The URI of the Neo4j instance (default is localhost).
        :param user: The username for the Neo4j database.
        :param password: The password for the Neo4j database.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Closes the connection to the Neo4j database.
        """
        self.driver.close()

    def store_paper(self, paper_data):
        """
        Stores a research paper in the Neo4j database.
        :param paper_data: Dictionary containing paper details such as title, abstract, authors, year, and topics.
        """
        with self.driver.session() as session:
            session.write_transaction(self._store_paper, paper_data)

    def fetch_papers_by_topic(self, topic):
        """
        Fetches research papers related to a given topic from the Neo4j database.
        :param topic: The topic to search for papers related to.
        :return: A list of papers related to the topic.
        """
        with self.driver.session() as session:
            return session.read_transaction(self._fetch_papers_by_topic, topic)

    def fetch_paper_by_title(self, title):
        """
        Fetches a paper by its title from the Neo4j database.
        :param title: The title of the paper.
        :return: A list of papers with the specified title.
        """
        with self.driver.session() as session:
            return session.read_transaction(self._fetch_paper_by_title, title)

    @staticmethod
    def _store_paper(tx, paper_data):
        """
        Helper function to store a research paper in Neo4j.
        :param tx: The transaction object.
        :param paper_data: The paper data dictionary.
        """
        # Create Paper Node
        tx.run("""
            MERGE (p:Paper {title: $title})
            SET p.abstract = $abstract, p.year = $year
            """, title=paper_data['title'], abstract=paper_data['abstract'], year=paper_data['year'])
        
        # Create Author Nodes and Relationship to Paper
        for author in paper_data['authors']:
            tx.run("""
                MERGE (a:Author {name: $author_name})
                MERGE (p)-[:PUBLISHED_BY]->(a)
                """, author_name=author)
        
        # Create Topic Nodes and Relationship to Paper
        for topic in paper_data['topics']:
            tx.run("""
                MERGE (t:Topic {name: $topic_name})
                MERGE (p)-[:BELONGS_TO]->(t)
                """, topic_name=topic)

    @staticmethod
    def _fetch_papers_by_topic(tx, topic):
        """
        Helper function to fetch papers related to a specific topic.
        :param tx: The transaction object.
        :param topic: The topic to search for papers related to.
        :return: List of papers related to the topic.
        """
        result = tx.run("""
            MATCH (p:Paper)-[:BELONGS_TO]->(t:Topic {name: $topic})
            RETURN p.title AS title, p.abstract AS abstract, p.year AS year
            ORDER BY p.year DESC
            LIMIT 10
            """, topic=topic)
        return [{"title": record["title"], "abstract": record["abstract"], "year": record["year"]} for record in result]

    @staticmethod
    def _fetch_paper_by_title(tx, title):
        """
        Helper function to fetch a paper by its title.
        :param tx: The transaction object.
        :param title: The title of the paper to search for.
        :return: List of papers with the specified title.
        """
        result = tx.run("""
            MATCH (p:Paper {title: $title})
            RETURN p.title AS title, p.abstract AS abstract, p.year AS year
            """, title=title)
        return [{"title": record["title"], "abstract": record["abstract"], "year": record["year"]} for record in result]


# Test the Neo4j connection and functionality
if __name__ == "__main__":
    # Initialize connection to Neo4j
    neo4j_db = Neo4jDatabase()

    # Test storing paper data
    paper_data = {
        "title": "Artificial Intelligence in Healthcare",
        "abstract": "This paper discusses the applications of AI in healthcare, particularly in diagnosis.",
        "authors": ["John Doe", "Jane Smith"],
        "year": 2023,
        "topics": ["AI", "Healthcare"]
    }

    # Store paper data in Neo4j
    neo4j_db.store_paper(paper_data)

    # Fetch papers by topic
    topic = "AI"
    papers = neo4j_db.fetch_papers_by_topic(topic)
    
    print(f"Papers on {topic}:")
    for paper in papers:
        print(f"Title: {paper['title']}, Abstract: {paper['abstract']}, Year: {paper['year']}")

    # Fetch paper by title
    paper_title = "Artificial Intelligence in Healthcare"
    paper_info = neo4j_db.fetch_paper_by_title(paper_title)
    print(f"\nDetails for paper titled '{paper_title}':")
    for paper in paper_info:
        print(f"Title: {paper['title']}, Abstract: {paper['abstract']}, Year: {paper['year']}")

    # Close the connection
    neo4j_db.close()
