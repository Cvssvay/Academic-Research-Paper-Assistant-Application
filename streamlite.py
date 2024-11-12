import os
import requests
import fitz  # PyMuPDF for PDF processing
from datetime import datetime
from neo4j import GraphDatabase
import streamlit as st

# Neo4j Setup
uri = "bolt://localhost:7687"  # Default URI for local Neo4j
username = "neo4j"  # Default username for Neo4j
password = "12345678"  # Replace with your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

# Ollama API setup
ollama_url = "http://127.0.0.1:11434/v1/chat/completions"  # Ollama API endpoint (using 127.0.0.1 for local access)
ollama_model = "llama2"  # You can change the model if needed

def get_ollama_response(prompt):
    """Send a prompt to Ollama API and return the response."""
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": ollama_model,
        "temperature": 0.7,
    }
    response = requests.post(ollama_url, json=data, headers=headers)
    response_data = response.json()
    
    if response.status_code == 200:
        return response_data['choices'][0]['message']['content']
    else:
        return "Error: Could not get response from Ollama."

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def store_paper_in_neo4j(title, content, publish_date):
    """Store paper information in Neo4j."""
    with driver.session() as session:
        session.run(
            "CREATE (p:Paper {title: $title, content: $content, publish_date: $publish_date})",
            title=title, content=content, publish_date=publish_date
        )

def process_papers(papers_folder):
    """Loop through papers and store them in Neo4j."""
    for filename in os.listdir(papers_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(papers_folder, filename)
            paper_content = extract_text_from_pdf(pdf_path)
            paper_title = filename  # You can replace this with better title extraction logic
            publish_date = datetime.now().strftime("%Y-%m-%d")  # Replace with actual publish date if available
            store_paper_in_neo4j(paper_title, paper_content, publish_date)

# Streamlit User Interface
def app():
    st.title("Research Paper Assistant Chatbot")
    st.write("This app helps you interact with research papers using a chatbot. Upload your PDFs and get started!")

    # File upload
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

    # Process uploaded files and store in Neo4j
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract text from PDF
            paper_content = extract_text_from_pdf(f"temp_{uploaded_file.name}")
            paper_title = uploaded_file.name
            publish_date = datetime.now().strftime("%Y-%m-%d")

            # Store paper in Neo4j
            store_paper_in_neo4j(paper_title, paper_content, publish_date)
            st.success(f"Paper '{paper_title}' has been processed and stored in Neo4j.")

    # Chatbot interaction
    user_input = st.text_input("Ask the bot", "")
    if user_input:
        # Handle different types of queries
        if "summarize" in user_input.lower():
            prompt = f"Summarize the advancements in the following papers: {user_input}"
        elif "future work" in user_input.lower():
            prompt = f"Suggest future work based on these papers: {user_input}"
        else:
            prompt = user_input  # General query to answer questions
        
        response = get_ollama_response(prompt)
        st.write(f"Bot: {response}")

    # Show instructions
    st.sidebar.header("Instructions")
    st.sidebar.write("""
    - Upload your research papers (PDF format).
    - The bot can summarize papers or suggest future research work based on them.
    - You can also ask general questions about the content.
    - Type 'exit' to stop interacting with the bot.
    """)

# Run the Streamlit app
if __name__ == "__main__":
    app()
