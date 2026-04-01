"""API models for request/response validation"""

from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    agent_type: Optional[str] = None  # Optional: specify agent directly, or None for auto-routing

class ChatResponse(BaseModel):
    response: str
    session_id: str
    success: bool
    agent_used: Optional[str] = None

class ClearRequest(BaseModel):
    session_id: str

class ClearResponse(BaseModel):
    cleared: bool
    session_id: str

class HealthResponse(BaseModel):
    status: str
    version: str
    model: str

class AgentListResponse(BaseModel):
    system: str
    agents: dict
    routing: dict
