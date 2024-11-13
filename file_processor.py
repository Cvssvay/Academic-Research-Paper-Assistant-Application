# file_processor.py
import os
from datetime import datetime
from pdf_processor import extract_text_from_pdf
from database import Neo4jHandler
from config import CONFIG

class FileProcessor:
    def __init__(self):
        """Initialize the file processor with a Neo4j handler."""
        self.db_handler = Neo4jHandler()
    
    def process_pdfs(self):
        """Process and store PDF papers from the specified folder into Neo4j."""
        folder_path = CONFIG["papers_directory"]
        
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(".pdf"):
                file_path = os.path.join(folder_path, file_name)
                paper_text = extract_text_from_pdf(file_path)
                paper_title = file_name  # You can improve this logic for title extraction
                publish_date = datetime.now().strftime("%Y-%m-%d")  # Placeholder for actual publish date
                self.db_handler.store_paper(paper_title, paper_text, publish_date)

    def close(self):
        """Close the database handler after processing."""
        self.db_handler.close()
