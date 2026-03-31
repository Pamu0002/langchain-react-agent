from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage, AIMessage
from config import config
from typing import Dict
import uuid

# Store one memory object per session
_sessions: Dict[str, ConversationBufferWindowMemory] = {}

def get_or_create_session(session_id: str = None) -> tuple:
    """Get existing session memory or create a new one. Returns (session_id, memory)."""
    if session_id is None or session_id not in _sessions:
        session_id = session_id or str(uuid.uuid4())[:8]
        _sessions[session_id] = ConversationBufferWindowMemory(
            k=config.max_history_messages,
            return_messages=True,
            memory_key="chat_history"
        )
    return session_id, _sessions[session_id]

def clear_session(session_id: str) -> bool:
    """Clear memory for a specific session."""
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False

def get_history_as_text(session_id: str) -> str:
    """Return conversation history as a plain string for display."""
    if session_id not in _sessions:
        return ""
    memory = _sessions[session_id]
    messages = memory.load_memory_variables({}).get("chat_history", [])
    lines = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            lines.append(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            lines.append(f"ARIA: {msg.content}")
    return "\n".join(lines)
