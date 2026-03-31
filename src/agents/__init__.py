"""
ARIA Agents Package

Multi-agent system with specialist agents:
- Research Agent: Web search and current information
- Document Agent: File analysis and understanding
- General Agent: Knowledge-based Q&A
- Code Agent: Programming and technical help
- Coordinator: Intelligent routing
"""

from src.agents.research import ResearchAgent
from src.agents.document import DocumentAgent
from src.agents.general import GeneralAgent
from src.agents.code import CodeAgent
from src.agents.coordinator import Coordinator
import logging

logger = logging.getLogger(__name__)

# Initialize agents
research_agent = ResearchAgent()
document_agent = DocumentAgent()
general_agent = GeneralAgent()
code_agent = CodeAgent()
coordinator = Coordinator()

# Agent registry
AGENTS = {
    "research": research_agent,
    "document": document_agent,
    "general": general_agent,
    "code": code_agent,
}


def run_multi_agent(message: str, session_id: str = None, agent_type: str = None) -> dict:
    """
    Run appropriate agent based on message content.
    
    Args:
        message: User message
        session_id: Session ID for memory
        agent_type: Optional override - 'research', 'document', 'general', 'code'
    
    Returns:
        dict with response, session_id, agent_used, success
    """
    # Determine which agent to use
    if agent_type is None:
        agent_type = coordinator.determine_agent(message, session_id)
    
    logger.info(f"Multi-agent system using {agent_type} agent")
    
    # Get agent
    agent = AGENTS.get(agent_type, general_agent)
    
    # Run agent
    return agent.run(message, session_id=session_id)


__all__ = [
    "ResearchAgent",
    "DocumentAgent",
    "GeneralAgent",
    "CodeAgent",
    "Coordinator",
    "run_multi_agent",
]
