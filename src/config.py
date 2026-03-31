from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:
    """Centralized configuration for ARIA"""
    
    # LLM
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    model_name: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 2048

    # Tools
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    max_search_results: int = 5

    # Memory
    max_history_messages: int = 20

    # Files
    upload_dir: str = "uploads"
    allowed_extensions: tuple = (".pdf", ".txt", ".docx", ".md")
    max_file_size_mb: int = 10

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list = None

    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]
        os.makedirs(self.upload_dir, exist_ok=True)

config = Config()
