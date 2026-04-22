// ── DOM refs ──────────────────────────────────────────────────────────────────
const userInput       = document.getElementById("user-input");
const chatBox         = document.getElementById("chat-box");
const suggestionsArea = document.getElementById("suggestions-area");

// ── Boot ─────────────────────────────────────────────────────────────────────
window.addEventListener("load", () => {
    userInput.focus();
    setTimeout(() => {
        addMessage("👋 Hello! I'm your AI ChatBot. Ask me anything about science, math, history, geography, technology, health, and more. I'll give you real answers!", "bot");
    }, 600);
});

// ── Suggestion click ─────────────────────────────────────────────────────────
function suggestClick(text) {
    userInput.value = text;
    userInput.focus();
    setTimeout(sendMessage, 120);
}

// ── Send message ─────────────────────────────────────────────────────────────
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) { userInput.focus(); return; }

    // Hide suggestions on first real message
    if (suggestionsArea && chatBox.children.length <= 1) {
        suggestionsArea.style.opacity = "0";
        suggestionsArea.style.maxHeight = "0";
        suggestionsArea.style.padding = "0 28px";
        setTimeout(() => suggestionsArea.style.display = "none", 350);
    }

    addMessage(message, "user");
    userInput.value = "";
    userInput.focus();
    showTypingIndicator();

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        if (!res.ok) throw new Error("Bad response");

        const data = await res.json();
        removeTypingIndicator();
        setTimeout(() => addMessage(data.reply, "bot"), 200);

    } catch (err) {
        removeTypingIndicator();
        addMessage("⚠️ I couldn't connect to the server. Please make sure the Flask app is running and try again.", "bot");
        console.error(err);
    }
}

// ── Add message ───────────────────────────────────────────────────────────────
function addMessage(text, sender) {
    const wrap    = document.createElement("div");
    wrap.classList.add("message", sender);

    if (sender === "bot") {
        const avatar = document.createElement("div");
        avatar.classList.add("msg-avatar");
        avatar.textContent = "🤖";
        wrap.appendChild(avatar);
    }

    const bubble = document.createElement("div");
    bubble.classList.add("message-content");
    bubble.textContent = text;

    wrap.appendChild(bubble);
    chatBox.appendChild(wrap);
    scrollBottom();
}

// ── Typing indicator ──────────────────────────────────────────────────────────
function showTypingIndicator() {
    const wrap = document.createElement("div");
    wrap.classList.add("message", "bot");
    wrap.id = "typing-indicator";

    const avatar = document.createElement("div");
    avatar.classList.add("msg-avatar");
    avatar.textContent = "🤖";

    const dots = document.createElement("div");
    dots.classList.add("typing-indicator");
    dots.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

    wrap.appendChild(avatar);
    wrap.appendChild(dots);
    chatBox.appendChild(wrap);
    scrollBottom();
}

function removeTypingIndicator() {
    const el = document.getElementById("typing-indicator");
    if (el) el.remove();
}

// ── Scroll ────────────────────────────────────────────────────────────────────
function scrollBottom() {
    setTimeout(() => chatBox.scrollTop = chatBox.scrollHeight, 60);
}

// ── Clear chat ────────────────────────────────────────────────────────────────
function clearChat() {
    if (chatBox.children.length === 0) return;
    chatBox.style.opacity = "0.4";
    setTimeout(() => {
        chatBox.innerHTML = "";
        chatBox.style.opacity = "1";
        userInput.focus();

        // Show suggestions again
        if (suggestionsArea) {
            suggestionsArea.style.display = "block";
            suggestionsArea.style.opacity = "1";
            suggestionsArea.style.maxHeight = "160px";
            suggestionsArea.style.padding   = "12px 28px";
        }

        setTimeout(() => addMessage("👋 Welcome back! Start a fresh conversation. What would you like to know?", "bot"), 300);
    }, 250);
}

// ── About dialog ──────────────────────────────────────────────────────────────
function showInfo() {
    alert("🤖  AI ChatBot v2.0\n\n📚 I can answer questions about:\n  • Science & Nature\n  • Math (including calculations)\n  • World History\n  • Geography\n  • Technology & Programming\n  • Health & Lifestyle\n  • Fun & Trivia\n\n⚙️ Built with: Python · Flask · JavaScript\n\nJust ask me anything!");
}

// ── Enter key ─────────────────────────────────────────────────────────────────
userInput.addEventListener("keypress", e => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});


// Focus input on load
window.addEventListener("load", () => {
    userInput.focus();
    setupEventListeners();
});

// Setup event listeners for all buttons
function setupEventListeners() {
    // Info button click handler
    const infoBtn = document.querySelector(".btn-info");
    if (infoBtn) {
        infoBtn.addEventListener("click", () => {
            alert("🤖 AI ChatBot v1.0\n\n✨ Features:\n💬 Real-time chat\n🎯 Smart suggestions\n🚀 Powered by AI\n\nMade with ❤️ for amazing conversations!");
        });
    }
}

// Handle suggestion button click
function suggestClick(suggestion) {
    userInput.value = suggestion;
    userInput.focus();
    
    // Add visual feedback
    userInput.style.transform = "scale(1.02)";
    setTimeout(() => {
        userInput.style.transform = "scale(1)";
        sendMessage();
    }, 100);
}

// Send message function
async function sendMessage() {
    const message = userInput.value.trim();

    if (message === "") {
        userInput.focus();
        return;
    }

    // Hide suggestions on first message
    if (suggestionsArea && chatBox.children.length === 0) {
        suggestionsArea.style.display = "none";
    }

    // Add user message to chat
    addMessage(message, "user");
    userInput.value = "";
    userInput.focus();

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send message to backend
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        // Add bot response with delay for natural feel
        setTimeout(() => {
            addMessage(data.reply, "bot");
        }, 300);

    } catch (error) {
        removeTypingIndicator();
        addMessage("Sorry, something went wrong. Please try again. 🔧", "bot");
        console.error("Error:", error);
    }
}

// Add message to chat
function addMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");
    contentDiv.textContent = message;

    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);

    // Scroll to bottom with smooth behavior
    scrollToBottom();
}

// Show typing indicator
function showTypingIndicator() {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "bot");
    messageDiv.id = "typing-indicator";

    const typingDiv = document.createElement("div");
    typingDiv.classList.add("typing-indicator");
    typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

    messageDiv.appendChild(typingDiv);
    chatBox.appendChild(messageDiv);

    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById("typing-indicator");
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 50);
}

// Clear chat
function clearChat() {
    if (chatBox.children.length === 0) {
        return; // Already empty
    }
    
    if (confirm("🗑️ Clear all messages? This action cannot be undone.")) {
        // Fade out effect
        chatBox.style.opacity = "0.5";
        setTimeout(() => {
            chatBox.innerHTML = "";
            chatBox.style.opacity = "1";
            userInput.focus();
            
            // Show suggestions again
            if (suggestionsArea) {
                suggestionsArea.style.display = "block";
            }
            
            // Add welcome message
            setTimeout(() => {
                addMessage("👋 Welcome! I'm ready to chat. What would you like to know?", "bot");
            }, 300);
        }, 300);
    }
}

// Enter key support
userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

// Add welcome message on load
window.addEventListener("load", () => {
    setTimeout(() => {
        addMessage("👋 Welcome! I'm your AI ChatBot. Ask me anything and I'll do my best to help!", "bot");
    }, 800);
});