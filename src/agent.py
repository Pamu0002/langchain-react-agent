"""Original single agent for backward compatibility"""

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.tools import tool
from src.config import config
from src.memory import get_or_create_session
from src.tools import web_search, read_document, list_documents
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are ARIA, a helpful and intelligent personal assistant.

You have access to the following tools:
- web_search: Search the internet for current information
- read_document: Read the contents of an uploaded file
- list_documents: See what files have been uploaded

Guidelines:
- Be concise and helpful. Get to the point.
- Use web_search when the user needs current or real-time information.
- Use read_document when the user mentions a file or asks about an uploaded document.
- Use list_documents when the user asks what files are available.
- If you don't need a tool, just answer directly from your knowledge.
- Always cite sources when you use web search results.
- If you're unsure, say so — don't make things up.

Conversation history is provided below. Use it to maintain context.
"""

ALL_TOOLS = [web_search, read_document, list_documents]

def build_simple_chain(session_id: str = None):
    """Build simple LLM chain without agent"""
    session_id, memory = get_or_create_session(session_id)
    
    llm = ChatGroq(
        api_key=config.groq_api_key,
        model=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    
    # Simple prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "{input}")
    ])
    
    # Create chain
    chain = prompt | llm
    
    return chain, session_id, memory


def run_agent(message: str, session_id: str = None) -> dict:
    """Run single agent"""
    chain, session_id, memory = build_simple_chain(session_id)
    
    try:
        # Get conversation history
        history = memory.buffer if hasattr(memory, 'buffer') else ""
        input_text = f"Chat History:\n{history}\n\nCurrent message: {message}"
        
        result = chain.invoke({"input": input_text})
        response = result.content if hasattr(result, 'content') else str(result)
        
        # Store in memory
        memory.chat_memory.add_user_message(message)
        memory.chat_memory.add_ai_message(response)
        
        return {
            "response": response,
            "session_id": session_id,
            "success": True
        }
    except Exception as e:
        logger.error(f"Agent error: {e}")
        return {
            "response": f"I encountered an error: {str(e)}. Please try again.",
            "session_id": session_id,
            "success": False
        }
