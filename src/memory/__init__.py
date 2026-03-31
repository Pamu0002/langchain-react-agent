from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from src.config import config
from typing import Dict, List
import uuid
import logging

logger = logging.getLogger(__name__)

# Store one conversation history per session
_sessions: Dict[str, List[BaseMessage]] = {}


def get_or_create_session(session_id: str = None) -> tuple:
    """Get existing session or create a new one. Returns (session_id, memory_object)."""
    if session_id is None or session_id not in _sessions:
        session_id = session_id or str(uuid.uuid4())[:8]
        _sessions[session_id] = []
    
    return session_id, SimpleChatMemory(_sessions[session_id])


def clear_session(session_id: str) -> bool:
    """Clear memory for a specific session."""
    if session_id in _sessions:
        del _sessions[session_id]
        logger.info(f"Cleared session: {session_id}")
        return True
    return False


def get_history_as_text(session_id: str) -> str:
    """Return conversation history as a plain string for display."""
    if session_id not in _sessions:
        return ""
    
    messages = _sessions[session_id]
    lines = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            lines.append(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            lines.append(f"ARIA: {msg.content}")
    
    return "\n".join(lines)


# Simple wrapper class for memory operations  
class SimpleChatMemory:
    """Simple chat memory wrapper"""
    
    def __init__(self, messages: List[BaseMessage]):
        self.messages = messages
        self.chat_memory = self  # For compatibility
    
    def add_user_message(self, content: str):
        """Add user message"""
        self.messages.append(HumanMessage(content=content))
        # Keep last N messages
        if len(self.messages) > config.max_history_messages * 2:
            self.messages = self.messages[-config.max_history_messages:]
    
    def add_ai_message(self, content: str):
        """Add AI message"""
        self.messages.append(AIMessage(content=content))
        # Keep last N messages
        if len(self.messages) > config.max_history_messages * 2:
            self.messages = self.messages[-config.max_history_messages:]
    
    @property
    def buffer(self) -> str:
        """Get buffer as text"""
        lines = []
        for msg in self.messages:
            if isinstance(msg, HumanMessage):
                lines.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                lines.append(f"ARIA: {msg.content}")
        return "\n".join(lines)
