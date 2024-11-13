# file_handler.py
import os
import shutil
from config import CONFIG

def save_uploaded_file(uploaded_file):
    """Save uploaded files temporarily."""
    temp_dir = CONFIG["temp_file_path"]
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path

def clear_temp_files():
    """Clear all temporary files after processing."""
    temp_dir = CONFIG["temp_file_path"]
    shutil.rmtree(temp_dir)
