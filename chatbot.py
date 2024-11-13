# chatbot.py
from ollama_api_ import OllamaAPI

class Chatbot:
    def __init__(self):
        """Initialize the chatbot with the Ollama API handler."""
        self.ollama_api = OllamaAPI()

    def handle_query(self, user_input):
        """Process user input and return a response."""
        if "summarize" in user_input.lower():
            prompt = f"Summarize the advancements in the following papers: {user_input}"
        elif "future work" in user_input.lower():
            prompt = f"Suggest future work based on these papers: {user_input}"
        else:
            prompt = user_input  # General query
        return self.ollama_api.get_response(prompt)
