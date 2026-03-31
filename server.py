from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import aiofiles
import logging

from config import config
from agent import run_agent
from memory import clear_session, get_history_as_text
from tools.doc_reader import load_document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ARIA - Personal AI Assistant",
    description="Agentic Research & Intelligence Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request / Response models ---

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    success: bool

class ClearRequest(BaseModel):
    session_id: str

# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0", "model": config.model_name}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    logger.info(f"Chat request — session: {request.session_id}, message: {request.message[:80]}")
    
    result = run_agent(
        message=request.message,
        session_id=request.session_id
    )
    
    return ChatResponse(
        response=result["response"],
        session_id=result["session_id"],
        success=result["success"]
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in config.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(config.allowed_extensions)}"
        )
    
    # Validate size
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > config.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {config.max_file_size_mb}MB"
        )
    
    # Save file
    save_path = os.path.join(config.upload_dir, file.filename)
    async with aiofiles.open(save_path, "wb") as f:
        await f.write(content)
    
    # Pre-load into memory
    load_document(save_path)
    
    logger.info(f"File uploaded: {file.filename} ({size_mb:.2f}MB)")
    return {
        "filename": file.filename,
        "size_mb": round(size_mb, 2),
        "message": f"'{file.filename}' uploaded successfully. You can now ask ARIA about it."
    }

@app.post("/clear")
async def clear_memory(request: ClearRequest):
    cleared = clear_session(request.session_id)
    return {"cleared": cleared, "session_id": request.session_id}

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    history = get_history_as_text(session_id)
    return {"session_id": session_id, "history": history}

# Serve frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_ui():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "ARIA API is running. Frontend not found."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host=config.host, port=config.port, reload=True)
