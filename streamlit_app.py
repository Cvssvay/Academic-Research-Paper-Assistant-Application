# streamlit_app.py
import streamlit as st
from file_handler import save_uploaded_file, clear_temp_files
from neo4j_handler import Neo4jHandler
from pdf_processor_ import extract_text_from_pdf
from chatbot import Chatbot
from datetime import datetime

# Initialize handlers
neo4j_handler = Neo4jHandler()
chatbot = Chatbot()

def app():
    st.title("Research Paper Assistant Chatbot")
    st.write("This app helps you interact with research papers using a chatbot. Upload your PDFs and get started!")

    # File upload
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save uploaded files temporarily
            temp_file_path = save_uploaded_file(uploaded_file)
            
            # Extract text from PDF
            paper_content = extract_text_from_pdf(temp_file_path)
            paper_title = uploaded_file.name
            publish_date = datetime.now().strftime("%Y-%m-%d")

            # Store paper in Neo4j
            neo4j_handler.store_paper(paper_title, paper_content, publish_date)
            st.success(f"Paper '{paper_title}' has been processed and stored in Neo4j.")

            # Clear temporary files after processing
            clear_temp_files()

    # Chatbot interaction
    user_input = st.text_input("Ask the bot", "")
    if user_input:
        response = chatbot.handle_query(user_input)
        st.write(f"Bot: {response}")

    # Show instructions in the sidebar
    st.sidebar.header("Instructions")
    st.sidebar.write("""
    - Upload your research papers (PDF format).
    - The bot can summarize papers or suggest future research work based on them.
    - You can also ask general questions about the content.
    - Type 'exit' to stop interacting with the bot.
    """)

if __name__ == "__main__":
    app()
