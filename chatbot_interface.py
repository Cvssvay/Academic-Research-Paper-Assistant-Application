# chatbot_interface.py
from ollama_api import OllamaAPI

class Chatbot:
    def __init__(self):
        """Initialize the chatbot with Ollama API handler."""
        self.ollama = OllamaAPI()
    
    def start(self):
        """Start the chatbot interface to interact with the user."""
        print("Welcome to the Research Paper Assistant Chatbot!")
        print("Type 'exit' to end the conversation.")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            # Handle different types of queries
            if "summarize" in user_input.lower():
                prompt = f"Summarize the advancements in the following papers: {user_input}"
            elif "future work" in user_input.lower():
                prompt = f"Suggest future research directions based on these papers: {user_input}"
            else:
                prompt = user_input  # Generic query
            
            response = self.ollama.query(prompt)
            print(f"Bot: {response}")
