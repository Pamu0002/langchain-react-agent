from langchain_core.tools import tool, Tool
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import config
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
            docs = loader.load()
            full_text = "\n\n".join(doc.page_content for doc in docs)
        elif ext in (".txt", ".md"):
            loader = TextLoader(filepath, encoding="utf-8")
            docs = loader.load()
            full_text = "\n\n".join(doc.page_content for doc in docs)
        elif ext == ".docx":
            # Use docx2txt for .docx files
            try:
                import docx2txt
                full_text = docx2txt.process(filepath)
            except ImportError:
                return f"Unsupported file type: {ext} (docx2txt not installed)"
        else:
            return f"Unsupported file type: {ext}"
        
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

def _read_document_impl(filename: str) -> str:
    """
    Read and return the contents of an uploaded document.
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

def _list_documents_impl(placeholder: str = "") -> str:
    """
    List all documents that have been uploaded and are available to read.
    """
    # Scan uploads folder
    if not os.path.exists(config.upload_dir):
        return "No documents uploaded yet."
    
    files = [
        f for f in os.listdir(config.upload_dir)
        if os.path.splitext(f)[1].lower() in config.allowed_extensions
    ]
    
    if not files:
        return "No documents uploaded yet. Please upload a PDF, TXT, DOCX, or Markdown file."
    
    return f"Available documents: {', '.join(files)}"


# Create tools as Tool objects instead of using @tool decorator
read_document = Tool(
    name="read_document",
    func=_read_document_impl,
    description="""Read and return the contents of an uploaded document.
Use this when the user asks questions about a file they uploaded,
wants you to summarise a document, or refers to a file by name.
Input should be the filename (e.g. 'report.pdf' or 'notes.txt').
Returns the full text content of the document."""
)

list_documents = Tool(
    name="list_documents",
    func=_list_documents_impl,
    description="""List all documents that have been uploaded and are available to read.
Use this when the user asks what files are available or uploaded.
Input can be any string or empty string."""
)
