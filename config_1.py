# config.py

# Configuration settings for Neo4j and Ollama API
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
    "temp_file_path": "temp_papers/"  # Temporary folder for uploaded files
}
