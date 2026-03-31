"""API models for request/response validation"""

from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_multi_agent: Optional[bool] = False
    agent_type: Optional[str] = None

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
    single_agent: dict
    multi_agents: dict
    usage: dict
