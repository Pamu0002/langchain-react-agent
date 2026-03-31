# ARIA Architecture

## Overview

ARIA (Agentic Research & Intelligence Assistant) is a multi-agent AI system powered by LangChain and Groq's LLM. It uses a coordinator pattern to intelligently route user queries to specialized agents.

## System Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (HTML/JS) - Browser UI        │
└────────────────┬────────────────────────┘
                 │ HTTP/JSON
┌────────────────▼────────────────────────┐
│  FastAPI Server (main.py)               │
│  - Endpoints: /chat, /upload, /health   │
└────────────────┬────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
    ┌────▼────────┐  ┌───▼──────────────┐
    │ Single      │  │ Multi-Agent      │
    │ Agent Mode  │  │ System + Router  │
    └─────────────┘  └──────┬───────────┘
                            │
         ┌──────┬───────┬──┴──┬──────┐
         │      │       │     │      │
    ┌────▼──┐ ┌─▼────┐ ┌─▼───┐ ┌──▼────┐ ┌────────┐
    │Research│ │Doc   │ │Gen. │ │ Code  │ │Coord   │
    │ Agent  │ │Agent │ │Q&A  │ │ Agent │ │(Router)│
    └────────┘ └──────┘ └─────┘ └───────┘ └────────┘
         │        │        │         │
    ┌────┴────┬───┴────┬──┴────┬────┴────┐
    │ Web     │ File   │ LLM   │ Math    │
    │ Search  │ Reader │ Only  │ Tools   │
    └─────────┴────────┴───────┴─────────┘
```

## Directory Structure

```
src/
├── __init__.py              # Package marker
├── agent.py                 # Original single agent (backward compatible)
├── config.py                # Configuration management
│
├── api/
│   ├── __init__.py          # FastAPI app factory
│   ├── routes.py            # API endpoints
│   └── models.py            # Pydantic models
│
├── agents/
│   ├── __init__.py          # Agent registry & multi_agent()
│   ├── base.py              # BaseAgent class
│   ├── research.py          # ResearchAgent
│   ├── document.py          # DocumentAgent
│   ├── general.py           # GeneralAgent
│   ├── code.py              # CodeAgent
│   └── coordinator.py       # Coordinator (router)
│
├── tools/
│   ├── __init__.py          # Tool exports
│   ├── search.py            # Web search tool (Tavily)
│   └── doc_reader.py        # Document reading tools
│
├── memory/
│   ├── __init__.py          # Memory functions
│   └── storage.py           # Session storage
│
└── frontend/
    ├── index.html           # UI
    └── app.js               # Frontend JavaScript
```

## Core Components

### 1. Configuration (`src/config.py`)
- Centralized settings management
- API keys (Groq, Tavily)
- Model parameters (temperature, max_tokens)
- File handling (upload directory, allowed extensions)

### 2. Memory System (`src/memory/`)
- **Purpose**: Maintain conversation context
- **Implementation**: 
  - Per-session storage using UUID
  - Stores up to 20 messages per session
  - Memory window for ReAct agent reasoning
  - Auto-cleanup of old sessions

### 3. Tools (`src/tools/`)
- **web_search**: Tavily API with DuckDuckGo fallback
- **read_document**: PDF, TXT, DOCX, MD support
- **list_documents**: Show uploaded files

### 4. Agent System (`src/agents/`)

#### BaseAgent Class
- Shared initialization and execution logic
- Methods:
  - `build_prompt()` - Create agent prompt
  - `build_executor()` - Setup ReAct executor
  - `run(message, session_id)` - Execute query

#### Specialized Agents
- **ResearchAgent**: Web search + reasoning
- **DocumentAgent**: File analysis
- **GeneralAgent**: Knowledge Q&A (no tools)
- **CodeAgent**: Programming help

#### Coordinator
- Analyzes user query to determine best agent
- Routes to appropriate specialist
- Falls back to multi-agent if needed

### 5. API (`src/api/`)

**Endpoints:**
- `GET /health` - Server status
- `GET /agents` - List agents & capabilities
- `POST /chat` - Main chat endpoint
- `POST /upload` - File upload
- `POST /clear` - Clear session memory
- `GET /history/{session_id}` - Get conversation history

**Models:**
- ChatRequest/ChatResponse
- HealthResponse
- AgentListResponse

### 6. Frontend (`src/frontend/`)
- React-style vanilla JavaScript UI
- Real-time message streaming
- File upload with progress
- Session persistence
- Markdown rendering support

## Message Flow

### Single Agent Mode
```
User Query → API → agent.py → LLM + Tools → Response → API → Frontend
```

### Multi-Agent Mode (With Router)
```
User Query
    ↓
Coordinator analyzes query
    ↓
Determines best agent
    ↓
Routes to ResearchAgent OR DocumentAgent OR GeneralAgent OR CodeAgent
    ↓
Agent builds prompt + executor
    ↓
LLM + Tools (if needed)
    ↓
Response → API → Frontend
```

## LLM Configuration

- **Model**: `llama-3.3-70b-versatile` (Groq)
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Max Tokens**: 2048
- **Tool Use**: Enabled via LangChain ReAct pattern

## Key Design Patterns

1. **Inheritance**: BaseAgent with specialized subclasses
2. **Router Pattern**: Coordinator for intelligent agent selection
3. **Dependency Injection**: Config passed to components
4. **Session-based State**: Isolated per-user memory
5. **Async API**: FastAPI for concurrent request handling

## Deployment

- **Development**: `python main.py` (uvicorn default)
- **Production**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Frontend**: Static files served from `src/frontend/`

## Error Handling

- Try-catch in agent execution
- Graceful LLM fallbacks
- User-friendly error messages
- Logging for debugging

## Future Enhancements

- Machine learning-based routing
- New specialized agents (math, writing, etc.)
- Streaming responses
- Multi-turn conversation improvements
- Agent performance metrics
