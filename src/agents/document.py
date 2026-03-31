from src.agents.base import BaseAgent
from src.tools.doc_reader import _read_document_impl, _list_documents_impl
from src.config import config
import os
import logging

logger = logging.getLogger(__name__)

DOCUMENT_PROMPT = """You are ARIA's Document Analysis Agent, specialized in reading and understanding documents.

Your expertise:
- Analyze PDF, TXT, DOCX, and Markdown files
- Provide accurate summaries
- Answer questions about document content  
- Extract key information
- Compare documents

When analyzing documents provided to you:
1. Read the content carefully
2. Provide a clear, concise summary or answer based on what you've read
3. Quote relevant passages when appropriate
4. Maintain accuracy when referencing documents

Always provide thoughtful, accurate analysis.
"""

class DocumentAgent(BaseAgent):
    """Document Agent - specialized in file analysis and document understanding"""
    
    def __init__(self):
        super().__init__(
            name="Document Agent",
            system_prompt=DOCUMENT_PROMPT,
            tools=[]
        )
    
    def run(self, message: str, session_id: str = None, **kwargs) -> dict:
        """Run document agent with auto-loaded document content."""
        from src.memory import get_or_create_session
        
        session_id, memory = get_or_create_session(session_id)
        
        logger.info(f"{self.name} processing: {message[:80]}")
        
        try:
            # Build enhanced message with document context
            enhanced_message = message
            
            # If user asks to summarize/analyze and documents exist, auto-load them
            if ("summarize" in message.lower() or "analyze" in message.lower() or 
                "read" in message.lower() or "what" in message.lower() or 
                "tell" in message.lower()) and os.path.exists(config.upload_dir):
                
                # List all available documents
                files = [f for f in os.listdir(config.upload_dir) 
                        if os.path.splitext(f)[1].lower() in config.allowed_extensions]
                
                if files:
                    doc_content_parts = []
                    
                    # Load first document
                    for filename in files[:1]:
                        try:
                            content = _read_document_impl(filename)
                            doc_content_parts.append(f"Document '{filename}':\n{content}")
                            logger.info(f"Loaded document: {filename}")
                        except Exception as e:
                            logger.error(f"Error loading {filename}: {e}")
                    
                    if doc_content_parts:
                        enhanced_message = (
                            f"{message}\n\n" +
                            "DOCUMENT CONTENT:\n---\n" +
                            "\n---\n".join(doc_content_parts) +
                            "\n---\n\nPlease analyze the above document and respond to the user's request."
                        )
            
            # Invoke the LLM
            prompt = self.build_prompt()
            chain = prompt | self.llm
            result = chain.invoke({"input": enhanced_message})
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
