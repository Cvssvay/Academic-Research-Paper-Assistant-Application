# pdf_processor.py
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file_path):
    """Extract text from a given PDF file."""
    document = fitz.open(pdf_file_path)
    text = ""
    for page in document:
        text += page.get_text()
    return text
