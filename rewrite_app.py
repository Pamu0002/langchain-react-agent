#!/usr/bin/env python3
import os

new_app_js = '''const API_BASE = "http://localhost:8000";

let sessionId = null;
let isLoading = false;
let isDarkMode = localStorage.getItem("theme") === "dark";

console.log("✅ app.js loaded - API_BASE:", API_BASE);
console.log("✅ isDarkMode from localStorage:", isDarkMode);

// --- THEME FUNCTIONS ---
function initTheme() {
  console.log("🎨 initTheme() called, isDarkMode:", isDarkMode);
  if (isDarkMode) {
    document.body.classList.add("dark-mode");
    const toggle = document.querySelector(".theme-toggle");
    if (toggle) toggle.textContent = "☀️";
    const name = document.getElementById("theme-name");
    if (name) name.textContent = "Dark";
  } else {
    document.body.classList.remove("dark-mode");
    const toggle = document.querySelector(".theme-toggle");
    if (toggle) toggle.textContent = "🌙";
    const name = document.getElementById("theme-name");
    if (name) name.textContent = "Light";
  }
}

function toggleTheme() {
  console.log("🔄 toggleTheme() called");
  isDarkMode = !isDarkMode;
  document.body.classList.toggle("dark-mode");
  
  const toggleBtn = document.querySelector(".theme-toggle");
  if (toggleBtn) toggleBtn.textContent = isDarkMode ? "☀️" : "🌙";
  
  const themeName = document.getElementById("theme-name");
  if (themeName) themeName.textContent = isDarkMode ? "Dark" : "Light";
  
  localStorage.setItem("theme", isDarkMode ? "dark" : "light");
  console.log("✅ Theme switched to:", isDarkMode ? "DARK" : "LIGHT");
}

// --- MESSAGE FUNCTIONS ---
function appendMessage(role, text, agentUsed = null) {
  console.log("📝 appendMessage() - role:", role, "text length:", text.length);
  
  const welcome = document.getElementById("welcome");
  if (welcome) welcome.style.display = "none";

  const container = document.getElementById("messages");
  if (!container) {
    console.error("❌ Messages container NOT found!");
    return null;
  }

  const div = document.createElement("div");
  div.className = `message ${role}`;

  const initial = role === "user" ? "👤" : "✨";
  const avatarClass = role === "user" ? "user-av" : "aria-av";

  let html = `
    <div class="avatar ${avatarClass}">${initial}</div>
    <div class="message-content">
  `;
  
  if (role === "assistant" && agentUsed) {
    html += `<div class="agent-badge">${agentUsed}</div>`;
  }
  
  html += `<div class="bubble">${formatText(text)}</div></div>`;

  div.innerHTML = html;
  
  if (role === "assistant") {
    div.style.cursor = "pointer";
    div.addEventListener("click", () => {
      const bubble = div.querySelector(".bubble");
      navigator.clipboard.writeText(bubble.innerText);
    });
  }
  
  container.appendChild(div);
  console.log("✅ Message added!");
  container.scrollTop = container.scrollHeight;
  return div;
}

function formatText(text) {
  return text
    .replace(/```([\\s\\S]*?)```/g, "<pre>$1</pre>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\\*\\*(.*?)\\*\\*/g, "<strong>$1</strong>")
    .replace(/\\n/g, "<br>");
}

function appendTyping() {
  const container = document.getElementById("messages");
  if (!container) return;
  
  const div = document.createElement("div");
  div.className = "message assistant";
  div.id = "typing-indicator";
  div.innerHTML = `
    <div class="avatar aria-av">✨</div>
    <div class="message-content">
      <div class="bubble typing"><span></span><span></span><span></span></div>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

// --- SEND MESSAGE ---
async function sendMessage() {
  console.log("📤 sendMessage() called");
  
  const input = document.getElementById("msg-input");
  if (!input) {
    console.error("❌ Input element NOT found!");
    return;
  }
  
  const message = input.value.trim();
  console.log("💬 Message text:", message, "isLoading:", isLoading);
  
  if (!message || isLoading) {
    console.log("⚠️ Empty message or already loading");
    return;
  }

  input.value = "";
  input.style.height = "44px";
  isLoading = true;

  appendMessage("user", message);
  appendTyping();

  try {
    console.log("🚀 Sending to API...");
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId })
    });

    console.log("📨 Response status:", res.status);
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    
    const data = await res.json();
    console.log("💾 Got data - session:", data.session_id);
    
    removeTyping();
    appendMessage("assistant", data.response, data.agent_used);
    
    sessionId = data.session_id;
    const sessionDisplay = document.getElementById("session-display");
    if (sessionDisplay) sessionDisplay.textContent = `session: ${sessionId || ""}`;

  } catch (err) {
    console.error("❌ Error:", err.message);
    removeTyping();
    appendMessage("assistant", `Error: ${err.message}`);
  } finally {
    isLoading = false;
  }
}

// --- CLEAR CHAT ---
async function clearChat() {
  console.log("🗑️ clearChat() called");
  if (sessionId) {
    await fetch(`${API_BASE}/clear`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId })
    }).catch(e => console.error("Clear error:", e));
  }
  sessionId = null;
  const messagesDiv = document.getElementById("messages");
  if (messagesDiv) {
    messagesDiv.innerHTML = `
      <div class="welcome" id="welcome">
        <h2>Welcome to ARIA ✨</h2>
        <p>Your intelligent multi-agent AI assistant</p>
      </div>
    `;
  }
}

// --- FILE UPLOAD ---
async function uploadFile(input) {
  console.log("📎 uploadFile() called");
  const file = input.files[0];
  if (!file) return;

  const status = document.getElementById("file-status");
  if (status) status.textContent = `Uploading ${file.name}...`;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
    if (!res.ok) throw new Error("Upload failed");
    const data = await res.json();
    if (status) status.textContent = `✅ ${file.name} uploaded`;
    appendMessage("assistant", `Loaded: **${file.name}** (${data.size_mb}MB)`, "Document Agent");
  } catch (err) {
    if (status) status.textContent = `❌ Error: ${err.message}`;
    console.error("Upload error:", err);
  }
  input.value = "";
}

// --- INITIALIZE ALL WHEN DOM READY ---
function initializeApp() {
  console.log("🚀 Initializing app...");
  
  initTheme();
  
  // Setup Send Button
  const sendBtn = document.querySelector(".send-btn");
  if (sendBtn) {
    sendBtn.addEventListener("click", sendMessage);
    console.log("✅ Send button ready");
  } else console.error("❌ Send button not found");

  // Setup Input Enter key
  const msgInput = document.getElementById("msg-input");
  if (msgInput) {
    msgInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    msgInput.addEventListener("input", () => {
      msgInput.style.height = "44px";
      msgInput.style.height = Math.min(msgInput.scrollHeight, 150) + "px";
    });
    console.log("✅ Input field ready");
  } else console.error("❌ Input not found");

  // Setup Theme Toggle
  const themeToggle = document.querySelector(".theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
    console.log("✅ Theme toggle ready");
  } else console.error("❌ Theme toggle not found");

  // Setup Clear Button
  const clearBtn = document.querySelector(".clear-btn");
  if (clearBtn) {
    clearBtn.addEventListener("click", clearChat);
    console.log("✅ Clear button ready");
  } else console.error("❌ Clear button not found");

  // Setup File Upload
  const uploadBtn = document.querySelector(".upload-btn");
  const fileInput = document.getElementById("file-input");
  if (uploadBtn && fileInput) {
    uploadBtn.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => uploadFile(e.target));
    console.log("✅ File upload ready");
  } else console.error("❌ Upload components not found");

  // Setup Quick Chips
  const chips = document.querySelectorAll(".chip");
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const msg = chip.getAttribute("data-message") || chip.textContent.trim();
      const input = document.getElementById("msg-input");
      if (input) input.value = msg;
      sendMessage();
    });
  });
  if (chips.length > 0) console.log("✅ Quick chips ready");

  console.log("✨ App initialization complete!");
}

// Start when DOM is ready
if (document.readyState === 'loading') {
  console.log("📋 DOM loading, waiting for DOMContentLoaded...");
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  console.log("📋 DOM already ready, initializing now...");
  initializeApp();
}
'''

file_path = r"c:\Users\Pamudi\Desktop\new\Projects\agent aiii\src\frontend\app.js"
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_app_js)

print(f"✅ app.js updated successfully!")
print(f"📝 File size: {len(new_app_js)} characters")
