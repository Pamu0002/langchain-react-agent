"""FastAPI routes for ARIA"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from src.api.models import (
    ChatRequest, ChatResponse, ClearRequest, ClearResponse,
    HealthResponse, AgentListResponse
)
from src.agents import run_multi_agent
from src.memory import clear_session, get_history_as_text
from src.tools.doc_reader import load_document
from src.config import config
import os
import aiofiles
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "model": config.model_name
    }

@router.get("/agents", response_model=AgentListResponse)
async def list_agents():
    """List available agents and their specialties"""
    return {
        "system": "Multi-Agent with Intelligent Coordinator",
        "agents": {
            "research": {
                "name": "Research Agent",
                "description": "Specialized in web search and current information",
                "tools": ["web_search"],
                "best_for": "News, trends, real-time data"
            },
            "document": {
                "name": "Document Agent",
                "description": "Specialized in reading and analyzing documents",
                "tools": ["read_document", "list_documents"],
                "best_for": "PDF analysis, document summarization"
            },
            "general": {
                "name": "General Q&A Agent",
                "description": "Specialized in reasoning and knowledge-based questions",
                "tools": [],
                "best_for": "Explanations, reasoning, general knowledge"
            },
            "code": {
                "name": "Code/Technical Agent",
                "description": "Specialized in programming and technical topics",
                "tools": ["web_search"],
                "best_for": "Coding questions, tech help, debugging"
            }
        },
        "routing": {
            "auto": {
                "agent_type": None,
                "description": "Coordinator automatically analyzes query and routes to best agent"
            },
            "manual": {
                "agent_type": "research|document|general|code",
                "description": "Specify which agent to use directly"
            }
        }
    }

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint - main API for user queries"""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    logger.info(f"Chat request — session: {request.session_id}")
    
    # Always use multi-agent with coordinator routing
    result = run_multi_agent(
        message=request.message,
        session_id=request.session_id,
        agent_type=request.agent_type
    )
    
    return ChatResponse(
        response=result["response"],
        session_id=result["session_id"],
        success=result["success"],
        agent_used=result.get("agent_used", "Coordinator-Routed Agent")
    )

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload document file"""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in config.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(config.allowed_extensions)}"
        )
    
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > config.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {config.max_file_size_mb}MB"
        )
    
    save_path = os.path.join(config.upload_dir, file.filename)
    async with aiofiles.open(save_path, "wb") as f:
        await f.write(content)
    
    load_document(save_path)
    
    logger.info(f"File uploaded: {file.filename} ({size_mb:.2f}MB)")
    return {
        "filename": file.filename,
        "size_mb": round(size_mb, 2),
        "message": f"'{file.filename}' uploaded successfully. You can now ask ARIA about it."
    }

@router.post("/clear", response_model=ClearResponse)
async def clear_memory(request: ClearRequest):
    """Clear conversation memory for a session"""
    cleared = clear_session(request.session_id)
    return {
        "cleared": cleared,
        "session_id": request.session_id
    }

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history for a session"""
    history = get_history_as_text(session_id)
    return {
        "session_id": session_id,
        "history": history
    }
