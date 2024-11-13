# ollama_api.py
import requests
from config import CONFIG

class OllamaAPI:
    def __init__(self):
        """Initialize the Ollama API handler."""
        self.api_url = CONFIG["ollama"]["api_url"]
        self.model = CONFIG["ollama"]["model"]

    def get_response(self, prompt):
        """Send a prompt to the Ollama API and return the response."""
        headers = {"Content-Type": "application/json"}
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model,
            "temperature": 0.7
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Error: Unable to get response from Ollama."
