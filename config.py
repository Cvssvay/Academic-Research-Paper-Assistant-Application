# config.py

# Configuration settings for the application
CONFIG = {
    "neo4j": {
        "uri": "bolt://localhost:7687",
        "username": "neo4j",
        "password": "12345678"
    },
    "ollama": {
        "api_url": "http://127.0.0.1:11434/v1/chat/completions",
        "model": "llama2"
    },
    "papers_directory": r"C:\Users\yashn\OneDrive\Desktop\Attention_Ai\data"  # Path to the folder containing PDFs
}
