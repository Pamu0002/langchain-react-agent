# ARIA — Agentic Research & Intelligence Assistant

> A personal AI assistant web application that combines reasoning, web search, and document understanding in a single interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## Overview

ARIA is a **self-hosted AI assistant** built with LangChain and FastAPI. It provides:

- 💬 **Conversational AI** — Replies intelligently using llama-3.3-70b via Groq
- 🌐 **Web Search** — Real-time information retrieval via Tavily + DuckDuckGo
- 📄 **Document Analysis** — Read and answer questions about PDF, TXT, DOCX files
- 💾 **Session Memory** — Maintains conversation history within a session
- ⚡ **Fast Responses** — Groq's optimized LLM for quick inference
- 🎨 **Clean UI** — Vanilla HTML/CSS/JavaScript frontend (no frameworks)

### Use Cases

✅ Research topics with real-time web data  
✅ Understand your documents faster  
✅ Maintain context across a conversation  
✅ Run entirely locally with your own API keys  
✅ No data sent to external servers (except APIs you control)

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **LLM** | llama-3.3-70b (via Groq) |
| **Agent Framework** | LangChain ReAct |
| **Backend** | FastAPI + Uvicorn |
| **Frontend** | Vanilla HTML/CSS/JS |
| **Memory** | In-memory conversation buffer |
| **Search** | Tavily API + DuckDuckGo fallback |
| **Document Processing** | PyPDF, python-docx, TextLoader |

---

## Prerequisites

- **Python 3.10+** (tested on 3.13.7)
- **Groq API Key** (free) — https://console.groq.com
- **Tavily API Key** (optional, free) — https://tavily.com
- **Internet connection** (for web search and LLM calls)

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Pamu0002/langchain-react-agent.git
cd langchain-react-agent
```

### 2. Create Virtual Environment
```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows CMD
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
# GROQ_API_KEY=your_groq_key_here
# TAVILY_API_KEY=your_tavily_key_here
```

**Where to get API keys:**
- **Groq** (required, free tier available): https://console.groq.com/keys
- **Tavily** (optional, free tier available): https://tavily.com/api-keys
- **LangSmith** (optional, for tracing): https://smith.langchain.com

### 5. Start the Server
```bash
python server.py
```

or with uvicorn directly:
```bash
uvicorn server:app --reload --port 8000
```

### 6. Open in Browser
Navigate to: **http://localhost:8000**

---

## Project Structure

```
langchain-react-agent/
├── README.md                    ← You are here
├── requirements.txt             ← Python dependencies
├── .env                         ← API keys (never commit)
├── .env.example                 ← Template for .env
│
├── config.py                    ← Centralized configuration
├── server.py                    ← FastAPI application (entry point)
├── agent.py                     ← LangChain ReAct agent logic
├── memory.py                    ← Session conversation memory
│
├── tools/
│   ├── __init__.py
│   ├── search.py                ← Web search tool (Tavily + DuckDuckGo)
│   └── doc_reader.py            ← Document reader tool (PDF/TXT/DOCX)
│
├── uploads/                     ← User-uploaded files (gitignored)
│   └── (created automatically)
│
└── frontend/
    ├── index.html               ← Chat UI
    └── app.js                   ← JavaScript logic (fetch, SSE, UI)
```

---

## Configuration

### Environment Variables (`.env`)

```bash
# Required
GROQ_API_KEY=gsk_xxxxxxx...

# Optional but recommended
TAVILY_API_KEY=tvly-dev-xxx...

# Optional - for LangChain tracing
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
```

### Settings (`config.py`)

Customize these without restarting:

```python
@dataclass
class AgentConfig:
    # LLM
    model_name: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 2048

    # Files
    max_file_size_mb: int = 10
    allowed_extensions: tuple = (".pdf", ".txt", ".docx", ".md")

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
```

---

## Usage

### 1. Send a Message
```javascript
// Browser console or UI
POST /chat
{
  "message": "What can you do?",
  "session_id": "optional_session_id"
}
```

### 2. Upload a Document
```javascript
POST /upload (multipart/form-data)
file: <PDF, TXT, or DOCX file>
```

### 3. Clear Chat History
```javascript
POST /clear
{
  "session_id": "abc123"
}
```

---

## API Reference

### Health Check
```
GET /health
Response: {"status": "ok", "version": "1.0.0", "model": "llama-3.3-70b-versatile"}
```

### Chat Endpoint
```
POST /chat

Request:
{
  "message": "Search for AI news",
  "session_id": "abc123"  // optional - generates new if omitted
}

Response:
{
  "response": "I found several AI news stories...",
  "session_id": "abc123",
  "success": true
}
```

### Upload Endpoint
```
POST /upload

Request: multipart/form-data with file

Response:
{
  "filename": "report.pdf",
  "size_mb": 2.5,
  "message": "'report.pdf' uploaded successfully. You can now ask ARIA about it."
}
```

### Clear Memory
```
POST /clear

Request:
{
  "session_id": "abc123"
}

Response:
{
  "cleared": true,
  "session_id": "abc123"
}
```

### Get History
```
GET /history/{session_id}

Response:
{
  "session_id": "abc123",
  "history": "User: Hello\nARIA: Hi there!\nUser: How are you?\nARIA: I'm doing great!"
}
```

---

## Features

### ✅ Implemented

- [x] ReAct agent with tool selection
- [x] Web search (Tavily + DuckDuckGo fallback)
- [x] Document reading (PDF, TXT, DOCX, Markdown)
- [x] Session-based conversation memory
- [x] File upload and storage
- [x] FastAPI with CORS support
- [x] Clean, responsive UI
- [x] Error handling and logging
- [x] Graceful fallback for API failures

### 🚀 Future Enhancements

- [ ] **Streaming Responses** — SSE for token-by-token streaming
- [ ] **Persistent Storage** — SQLite for conversation history
- [ ] **RAG (Retrieval-Augmented Generation)** — Better document understanding
- [ ] **User Authentication** — Multi-user support with login
- [ ] **Voice Input** — Speech-to-text via Web Speech API
- [ ] **Multiple LLMs** — Support for OpenAI, Anthropic, Ollama
- [ ] **Scheduled Tasks** — Cron job-based assistant tasks
- [ ] **Docker Deployment** — Container for easy deployment
- [ ] **Analytics** — Track usage and performance

---

## Architecture

### ReAct Agent Pattern

ARIA uses the **ReAct (Reasoning + Acting)** pattern:

1. **Reason** — Think about the user's request
2. **Act** — Choose and execute a tool (or answer directly)
3. **Observe** — Get tool results
4. **Repeat** — Iterate until response is ready

```
User Input
    ↓
[Agent Thinks]
    ↓
[Choose Tool: search? read_document? answer?]
    ↓
[Execute Tool]
    ↓
[Observe Results]
    ↓
[Generate Response]
    ↓
User Output
```

### Memory Management

- Each user gets a unique **session_id**
- Stores up to **20 messages** (configurable)
- Oldest messages discarded to prevent token overflow
- Memory cleared when user clicks "clear chat"

### Tool Selection

The agent automatically decides which tool to use:

| User Input | Tools Used |
|------------|-----------|
| "What's new in AI?" | web_search |
| "Summarize my PDF" | read_document |
| "What files do I have?" | list_documents |
| "Hi, how are you?" | None (direct answer) |

---

## Testing Checklist

After installation, verify all features work:

- [ ] Server starts without errors: `python server.py`
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] UI loads at http://localhost:8000
- [ ] Send a simple message: "Hello"
- [ ] Web search works: "Search for AI news"
- [ ] Upload a PDF and ask about it
- [ ] List documents works: "What files do I have?"
- [ ] Clear chat history resets memory
- [ ] Session ID persists across messages
- [ ] Errors handled gracefully (try invalid file type)

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'X'"
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: "Server starts but UI doesn't load"
```
1. Check browser console (F12)
2. Verify /static/app.js is loading
3. Hard refresh (Ctrl+F5)
4. Check server logs for 404 errors
```

### Issue: "Chat doesn't work, API returns 400"
```
1. Verify GROQ_API_KEY is set in .env
2. Check server logs for specific error
3. Ensure message is not empty
4. Try /health endpoint first
```

### Issue: "Web search returns no results"
```
1. Check TAVILY_API_KEY in .env
2. DuckDuckGo fallback should still work
3. Try a different search query
4. Check API rate limits
```

### Issue: "Document upload fails"
```
1. File must be .pdf, .txt, .docx, or .md
2. File size must be < 10MB (default)
3. Check uploads/ folder has write permissions
4. Try a different file
```

### Issue: "Agent keeps timing out"
```
1. Reduce max_tokens in config.py (default 2048)
2. Check internet connection for web_search
3. Try simpler queries first
4. Check Groq API status
```

---

## Logging

Server logs include:
- Chat requests and responses
- File uploads
- Tool executions (search, document reads)
- Agent decisions and reasoning
- Errors and warnings

View logs in terminal while server is running.

---

## Industry Standards & Best Practices

### ✅ This Project Follows:

**1. Project Structure**
- Modular organization (tools/, frontend/ separation)
- Single entry point (server.py)
- Clear configuration (config.py)
- Environment variable management (.env)

**2. Code Quality**
- Type hints in Python (used in request models)
- Docstrings on all tools
- Error handling with try/except
- Logging for debugging

**3. API Design**
- RESTful endpoints (GET, POST, PUT semantics)
- JSON request/response format
- HTTP status codes (200, 400, 404, 500)
- CORS support for cross-origin requests

**4. Security**
- API keys via environment variables (never hardcoded)
- File upload validation (type and size checks)
- Input validation (empty message checks)
- Session isolation (per-user memory)

**5. Frontend**
- Responsive design (works on mobile)
- Progressive enhancement (works without JS disabled)
- Accessibility basics (semantic HTML)
- User feedback (loading states, error messages)

**6. DevOps**
- requirements.txt for dependency management
- Virtual environment support
- .env/.env.example pattern
- Graceful server startup

---

## Performance Considerations

| Aspect | Value | Notes |
|--------|-------|-------|
| Max file size | 10 MB | Configurable in config.py |
| Memory limit | 20 messages | Prevents token overflow |
| LLM timeout | 60 seconds | Max execution time |
| Agent iterations | 8 max | Prevents infinite loops |
| Response time | ~1-3 sec | Depends on query complexity |

---

## Security Notes

⚠️ **Important:**
- **Never commit `.env`** file with real API keys
- Run on **localhost only** for personal use
- If deploying publicly:
  - Add user authentication
  - Use HTTPS
  - Implement rate limiting
  - Add API key rotation
  - Use reverse proxy (nginx)

---

## Contributing

To extend ARIA:

### Add a New Tool
1. Create function in `tools/new_tool.py`
2. Decorate with `@tool`
3. Add to `TOOLS` list in `agent.py`
4. Document the tool's docstring

### Modify the Agent
1. Edit `SYSTEM_PROMPT` in `agent.py`
2. Change `temperature`, `max_tokens`, `max_iterations`
3. Test with different query types

### Enhance the UI
1. Edit `frontend/index.html` (styles)
2. Edit `frontend/app.js` (logic)
3. Refresh browser to see changes (reload is active)

---

## Resources

- **LangChain Docs**: https://docs.langchain.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Groq Console**: https://console.groq.com
- **Tavily API**: https://tavily.com/api
- **ReAct Paper**: https://arxiv.org/abs/2210.03629

---

## Roadmap

**v1.0** (Current)
- Core ReAct agent
- Web search + document reading
- Basic UI
- Session memory

**v1.1** (Planned)
- Streaming responses (SSE)
- Persistent storage (SQLite)

**v2.0** (Future)
- Multiple LLM support
- User authentication
- Advanced RAG
- Voice input

---

## License

This project is provided as-is for educational and personal use.

---

## Support

Found a bug? Want a feature? Create an issue on GitHub!

---

**Made with ❤️ using LangChain, FastAPI, and Groq**

*Repository: https://github.com/Pamu0002/langchain-react-agent*
*Last Updated: April 2026*