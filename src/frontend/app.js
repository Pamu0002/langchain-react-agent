const API_BASE = "http://localhost:8000";

let sessionId = null;
let isLoading = false;

// --- Message rendering ---

function appendMessage(role, text) {
  const welcome = document.getElementById("welcome");
  if (welcome) welcome.remove();

  const container = document.getElementById("messages");
  const div = document.createElement("div");
  div.className = `message ${role}`;

  const initial = role === "user" ? "U" : "A";
  const avatarClass = role === "user" ? "user-av" : "aria-av";

  div.innerHTML = `
    <div class="avatar ${avatarClass}">${initial}</div>
    <div class="bubble">${formatText(text)}</div>
  `;

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function appendTyping() {
  const welcome = document.getElementById("welcome");
  if (welcome) welcome.remove();

  const container = document.getElementById("messages");
  const div = document.createElement("div");
  div.className = "message assistant";
  div.id = "typing-indicator";
  div.innerHTML = `
    <div class="avatar aria-av">A</div>
    <div class="bubble typing">
      <span></span><span></span><span></span>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

function formatText(text) {
  // Basic markdown: code blocks, bold, line breaks
  return text
    .replace(/```([\s\S]*?)```/g, "<pre>$1</pre>")
    .replace(/`([^`]+)`/g, "<code style='background:#f5f5f4;padding:2px 5px;border-radius:4px;font-size:12px'>$1</code>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");
}

// --- Send message ---

async function sendMessage() {
  const input = document.getElementById("msg-input");
  const message = input.value.trim();
  if (!message || isLoading) return;

  input.value = "";
  input.style.height = "44px";
  setLoading(true);

  appendMessage("user", message);
  appendTyping();

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId })
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();

    removeTyping();
    appendMessage("assistant", data.response);

    // Save session
    sessionId = data.session_id;
    document.getElementById("session-display").textContent = `session: ${sessionId}`;

  } catch (err) {
    removeTyping();
    appendMessage("assistant", `Sorry, something went wrong: ${err.message}`);
  } finally {
    setLoading(false);
  }
}

// --- File upload ---

async function uploadFile(input) {
  const file = input.files[0];
  if (!file) return;

  const status = document.getElementById("file-status");
  status.textContent = `Uploading ${file.name}...`;
  status.className = "file-status visible";
  status.style.color = "#888";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Upload failed");
    }

    const data = await res.json();
    status.textContent = `${file.name} uploaded successfully`;
    status.style.color = "#22c55e";

    appendMessage("assistant", `I've loaded **${file.name}** (${data.size_mb}MB). Ask me anything about it!`);

  } catch (err) {
    status.textContent = `Upload failed: ${err.message}`;
    status.style.color = "#ef4444";
  }

  input.value = "";
  setTimeout(() => { status.className = "file-status"; }, 4000);
}

// --- Clear chat ---

async function clearChat() {
  if (sessionId) {
    await fetch(`${API_BASE}/clear`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId })
    });
  }
  sessionId = null;
  document.getElementById("messages").innerHTML = `
    <div class="welcome" id="welcome">
      <h2>Hello, I'm ARIA</h2>
      <p>I can answer questions, search the web, and read your uploaded documents.</p>
      <div class="chips">
        <div class="chip" onclick="sendSuggestion(this)">What can you do?</div>
        <div class="chip" onclick="sendSuggestion(this)">Search the web for AI news today</div>
        <div class="chip" onclick="sendSuggestion(this)">What files do I have uploaded?</div>
        <div class="chip" onclick="sendSuggestion(this)">Tell me a fun fact</div>
      </div>
    </div>`;
  document.getElementById("session-display").textContent = "";
}

// --- Helpers ---

function sendSuggestion(chip) {
  const input = document.getElementById("msg-input");
  input.value = chip.textContent;
  sendMessage();
}

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function autoResize(el) {
  el.style.height = "44px";
  el.style.height = Math.min(el.scrollHeight, 140) + "px";
}

function setLoading(state) {
  isLoading = state;
  document.getElementById("send-btn").disabled = state;
  document.getElementById("msg-input").disabled = state;
}
