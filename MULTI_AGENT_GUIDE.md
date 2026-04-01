# Multi-Agent System Guide

## Overview

ARIA now supports **4 Specialized Agents** plus a **Coordinator Agent** for intelligent routing.

---

## The 4 Specialized Agents

### **1. Research Agent** 🔍
**Specialization:** Web search and real-time information  
**Tools:** web_search  
**Best for:**
- "Search for AI news today"
- "What's trending?"
- "Find information about..."
- Latest developments and current events

**Example:**
```
User: "Tell me about the latest AI breakthroughs"
→ Coordinator routes to Research Agent
→ Research Agent searches web
→ Returns current information with sources
```

---

### **2. Document Agent** 📄
**Specialization:** Document analysis and file management  
**Tools:** read_document, list_documents  
**Best for:**
- "Summarize this PDF"
- "What files do I have?"
- Extracting information from documents
- Comparing multiple documents

**Example:**
```
User: "What's in my research paper?"
→ Coordinator routes to Document Agent
→ Document Agent reads file
→ Returns detailed summary
```

---

### **3. General Q&A Agent** 💡
**Specialization:** Knowledge and reasoning  
**Tools:** None (pure knowledge)  
**Best for:**
- "Explain quantum computing"
- "How does photosynthesis work?"
- General knowledge questions
- Conceptual explanations

**Example:**
```
User: "What is machine learning?"
→ Coordinator routes to General Q&A Agent
→ Agent uses knowledge to explain
→ Returns clear, structured explanation
```

---

### **4. Code/Technical Agent** 💻
**Specialization:** Programming and technical topics  
**Tools:** web_search (for latest docs/libraries)  
**Best for:**
- "How do I use React hooks?"
- "Debug this Python code"
- Framework/library help
- Code examples and best practices

**Example:**
```
User: "Show me how to create a REST API in FastAPI"
→ Coordinator routes to Code/Technical Agent
→ Agent provides code examples
→ Returns best practices and explanations
```

---

## How to Use

### **Mode 1: Automatic Routing (Recommended)**
Let coordinator decide which agent to use:

```bash
POST /chat
{
  "message": "Search for AI news",
  "session_id": "optional-session-id"
}

Response:
{
  "response": "Here's what I found...",
  "session_id": "abc123",
  "agent_used": "Research Agent",
  "success": true
}
```

### **Mode 2: Manual Agent Selection**
You choose the specific agent to use:

```bash
POST /chat
{
  "message": "Show me code examples",
  "agent_type": "code",
  "session_id": "optional-session-id"
}

Response:
{
  "response": "Here's a code example...",
  "session_id": "abc123",
  "agent_used": "Code/Technical Agent",
  "success": true
}
```

---

## API Endpoints

### Check Available Agents
```
GET /agents

Response:
{
  "system": "Multi-Agent with Intelligent Coordinator",
  "agents": {
    "research": {...},
    "document": {...},
    "general": {...},
    "code": {...}
  },
  "routing": {...}
}
```

### Chat with Multi-Agent
```
POST /chat

Parameters:
- message (required): User message
- session_id (optional): Existing session ID
- agent_type (optional): Specify agent ('research', 'document', 'general', 'code') or None for auto-routing

Response:
- response: Agent's response
- session_id: Session ID  
- agent_used: Which agent handled it
- success: Was it successful?
```

---

## Coordinator Logic

The **Coordinator Agent** analyzes user queries and automatically routes to the best specialist:

```python
def determine_agent(user_message: str) -> str:
    """
    Analyzes the message and returns:
    - 'research' if asking for current info
    - 'document' if referencing files
    - 'code' if asking about programming
    - 'general' as default
    """
```

**Routing Heuristics:**
```
"search" → Research Agent
"news" → Research Agent
"file", "pdf", "document" → Document Agent
"code", "python", "javascript" → Code Agent
"explain", "how" → General Agent (or specific agent)
```

---

## Architecture

```
┌──────────────────────────────────────────┐
│         User Request                     │
└────────────────┬─────────────────────────┘
                 │
          ┌──────▼──────────┐
          │  Agent Specified?│
          └──┬────────────┬──┘
             │no          │yes
             │         agent_type
             │              │
    ┌────────▼──────────────┘
    │  Coordinator
    │  Analyzes Intent
    │  Routes to Best Agent
    └────┬──────────────────┬──────────┬──────────┐
         │                  │          │          │
    ┌────▼────┐        ┌────▼────┐ ┌──▼────┐ ┌──▼────┐
    │Research │        │Document │ │General│ │Code   │
    │ Agent   │        │ Agent   │ │ Agent │ │ Agent │
    └────┬────┘        └────┬────┘ └───┬───┘ └───┬───┘
         │                  │          │         │
         └──────────┬───────┴──────────┴─────────┘
                    │
             ┌──────▼──────────────┐
             │   Run Agent         │
             │ • Execute tools     │
             │ • Maintain memory   │
             │ • Generate response │
             └──────┬──────────────┘
                    │
             ┌──────▼──────────────┐
             │ Return Response     │
             │ + Agent Used        │
             └─────────────────────┘
```

---

## Performance Characteristics

| Agent | Speed | Accuracy | Tools | Best Use |
|-------|-------|----------|-------|----------|
| Research | Medium | High | 1 | Current info |
| Document | Fast | Very High | 2 | File analysis |
| General | Fast | High | 0 | Knowledge Q&A |
| Code | Medium | High | 1 | Programming |
| Coordinator | Fast | Very High | 0 | Routing |

---

## Examples

### Example 1: Research Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the latest developments in generative AI?"
  }'

# Coordinator detects: research query
# Routes to: Research Agent
# Result: Latest AI news with sources
```

### Example 2: Document Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Summarize the paper I uploaded"
  }'

# Coordinator detects: document reference
# Routes to: Document Agent
# Result: Detailed summary of paper
```

### Example 3: Code Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I implement JWT authentication in Python?",
    "agent_type": "code"
  }'

# Manual routing to: Code/Technical Agent
# Result: Code example + explanation
```

### Example 4: General Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain photosynthesis"
  }'

# Coordinator detects: general knowledge
# Routes to: General Q&A Agent
# Result: Clear explanation
```

---

## Configuration

### Toggle Between Auto and Manual Routing in Frontend

Update `frontend/app.js`:

```javascript
// Auto-routing (let coordinator decide)
const agentType = null;

// Or specify agent directly
const agentType = "research"; // "research", "document", "general", "code"

// Send request
fetch("/chat", {
  method: "POST",
  body: JSON.stringify({
    message: userInput,
    agent_type: agentType
  })
});
```

### Adjust Agent Parameters

Edit `agents.py` or `coordinator.py`:

```python
# Change temperature for specific agent
RESEARCH_PROMPT = """Your specialized prompt here"""

# Change tools for agent
RESEARCH_TOOLS = [web_search]

# Change coordinator temperature for routing precision
coordinator_llm = ChatGroq(
    temperature=0.3,  # Lower = more precise routing
    max_tokens=50
)
```

---

## Troubleshooting

### Agent Not Routing Correctly
- Check coordinator logs in server output
- Try manual `agent_type` specification
- Verify agent tools are working

### Slow Response
- Reduce `max_iterations` in agent config
- Use faster model version
- Check API rate limits

### Agent Missing Tools
- Verify tools are in `agents.py`
- Check tool names match exactly
- Ensure tool functions have `@tool` decorator

---

## Future Enhancements

- [ ] Custom agent creation interface
- [ ] Agent performance metrics
- [ ] RAG-enhanced agents
- [ ] Streaming responses per agent
- [ ] Agent feedback loop for improvements
- [ ] Multi-agent collaboration

---

## File Structure

```
agents/
├── __init__.py               ← Multi-agent system entry point
├── base.py                   ← BaseAgent class
├── coordinator.py            ← Coordinator router
├── research.py               ← Research Agent
├── document.py               ← Document Agent
├── general.py                ← General Q&A Agent
├── code.py                   ← Code/Technical Agent
├── memory.py                 ← Shared session memory
└── tools/
    ├── search.py
    ├── doc_reader.py
    └── __init__.py
```

---

**Multi-Agent System v2.0** ✨  
Consolidated: 4 Specialist Agents + Intelligent Coordinator
