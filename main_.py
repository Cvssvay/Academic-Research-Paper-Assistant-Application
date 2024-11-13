# main.py
from file_processor import FileProcessor
from chatbot_interface import Chatbot

def main():
    # Step 1: Process the PDFs and store them in the database
    file_processor = FileProcessor()
    file_processor.process_pdfs()
    
    # Step 2: Start the chatbot interface
    chatbot = Chatbot()
    chatbot.start()
    
    # Close resources
    file_processor.close()

if __name__ == "__main__":
    main()
