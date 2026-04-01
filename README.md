# ARIA — Agentic Research & Intelligence Assistant

> A powerful multi-agent AI system that intelligently routes queries to specialized agents, combining web search, document analysis, and reasoning capabilities into one unified interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 Overview

ARIA is a **self-hosted multi-agent AI assistant** built with LangChain, FastAPI, and Groq's LLM. It features:

- 🤖 **Multi-Agent System** — 4 specialized agents that route intelligently
- 🔍 **ResearchAgent** — Web search for current information  
- 📄 **DocumentAgent** — Analyzes PDFs, TXT, DOCX, Markdown files
- 💭 **GeneralAgent** — Knowledge-based reasoning without tools
- 💻 **CodeAgent** — Programming help and technical assistance
- 🧠 **Coordinator** — Smart routing to best agent
- 💬 **Session Memory** — Per-user conversation history
- ⚡ **Fast Responses** — Groq's optimized llama-3.3-70b
- 🎨 **Modern UI** — Vanilla HTML/CSS/JavaScript interface

### Use Cases

✅ Research with real-time web data  
✅ Analyze and understand documents  
✅ Get code examples and programming help  
✅ Maintain context across conversations  
✅ Run entirely locally with your own API keys  
✅ Extensible — Add new agents easily  

---

## 🏗️ Architecture

ARIA implements a **Hierarchical Multi-Agent Router Pattern** with intelligent request classification and specialized agent delegation:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         📱 FRONTEND LAYER                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Web UI (HTML5/CSS3/JavaScript) - Glassmorphic Design               │   │
│  │ • Real-time Chat Interface  • File Upload  • Session Management    │   │
│  │ • Theme Persistence         • Message History                      │   │
│  └────────────────────────┬─────────────────────────────────────────┬─┘   │
│                          │ HTTP/JSON                               │       │
└──────────────────────────┼───────────────────────────────────────┼────────┘
                           │                                       │
                           ▼                                       ▼
        ┌──────────────────────────────────────────────────────────────┐
        │              ⚙️ FASTAPI BACKEND LAYER                        │
        │  ┌────────────────────────────────────────────────────────┐  │
        │  │ API Routes: /chat, /upload, /clear (REST Endpoints) │  │
        │  │ CORS Enabled • Static File Serving • Error Handling  │  │
        │  └────────────┬─────────────────────────────────────────┘  │
        │               │                                             │
        │               ▼                                             │
        │  ┌────────────────────────────────────────────────────────┐  │
        │  │         🧠 REQUEST PROCESSING PIPELINE                │  │
        │  │                                                        │  │
        │  │  1. Parse Request & Extract Message                  │  │
        │  │  2. Load Session Context (if exists)                 │  │
        │  │  3. Build Prompt with History                        │  │
        │  │  4. Route to Coordinator                             │  │
        │  └────────────┬─────────────────────────────────────────┘  │
        │               │                                             │
        └───────────────┼─────────────────────────────────────────────┘
                        │
        ┌───────────────▼─────────────────────────────────────────────┐
        │          🎯 COORDINATOR (ROUTER AGENT)                      │
        │  ┌──────────────────────────────────────────────────────┐  │
        │  │ Intent Classification Engine                         │  │
        │  │ • Analyzes query semantics & keywords               │  │
        │  │ • Determines optimal agent match                    │  │
        │  │ • Confidence score calculation                      │  │
        │  │ • Fallback to multi-agent if ambiguous             │  │
        │  │ Uses: llama-3.3-70b via Groq API                  │  │
        │  └──┬────────┬──────────┬──────────┬──────────────────┘  │
        │     │        │          │          │                      │
        └─────┼────────┼──────────┼──────────┼──────────────────────┘
              │        │          │          │
        ┌─────▼───┬────▼───┬─────▼────┬────▼──────────────────────┐
        │          │        │          │                           │
        │ 🔍 Research │📄 Document│💭 General Q&A│💻 Code Agent│
        │ Agent    │ Agent  │ Agent   │ Agent       │
        │          │        │          │             │
    ┌───▼──────┐ ┌─▼─────┐ ┌──▼────┐ ┌──▼─────────┐│
    │ Web Search│ │PDF    │ │Knowledge│ │ Web Search ││
    │ Tool      │ │Reader │ │ Base    │ │ Tool       ││
    │ DuckDuckGo│ │ Tool  │ │ Reasoning │ │ Tool Chain ││
    ├────────────┤ ├────────┤ ├────────┤ ├────────────┤│
    │ Research   │ │Document│ │ General│ │ Code       ││
    │ Prompt     │ │Prompt  │ │Prompt  │ │ Prompt     ││
    └─────┬──────┘ └──┬────┘ └───┬────┘ └──┬─────────┘│
          │           │          │         │           │
          └───────────┼──────────┼─────────┘           │
                      │          │                      │
          ┌───────────▼──────────▼──────────────────────▼──┐
          │    🚀 LLM INFERENCE ENGINE                     │
          │  ┌─────────────────────────────────────────┐  │
          │  │ Groq API Client                         │  │
          │  │ Model: llama-3.3-70b-versatile         │  │
          │  │ Token Management • Rate Limiting        │  │
          │  │ Response Streaming • Error Handling     │  │
          │  └──────────┬────────────────────────────┘  │
          │             │                                │
          └─────────────┼────────────────────────────────┘
                        │
          ┌─────────────▼────────────────────────────────┐
          │    💾 RESPONSE AGGREGATION & STORAGE        │
          │  ┌──────────────────────────────────────┐  │
          │  │ Format Response JSON                 │  │
          │  │ Parse Agent Output                   │  │
          │  │ Store in Session Memory              │  │
          │  │ Compute Session ID                   │  │
          │  └──────────┬─────────────────────────┘  │
          │             │                             │
          └─────────────┼─────────────────────────────┘
                        │
        ┌───────────────▼──────────────────────────────┐
        │   📊 SESSION & MEMORY MANAGEMENT            │
        │  ┌────────────────────────────────────────┐ │
        │  │ In-Memory Session Store                │ │
        │  │ • Max 20 messages per session         │ │
        │  │ • Conversation history tracking       │ │
        │  │ • Session TTL management              │ │
        │  │ • Document context preservation       │ │
        │  └────────────────────────────────────────┘ │
        └────────────┬──────────────────────────────────┘
                     │
        ┌────────────▼──────────────────────────────────┐
        │    📁 FILE HANDLING SUBSYSTEM                 │
        │  ┌────────────────────────────────────────┐  │
        │  │ Document Processing Pipeline           │  │
        │  │ • PDF Extraction (PyPDF)              │  │
        │  │ • DOCX Parsing (python-docx)          │  │
        │  │ • Markdown Processing                 │  │
        │  │ • Text File Reading                   │  │
        │  │ • File Size Validation (10MB limit)   │  │
        │  │ • MIME Type Checking                  │  │
        │  └────────────────────────────────────────┘  │
        └───────────────────────────────────────────────┘
```

### 🔄 Request Flow Sequence

```
1. USER MESSAGE INPUT
   └─→ Frontend captures message + optional file
       └─→ HTTP POST to /chat endpoint

2. REQUEST VALIDATION
   └─→ Parse JSON payload
       └─→ Validate message length
           └─→ Check file size/type (if upload)

3. SESSION CONTEXT LOADING
   └─→ Retrieve session by ID (or create new)
       └─→ Load conversation history (last 20 msgs)
           └─→ Prepare context window

4. COORDINATOR ANALYSIS
   └─→ Coordinator LLM analyzes query intent
       ├─→ Check if research query
       ├─→ Check if code-related
       ├─→ Check if document analysis
       └─→ Default to general Q&A

5. AGENT EXECUTION
   └─→ Selected agent initializes
       ├─→ Set system prompt (role-specific)
       ├─→ Add tools (if applicable)
       ├─→ Prepare context window
       └─→ Invoke LLM with prompt

6. LLM INFERENCE
   └─→ Groq API receives request
       └─→ llama-3.3-70b processes
           └─→ Streams or returns response
               └─→ Token counting + tracking

7. RESPONSE PROCESSING
   └─→ Parse LLM output
       ├─→ Extract text content
       ├─→ Identify agent used
       └─→ Format as JSON response

8. SESSION STORAGE
   └─→ Add user message to history
       └─→ Add assistant response to history
           └─→ Update session metadata
               └─→ Return response to frontend

9. FRONTEND RENDERING
   └─→ Receive JSON response
       ├─→ Display user message (immediate)
       ├─→ Show typing indicator
       ├─→ Display agent response (animated)
       └─→ Update session display
```

### 🎯 Why This Architecture?

| Aspect | Benefit |
|--------|---------|
| **Agents** | Specialized handling per domain → Better accuracy |
| **Coordinator** | Intelligent routing → Optimal resource use |
| **Session Memory** | Conversation persistence → Context awareness |
| **Tool System** | Pluggable tools → Extensibility |
| **Async Processing** | Non-blocking → Better UX |
| **Error Isolation** | Agent failures don't crash system → Reliability |
| **LLM Router** | AI-powered routing → Flexibility |
| **Modular Design** | Add agents without code changes → Maintainability |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **LLM** | llama-3.3-70b (via Groq) |
| **Framework** | LangChain 1.x |
| **Backend API** | FastAPI + Uvicorn |
| **Frontend** | Vanilla HTML/CSS/JS |
| **Memory** | In-memory session storage |
| **Web Search** | Tavily API + DuckDuckGo fallback |
| **Document Processing** | PyPDF, python-docx, BeautifulSoup4 |
| **Python** | 3.10+ (tested on 3.13.7) |

---

## 📋 Prerequisites

- **Python 3.10+** (tested on 3.13.7)
- **Groq API Key** (free) → https://console.groq.com
- **Tavily API Key** (optional, free) → https://tavily.com
- **Git** for cloning the repository
- **Internet connection** (for APIs and web search)

---

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/Pamu0002/langchain-react-agent.git
cd langchain-react-agent
```

### 2. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows (CMD)
python -m venv venv
.\venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your keys:
# GROQ_API_KEY=gsk_xxxxxxxxxxxxxxx
# TAVILY_API_KEY=tvly-dev-xxxxxxxxxxxx
```

**Get API keys:**
- **Groq** (required, free): https://console.groq.com/keys
- **Tavily** (optional, free): https://tavily.com/api

### 5. Start the Server
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn src.api:app --reload --port 8000
```

### 6. Open in Browser
Navigate to: **http://localhost:8000**

---

## 📁 Project Structure

```
src/
├── __init__.py              # Package marker
├── config.py                # Centralized configuration
│
├── api/
│   ├── __init__.py          # FastAPI app factory
│   ├── routes.py            # API endpoints
│   └── models.py            # Pydantic request/response models
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
│   ├── search.py            # Web search tool
│   └── doc_reader.py        # Document reader
│
├── memory/
│   └── __init__.py          # Session memory management
│
└── frontend/
    ├── index.html           # Chat UI
    └── app.js               # Frontend logic

main.py                       # Entry point
pyproject.toml               # Python package config
requirements.txt             # Dependencies
.env.example                 # Example environment file
tests/                       # Test suite
docs/                        # Documentation
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# Required
GROQ_API_KEY=gsk_your_key_here

# Optional but recommended
TAVILY_API_KEY=tvly-dev-your_key_here

# Optional - for debugging
DEBUG=false
```

### Settings (`src/config.py`)

All settings are centralized in `src/config.py`. Key configurations:
- **Model**: llama-3.3-70b-versatile
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 2048
- **Max History**: 20 messages per session
- **Max File Size**: 10MB
- **Allowed Extensions**: .pdf, .txt, .docx, .md

---

## 💬 Usage

### Via Web UI
1. Open **http://localhost:8000** in your browser
2. Type a message and press Send
3. ARIA routes to the best agent and responds
4. Upload files with the "+file" button
5. Clear chat with "clear chat" button

### Via API

**Health Check**
```bash
curl http://localhost:8000/health
```

**List Agents**
```bash
curl http://localhost:8000/agents
```

**Send Message (Auto-Routing)**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Search for latest AI news"}'
```

**Send Message (Specific Agent)**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Your query",
    "use_multi_agent": true,
    "agent_type": "research"
  }'
```

Agent types: `research`, `document`, `general`, `code`

**Upload Document**
```bash
curl -X POST http://localhost:8000/upload -F "file=@document.pdf"
```

**Get History**
```bash
curl http://localhost:8000/history/session_id_here
```

**Clear Memory**
```bash
curl -X POST http://localhost:8000/clear \
  -H "Content-Type: application/json" \
  -d '{"session_id": "session_id_here"}'
```

---

## 🤖 The 4 Agents

### ResearchAgent 🔍
- **Purpose**: Web search and current information
- **Specialization**: Finding latest news, trends, pricing, facts
- **Tools**: Web search, reasoning
- **Example**: "What's trending on GitHub today?"

### DocumentAgent 📄
- **Purpose**: File analysis and understanding
- **Specialization**: Summarizing, analyzing, extracting info from files
- **Tools**: Document reader, file listing
- **Example**: "Summarize the key points from this PDF"

### GeneralAgent 💭
- **Purpose**: Knowledge and reasoning
- **Specialization**: Explanations, concepts, comparisons
- **Tools**: None (pure reasoning)
- **Example**: "Explain quantum entanglement"

### CodeAgent 💻
- **Purpose**: Programming and technical help
- **Specialization**: Debug code, explain libraries, best practices
- **Tools**: Web search, reasoning
- **Example**: "How do I use async/await in Python?"

### Coordinator 🎯
- **Purpose**: Smart routing
- **Role**: Analyzes incoming message and routes to best agent
- **Logic**: LLM-based intent analysis
- **Fallback**: Multi-agent system as fallback

---

## 📡 API Reference

### GET /health
Returns server status

### GET /agents
Lists all agents and capabilities

### POST /chat
Main chat endpoint with auto or manual routing

### POST /upload
Upload document file

### POST /clear
Clear session memory

### GET /history/{session_id}
Get conversation history

---

## 📊 Session Management

Each user gets a unique **session ID**:
- Stores up to 20 conversation messages
- Isolated per user
- Can be cleared individually
- Enables context across multiple requests

---

## 🧪 Testing

```bash
pip install pytest pytest-asyncio
pytest tests/
pytest -v tests/
```

---

## 📈 Performance

- **Response Time**: 1-5 seconds per query
- **Memory Usage**: ~200-300MB + session context
- **File Size**: Up to 10MB per upload
- **Concurrent Users**: Limited by API rate limits

---

## 🔒 Security Notes

⚠️ **Important**:
- `.env` file contains API keys — **never commit to git**
- Use `.env.example` as template
- Consider rate limiting in production
- Run behind reverse proxy (nginx) for HTTPS

---

## ⚠️ Troubleshooting

**Server won't start**
```bash
python --version  # Should be 3.10+
```

**API key errors**
- Verify `.env` file exists and has keys

**Documents won't upload**
- Check file size < 10MB
- Check file extension is allowed

**Slow responses**
- Check Groq API status
- Verify internet connection

---

## 🚀 Future Enhancements

- [ ] Streaming responses with Server-Sent Events
- [ ] Persistent storage (SQLite/PostgreSQL)
- [ ] Advanced RAG (Retrieval-Augmented Generation)
- [ ] User authentication and multi-user support
- [ ] Voice input/output capabilities
- [ ] Support for more LLM providers
- [ ] Dashboard and analytics

---

## 📚 Documentation

See [docs/](docs/) folder for detailed guides:
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — System design
- [MULTI_AGENT_GUIDE.md](docs/MULTI_AGENT_GUIDE.md) — Multi-agent details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License — see LICENSE file for details

---

## 🙏 Acknowledgments

- **LangChain** — Agent framework
- **FastAPI** — Web framework
- **Groq** — LLM inference
- **Tavily** — Web search API

---

## 📞 Support

Questions or issues?
- Check existing GitHub issues
- Review docs/ folder
- Create a new issue with details

---

## 🔗 Links

- **Repository**: https://github.com/Pamu0002/langchain-react-agent
- **LangChain**: https://python.langchain.com
- **FastAPI**: https://fastapi.tiangolo.com
- **Groq**: https://console.groq.com

---

**Enjoy using ARIA! 🚀**
