# Research Paper Assistant Chatbot

The **Research Paper Assistant Chatbot** is a system designed to help users interact with research papers in an efficient and intelligent way. It allows users to upload research papers in PDF format, stores their content in a Neo4j database, and uses an AI-powered chatbot (via the Ollama API) to answer queries related to the papers, such as summarizing the content or suggesting future research directions.

This project integrates the following components:
- **PDF Text Extraction**: Extract text from PDF papers using `PyMuPDF` (fitz).
- **Neo4j**: Store paper metadata and content in a Neo4j graph database.
- **Ollama Chatbot**: A custom chatbot built on the Ollama API that can summarize papers and suggest future research work.
- **Streamlit UI**: A user-friendly web interface to interact with the chatbot and upload papers.

## Features
- **Upload and Process PDFs**: Users can upload PDF papers, and the system extracts and stores their content in a Neo4j database.
- **AI-powered Queries**: The chatbot can answer a variety of queries, including:
  - Summarizing papers
  - Suggesting future research based on paper content
  - Providing general information or answering specific questions about the papers
- **Neo4j Storage**: Papers are stored as nodes in the Neo4j graph database with metadata such as title, content, and publication date.
- **Streamlit Interface**: A simple web-based interface to interact with the system, upload files, and chat with the assistant.

## Requirements

### Python Dependencies
To run the project, you will need to install the following Python libraries:

```bash
pip install requests pymupdf neo4j streamlit
