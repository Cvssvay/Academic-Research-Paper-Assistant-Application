# ollama_api.py
import requests
from config import CONFIG

class OllamaAPI:
    def __init__(self):
        """Initialize the Ollama API configuration."""
        self.api_url = CONFIG["ollama"]["api_url"]
        self.model_name = CONFIG["ollama"]["model"]
    
    def query(self, prompt):
        """Send a query to the Ollama API and get a response."""
        headers = {"Content-Type": "application/json"}
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model_name,
            "temperature": 0.7
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Error: Unable to get response from Ollama."
