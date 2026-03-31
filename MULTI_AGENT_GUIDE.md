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

### **Mode 1: Automatic (Recommended)**
Let coordinator decide which agent to use:

```bash
POST /chat
{
  "message": "Search for AI news",
  "use_multi_agent": true
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
You choose the specific agent:

```bash
POST /chat
{
  "message": "Show me code examples",
  "use_multi_agent": true,
  "agent_type": "code"
}

Response:
{
  "response": "Here's a code example...",
  "session_id": "abc123",
  "agent_used": "Code/Technical Agent",
  "success": true
}
```

### **Mode 3: Single Agent (Original)**
Use the original all-in-one agent:

```bash
POST /chat
{
  "message": "Tell me about AI",
  "use_multi_agent": false
}

Response:
{
  "response": "AI is...",
  "session_id": "abc123",
  "agent_used": "Single Agent",
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
  "single_agent": {...},
  "multi_agents": {
    "research": {...},
    "document": {...},
    "general": {...},
    "code": {...}
  },
  "usage": {...}
}
```

### Chat with Multi-Agent
```
POST /chat

Query Params:
- message (required): User message
- session_id (optional): Existing session
- use_multi_agent (optional, default: false): Enable multi-agent mode
- agent_type (optional): Force specific agent

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
┌─────────────────────────────────────┐
│         User Request                │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │ Use_multi?  │
        └──┬───────┬──┘
      false│       │true
           │       ├─────────────────────┐
           │       │ Agent_type given?  │
           │       └──┬──────────────┬──┘
           │          │no            │yes
           │          │         agent_type return
           │          │              │
           │    ┌─────▼──────────────┘
           │    │ Coordinator
           │    │ Determines Agent
           │    └──┬──────────────────┬─────────┬──────────┐
           │       │                  │         │          │
        ┌──▼─────────────┐      ┌──────┴──┐ ┌──┴─────┐ ┌──┴────┐
        │ Single Agent   │      │Research │ │Document│ │General┐
        │ (All Tools)    │      │ Agent   │ │ Agent  │ │ Agent │
        └────┬───────────┘      └────┬────┘ └───┬────┘ └───┬───┘
             │                       │          │        │
             │            ┌──────────┴──────────┘        │
             │            │                      ┌────────┘
             └────────────┬┘                      │
                    ┌─────▼──────────────────────▼───┐
                    │      Run Agent                  │
                    │  • Execute tools               │
                    │  • Maintain memory             │
                    │  • Generate response           │
                    └─────┬───────────────────────────┘
                          │
                    ┌─────▼──────────────┐
                    │ Return Response    │
                    │ + Agent Used       │
                    └────────────────────┘
```

---

## Performance Characteristics

| Agent | Speed | Accuracy | Tools | Best Use |
|-------|-------|----------|-------|----------|
| Research | Medium | High | 1 | Current info |
| Document | Fast | Very High | 2 | File analysis |
| General | Fast | High | 0 | Knowledge Q&A |
| Code | Medium | High | 1 | Programming |
| Single | Slow | Medium | 3 | Everything |

---

## Examples

### Example 1: Research Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the latest developments in generative AI?",
    "use_multi_agent": true
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
    "message": "Summarize the paper I uploaded",
    "use_multi_agent": true
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
    "use_multi_agent": true,
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
    "message": "Explain photosynthesis",
    "use_multi_agent": true
  }'

# Coordinator detects: general knowledge
# Routes to: General Q&A Agent
# Result: Clear explanation
```

---

## Configuration

### Toggle Between Modes in Frontend

Update `frontend/app.js`:

```javascript
// Use multi-agent
const useMultiAgent = true;

// Or specify agent
const agentType = "research"; // or "document", "general", "code"

// Send request
fetch("/chat", {
  method: "POST",
  body: JSON.stringify({
    message: userInput,
    use_multi_agent: useMultiAgent,
    agent_type: agentType
  })
});
```

### Adjust Agent Parameters

Edit `agents.py`:

```python
# Change temperature for specific agent
@dataclass
class ResearchConfig:
    temperature: float = 0.5  # More factual
    max_iterations: int = 6

# Change tools for agent
RESEARCH_TOOLS = [web_search]  # Add more if needed
```

---

## Switching Back to Single Agent

If you prefer the original single agent:

```bash
POST /chat
{
  "message": "Your message",
  "use_multi_agent": false
}
```

Or leave `use_multi_agent` unset (defaults to false).

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
├── agents.py                 ← Multi-agent system
├── agent.py                  ← Original single agent
├── server.py                 ← Updated with multi-agent endpoints
├── memory.py                 ← Shared session memory
└── tools/
    ├── search.py
    ├── doc_reader.py
    └── __init__.py
```

---

**Multi-Agent System v1.0** ✨  
4 Specialist Agents + Intelligent Coordinator
