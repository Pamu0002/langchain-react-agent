from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain import hub
from config import config
from memory import get_or_create_session
from tools.search import web_search
from tools.doc_reader import read_document, list_documents
import logging

logger = logging.getLogger(__name__)

# All tools available to the agent
TOOLS = [web_search, read_document, list_documents]

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

def build_agent_executor(session_id: str = None) -> tuple:
    """Build and return (agent_executor, session_id, memory)."""
    session_id, memory = get_or_create_session(session_id)
    
    llm = ChatGroq(
        api_key=config.groq_api_key,
        model=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )

    # Pull standard ReAct prompt from LangChain Hub and inject system context
    try:
        prompt = hub.pull("hwchase17/react-chat")
    except Exception:
        # Fallback prompt if hub is unavailable
        prompt = PromptTemplate.from_template(
            SYSTEM_PROMPT + "\n\n{chat_history}\n\nQuestion: {input}\n\n"
            "Available tools: {tools}\nTool names: {tool_names}\n\n"
            "{agent_scratchpad}"
        )

    agent = create_react_agent(llm=llm, tools=TOOLS, prompt=prompt)
    
    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8,
        max_execution_time=60,
    )
    
    return executor, session_id, memory

def run_agent(message: str, session_id: str = None) -> dict:
    """
    Run the agent with a user message.
    Returns dict with keys: response, session_id, tools_used
    """
    executor, session_id, memory = build_agent_executor(session_id)
    
    try:
        result = executor.invoke({"input": message})
        return {
            "response": result.get("output", "I couldn't generate a response."),
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
