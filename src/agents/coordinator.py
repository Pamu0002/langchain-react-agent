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
   - Anything requiring internet search

2. **Document Agent** - Use for:
   - Analyzing uploaded files (PDF, TXT, DOCX, MD)
   - "Summarize this...", "What files do I have...", "I've loaded..."
   - "Tell me about the document...", "Extract from PDF..."
   - File analysis, document reading, file-related questions
   - Anything mentioning files, PDF, documents, papers, reports

3. **General Q&A Agent** - Use for:
   - General knowledge questions
   - Explanations and reasoning
   - "Explain...", "How does...", "What is...", "Why..."
   - Conceptual questions and definitions

4. **Code/Technical Agent** - Use for:
   - Programming questions and coding examples
   - Technology and framework help
   - "How do I code...", "Debug this...", "Explain React...", "Python question..."
   - Anything related to programming, coding, tech

Respond with ONLY the agent name (exactly as listed above) based on the user query.
If unsure, choose General Q&A Agent.

Examples:
- "Summarize my PDF" → Document Agent
- "I've loaded data.csv, what's inside?" → Document Agent
- "Find me AI news" → Research Agent
- "How do I code a loop?" → Code/Technical Agent
- "What is quantum computing?" → General Q&A Agent

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
        Analyze user message and determine best agent.
        First checks for explicit keywords, then uses LLM for complex queries.
        
        Returns: 'research', 'document', 'general', or 'code'
        """
        msg = user_message.lower()
        
        # Explicit keyword matching for common cases
        doc_keywords = ["pdf", "document", "file", "upload", "loaded", "summarize", "paper", "report", "docx", "txt", "markdown", "analyze document", "extract from", "read file"]
        code_keywords = ["code", "python", "javascript", "java", "c++", "debug", "programming", "function", "class", "variable", "algorithm", "framework", "library"]
        research_keywords = ["search", "find", "news", "latest", "trend", "current", "recent", "web", "google"]
        
        # Check for document-related queries
        if any(keyword in msg for keyword in doc_keywords):
            logger.info(f"Coordinator detected DOCUMENT query")
            return "document"
        
        # Check for code-related queries
        if any(keyword in msg for keyword in code_keywords):
            logger.info(f"Coordinator detected CODE query")
            return "code"
        
        # Check for research queries
        if any(keyword in msg for keyword in research_keywords):
            logger.info(f"Coordinator detected RESEARCH query")
            return "research"
        
        # For complex queries, use LLM
        session_id, memory = get_or_create_session(session_id)
        
        response = self.llm.invoke(COORDINATOR_PROMPT.format(input=user_message))
        agent_choice = response.content.strip().lower()
        
        logger.info(f"Coordinator LLM routing: {agent_choice} for query: {user_message[:60]}")
        
        # Match agent choice
        if "research" in agent_choice:
            return "research"
        elif "document" in agent_choice:
            return "document"
        elif "code" in agent_choice or "technical" in agent_choice:
            return "code"
        else:
            return "general"
