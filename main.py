"""ARIA - Main Entry Point

Run this file to start the FastAPI server:
    python main.py

Server will be available at http://localhost:8000
Frontend UI at http://localhost:8000/
"""

import uvicorn
import logging
from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Start the ARIA server"""
    logger.info(f"🚀 Starting ARIA on {config.host}:{config.port}")
    logger.info(f"📡 Using model: {config.model_name}")
    logger.info(f"🌐 Frontend: http://localhost:{config.port}")
    
    from src.api import create_app
    app = create_app()
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info"
    )

if __name__ == "__main__":
    main()
