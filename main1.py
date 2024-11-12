import os
import requests
import fitz  # PyMuPDF for PDF processing
from datetime import datetime
from neo4j import GraphDatabase

# Neo4j Setup
neo4j_uri = "bolt://localhost:7687"  # Default URI for local Neo4j
neo4j_username = "neo4j"  # Default username for Neo4j
neo4j_password = "12345678"  # Replace with your Neo4j password
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

# Ollama API setup
ollama_api_url = "http://127.0.0.1:11434/v1/chat/completions"  # Ollama API endpoint (using 127.0.0.1 for local access)
ollama_model_name = "llama2"  # You can change the model if needed

def get_ollama_response_from_prompt(prompt_text):
    """Send a prompt to Ollama API and return the response."""
    headers = {"Content-Type": "application/json"}
    request_data = {
        "messages": [{"role": "user", "content": prompt_text}],
        "model": ollama_model_name,
        "temperature": 0.7,
    }
    response = requests.post(ollama_api_url, json=request_data, headers=headers)
    response_data = response.json()
    
    if response.status_code == 200:
        return response_data['choices'][0]['message']['content']
    else:
        return "Error: Could not get response from Ollama."

def extract_text_from_pdf_file(pdf_file_path):
    """Extract text from a PDF file."""
    document = fitz.open(pdf_file_path)
    extracted_text = ""
    for page in document:
        extracted_text += page.get_text()
    return extracted_text

def store_paper_data_in_neo4j(paper_title, paper_content, paper_publish_date):
    """Store paper information in Neo4j."""
    with neo4j_driver.session() as session:
        session.run(
            "CREATE (p:Paper {title: $paper_title, content: $paper_content, publish_date: $paper_publish_date})",
            paper_title=paper_title, paper_content=paper_content, paper_publish_date=paper_publish_date
        )

def initiate_chatbot_interface():
    """Start the chatbot interface to interact with the user."""
    print("Welcome to the Research Paper Assistant Chatbot!")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_message = input("You: ")
        
        if user_message.lower() == "exit":
            print("Goodbye!")
            break
        
        # Handle different types of queries
        if "summarize" in user_message.lower():
            prompt_text = f"Summarize the advancements in the following papers: {user_message}"
        elif "future work" in user_message.lower():
            prompt_text = f"Suggest future work based on these papers: {user_message}"
        else:
            prompt_text = user_message  # General query to answer questions
        
        response_message = get_ollama_response_from_prompt(prompt_text)
        print(f"Bot: {response_message}")

def process_papers_in_directory(papers_directory):
    """Loop through papers in the specified folder and store them in Neo4j."""
    for file_name in os.listdir(papers_directory):
        if file_name.endswith(".pdf"):
            pdf_file_path = os.path.join(papers_directory, file_name)
            paper_text_content = extract_text_from_pdf_file(pdf_file_path)
            paper_title = file_name  # You can replace this with better title extraction logic
            paper_publish_date = datetime.now().strftime("%Y-%m-%d")  # Replace with actual publish date if available
            store_paper_data_in_neo4j(paper_title, paper_text_content, paper_publish_date)

# Main program execution
if __name__ == "__main__":
    papers_directory_path = r"C:\Users\yashn\OneDrive\Desktop\Attention_Ai\data"  # Folder containing PDF papers

    # Process all papers in the folder and store them in Neo4j
    process_papers_in_directory(papers_directory_path)
    
    # Start the chatbot interface
    initiate_chatbot_interface()
