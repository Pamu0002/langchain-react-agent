"""Base Agent class for multi-agent system"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from src.config import config
from src.memory import get_or_create_session
import re
import logging

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all specialist agents"""
    
    def __init__(self, name: str, system_prompt: str, tools: list = None):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.llm = ChatGroq(
            api_key=config.groq_api_key,
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
    
    def build_prompt(self):
        """Build prompt for this agent"""
        # Add tool descriptions to system prompt if tools available
        tools_info = ""
        if self.tools:
            tools_info = "\n\nAvailable Tools:\n"
            for tool in self.tools:
                tools_info += f"- {tool.name}: {tool.description}\n"
        
        return ChatPromptTemplate.from_messages([
            ("system", self.system_prompt + tools_info),
            ("user", "{input}")
        ])
    
    def execute_tool_call(self, tool_name: str, tool_input):
        """Execute a tool by name and return result"""
        # Handle different input formats
        if isinstance(tool_input, dict) and len(tool_input) == 1 and next(iter(tool_input.values())) == "":
            # If dict has one empty value, pass empty string
            actual_input = "" if "placeholder" in tool_input else next(iter(tool_input.values()))
        elif isinstance(tool_input, dict):
            # Extract the first argument value if it's a dict
            actual_input = next(iter(tool_input.values())) if tool_input else ""
        else:
            actual_input = tool_input
        
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    # Use func directly for Tool objects
                    if hasattr(tool, 'func'):
                        result = tool.func(actual_input)
                    else:
                        # Fallback for other tool types
                        result = tool.invoke({"input": actual_input})
                    return result
                except Exception as e:
                    logger.error(f"Tool {tool_name} error: {e}")
                    return f"Error calling {tool_name}: {str(e)}"
        
        return f"Tool {tool_name} not found"
    
    def run(self, message: str, session_id: str = None, **kwargs) -> dict:
        """Run this agent"""
        session_id, memory = get_or_create_session(session_id)
        
        logger.info(f"{self.name} processing: {message[:80]}")
        
        try:
            prompt = self.build_prompt()
            
            # Create simple chain without tool binding
            chain = prompt | self.llm
            
            # Invoke the agent
            result = chain.invoke({"input": message})
            response = result.content if hasattr(result, 'content') else str(result)
            
            # Store in memory
            memory.chat_memory.add_user_message(message)
            memory.chat_memory.add_ai_message(response)
            
            return {
                "response": response,
                "session_id": session_id,
                "agent_used": self.name,
                "success": True
            }
        except Exception as e:
            logger.error(f"{self.name} error: {e}", exc_info=True)
            error_msg = f"I encountered an error: {str(e)}. Please try again."
            
            # Try to store partial memory
            try:
                memory.chat_memory.add_user_message(message)
                memory.chat_memory.add_ai_message(error_msg)
            except:
                pass
            
            return {
                "response": error_msg,
                "session_id": session_id,
                "agent_used": self.name,
                "success": False
            }
