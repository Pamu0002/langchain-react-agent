from langchain_core.tools import tool
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import config
import os
import logging

logger = logging.getLogger(__name__)

# Store extracted text in memory keyed by filename
_loaded_docs: dict = {}

def load_document(filepath: str) -> str:
    """Load a document file and return its full text content."""
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(filepath)
        elif ext in (".txt", ".md"):
            loader = TextLoader(filepath, encoding="utf-8")
        elif ext == ".docx":
            loader = Docx2txtLoader(filepath)
        else:
            return f"Unsupported file type: {ext}"
        
        docs = loader.load()
        full_text = "\n\n".join(doc.page_content for doc in docs)
        filename = os.path.basename(filepath)
        _loaded_docs[filename] = full_text
        logger.info(f"Loaded document: {filename} ({len(full_text)} chars)")
        return full_text
    except Exception as e:
        logger.error(f"Failed to load {filepath}: {e}")
        return f"Error loading document: {str(e)}"

def get_loaded_filenames() -> list:
    """Return list of currently loaded document filenames."""
    return list(_loaded_docs.keys())

@tool
def read_document(filename: str) -> str:
    """
    Read and return the contents of an uploaded document.
    Use this when the user asks questions about a file they uploaded,
    wants you to summarise a document, or refers to a file by name.
    Input should be the filename (e.g. 'report.pdf' or 'notes.txt').
    Returns the full text content of the document.
    """
    # Check if already loaded in memory
    if filename in _loaded_docs:
        text = _loaded_docs[filename]
        return text[:6000] + ("\n\n[Document truncated for length...]" if len(text) > 6000 else "")
    
    # Try to load from uploads directory
    filepath = os.path.join(config.upload_dir, filename)
    if not os.path.exists(filepath):
        available = get_loaded_filenames()
        if available:
            return f"File '{filename}' not found. Available files: {', '.join(available)}"
        return f"File '{filename}' not found. Please upload a file first."
    
    text = load_document(filepath)
    return text[:6000] + ("\n\n[Document truncated for length...]" if len(text) > 6000 else "")

@tool
def list_documents(placeholder: str = "") -> str:
    """
    List all documents that have been uploaded and are available to read.
    Use this when the user asks what files are available or uploaded.
    Input can be any string or empty string.
    """
    # Scan uploads folder
    if not os.path.exists(config.upload_dir):
        return "No documents uploaded yet."
    
    files = [
        f for f in os.listdir(config.upload_dir)
        if os.path.splitext(f)[1].lower() in config.allowed_extensions
    ]
    
    if not files:
        return "No documents uploaded yet. Upload a PDF, TXT, or DOCX file to get started."
    
    return "Available documents:\n" + "\n".join(f"- {f}" for f in files)
