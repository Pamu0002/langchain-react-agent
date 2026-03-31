from langchain_groq import ChatGroq
from src.config import config
from src.memory import get_or_create_session
import logging

logger = logging.getLogger(__name__)

COORDINATOR_PROMPT = """You are ARIA's Coordinator Agent. Your job is to route user requests to the most appropriate specialist agent.

Available Specialist Agents:
1. **Research Agent** - Use for:
   - Current news, trends, latest information
   - "Search for...", "What's new...", "Find information about..."
   - Questions needing real-time web data

2. **Document Agent** - Use for:
   - Analyzing uploaded files
   - "Summarize this...", "What files do I have..."
   - "Tell me about the document...", "Extract from PDF..."

3. **General Q&A Agent** - Use for:
   - General knowledge questions
   - Explanations and reasoning
   - "Explain...", "How does...", "What is..."

4. **Code/Technical Agent** - Use for:
   - Programming questions and coding examples
   - Technology and framework help
   - "How do I code...", "Debug this...", "Explain React...", "Python question..."

Respond with ONLY the agent name (exactly as listed above) based on the user query.
If unsure, choose General Q&A Agent.

User Query: {input}

Response (agent name only):"""

class Coordinator:
    """Coordinator Agent - routes requests to appropriate specialist agent"""
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=config.groq_api_key,
            model=config.model_name,
            temperature=0.3,  # Lower temperature for routing
            max_tokens=50,
        )
    
    def determine_agent(self, user_message: str, session_id: str = None) -> str:
        """
        Analyze user message and determine best agent
        
        Returns: 'research', 'document', 'general', or 'code'
        """
        session_id, memory = get_or_create_session(session_id)
        
        response = self.llm.invoke(COORDINATOR_PROMPT.format(input=user_message))
        agent_choice = response.content.strip().lower()
        
        logger.info(f"Coordinator routing: {agent_choice} for query: {user_message[:60]}")
        
        # Match agent choice
        if "research" in agent_choice:
            return "research"
        elif "document" in agent_choice:
            return "document"
        elif "code" in agent_choice or "technical" in agent_choice:
            return "code"
        else:
            return "general"
