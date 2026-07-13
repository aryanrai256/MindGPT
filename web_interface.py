#!/usr/bin/env python3
"""
MindCare Web Interface
A simple web interface for the psychology chatbot using Flask
"""

import datetime
import os
import secrets
import threading
import uuid

from flask import Flask, request, jsonify, render_template_string, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from main import PsychologyChatbot

app = Flask(__name__)

# A secret key is required to sign the session cookie that identifies each
# visitor. Set SECRET_KEY in the environment for any real deployment - if
# it's not set we fall back to a random key generated at startup, which
# means every restart invalidates existing sessions. That's an acceptable
# default for local/dev use but should not be relied on in production.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
if not os.environ.get("SECRET_KEY"):
    print(
        "WARNING: SECRET_KEY not set in the environment - using a randomly "
        "generated key for this process. Sessions will not survive a "
        "restart. Set SECRET_KEY for production deployments."
    )

# Cap request body size to prevent trivially large payloads.
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # 16 KB

MAX_MESSAGE_LENGTH = 2000
SESSION_TIMEOUT = datetime.timedelta(hours=2)
app.permanent_session_lifetime = SESSION_TIMEOUT

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"],
    storage_uri="memory://",
)


class _SessionEntry:
    """One chatbot + lock per browser session."""

    def __init__(self):
        self.chatbot = PsychologyChatbot("MindCare")
        self.lock = threading.Lock()
        self.last_active = datetime.datetime.now()


# In-process, per-session chatbot store. This replaces the old module-level
# singleton `chatbot` instance that every visitor shared (which leaked
# conversation history, names, and crisis state across unrelated users).
#
# Note: this dict lives in one process's memory. It resets on restart and
# is NOT shared across multiple worker processes - if this is ever run
# behind gunicorn/uwsgi with more than one worker, move this to a shared
# store (e.g. Redis) instead, or pin to a single worker.
_sessions: dict = {}
_sessions_lock = threading.Lock()


def _prune_stale_sessions():
    """Drop sessions that have been idle past SESSION_TIMEOUT."""
    cutoff = datetime.datetime.now() - SESSION_TIMEOUT
    stale = [sid for sid, entry in _sessions.items() if entry.last_active < cutoff]
    for sid in stale:
        _sessions.pop(sid, None)


def _get_session_entry() -> _SessionEntry:
    """Get (creating if needed) the chatbot session tied to this browser."""
    sid = session.get("session_id")
    with _sessions_lock:
        if not sid or sid not in _sessions:
            sid = uuid.uuid4().hex
            session["session_id"] = sid
            session.permanent = True
            _sessions[sid] = _SessionEntry()
            _prune_stale_sessions()
        entry = _sessions[sid]
        entry.last_active = datetime.datetime.now()
        return entry


# HTML template for the web interface
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MindCare - Psychology Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 800px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 90vh;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 5px;
        }
        
        .header p {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        
        .messages {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            line-height: 1.4;
            animation: fadeIn 0.3s ease-in;
        }
        
        .user-message {
            align-self: flex-end;
            background: #667eea;
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .bot-message {
            align-self: flex-start;
            background: white;
            color: #333;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .bot-message p {
            margin: 5px 0;
        }
        
        .bot-message strong {
            color: #667eea;
        }
        
        .bot-message ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .bot-message li {
            margin: 5px 0;
        }
        
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
        }
        
        .input-area {
            display: flex;
            gap: 10px;
        }
        
        .message-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 1em;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .message-input:focus {
            border-color: #667eea;
        }
        
        .send-button {
            padding: 12px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .send-button:active {
            transform: translateY(0);
        }
        
        .send-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .typing-indicator {
            display: none;
            padding: 10px 20px;
            background: white;
            border-radius: 20px;
            align-self: flex-start;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            margin: 0 3px;
            animation: bounce 1.4s infinite ease-in-out;
        }
        
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0s; }
        
        .disclaimer {
            font-size: 0.8em;
            color: #666;
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-top: 1px solid #eee;
        }
        
        .welcome-message {
            text-align: center;
            color: #666;
            font-style: italic;
            margin-top: 20px;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes bounce {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1);
            }
        }
        
        @media (max-width: 600px) {
            .message {
                max-width: 90%;
            }
            
            .header h1 {
                font-size: 1.5em;
            }
            
            .container {
                height: 100vh;
            }
        }
        
        .crisis-warning {
            background: #ffebee;
            border: 1px solid #f44336;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            text-align: center;
        }
        
        .crisis-warning strong {
            color: #c62828;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 MindCare</h1>
            <p>Psychology & Psychiatry Chatbot</p>
        </div>
        
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="welcome-message">
                    <p>Hello! I'm MindCare, your mental health companion.</p>
                    <p>How are you feeling today?</p>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        
        <div class="input-container">
            <div class="input-area">
                <input type="text" class="message-input" id="messageInput" 
                       placeholder="Type your message here..." autocomplete="off">
                <button class="send-button" id="sendButton">Send</button>
            </div>
        </div>
        
        <div class="disclaimer">
            <strong>Disclaimer:</strong> MindCare provides informational support only. 
            It is NOT a substitute for professional mental health care. 
            If you are in crisis, please contact a mental health professional immediately.
        </div>
    </div>
    
    <script>
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const messagesContainer = document.getElementById('messages');
        const typingIndicator = document.getElementById('typingIndicator');
        
        // Add initial bot message
        addBotMessage("Hello! I'm MindCare, your mental health companion. What's your name?");
        
        // Focus on input field
        messageInput.focus();
        
        // Send message on button click
        sendButton.addEventListener('click', sendMessage);
        
        // Send message on Enter key - use keydown instead of keypress for better compatibility
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent form submission if any
                sendMessage();
            }
        });
        
        // Send message function
        function sendMessage() {
            const message = messageInput.value.trim();
            if (message === '') return;
            
            // Add user message
            addUserMessage(message);
            
            // Clear input
            messageInput.value = '';
            
            // Disable input while waiting for response
            messageInput.disabled = true;
            sendButton.disabled = true;
            
            // Show typing indicator
            typingIndicator.style.display = 'flex';
            
            // Scroll to bottom
            scrollToBottom();
            
            // Send to server
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Hide typing indicator
                typingIndicator.style.display = 'none';
                
                // Add bot response
                addBotMessage(data.response);
                
                // Check if it's a crisis response
                if (data.crisis_level >= 3) {
                    showCrisisWarning();
                }
                
                // Re-enable input
                messageInput.disabled = false;
                sendButton.disabled = false;
                
                // Focus on input
                messageInput.focus();
                
                // Scroll to bottom
                scrollToBottom();
            })
            .catch(error => {
                console.error('Error:', error);
                typingIndicator.style.display = 'none';
                addBotMessage("I'm sorry, I encountered an error. Please try again.");
                messageInput.disabled = false;
                sendButton.disabled = false;
                messageInput.focus();
            });
        }
        
        // Add user message to chat
        function addUserMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user-message';
            messageDiv.textContent = message;
            messagesContainer.appendChild(messageDiv);
            scrollToBottom();
        }
        
        // Escape HTML special characters so any text we later inject via
        // innerHTML can't be interpreted as markup/scripts. All bot replies
        // currently come from a fixed knowledge base, but escaping here
        // means this stays safe even if a future response ever reflects
        // user-provided text back into the chat.
        function escapeHtml(str) {
            const div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

        // Add bot message to chat
        function addBotMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot-message';
            
            // Escape first, then apply our own lightweight markdown-ish
            // formatting (bold, bullets, newlines) on top of the escaped text.
            let formattedMessage = escapeHtml(message)
                .replace(/\n\n/g, '<p></p>')
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\- (.*?)(?=\n|$)/g, '<li>$1</li>')
                .replace(/<li>/g, '<ul><li>')
                .replace(/<\/p><ul>/g, '<p><ul>')
                .replace(/<\/ul><p>/g, '</ul><p>')
                .replace(/<\/ul>/g, '</ul>');
            
            // Ensure proper HTML structure
            if (formattedMessage.includes('<ul>') && !formattedMessage.includes('<p><ul>')) {
                formattedMessage = '<p>' + formattedMessage.replace(/<ul>/g, '<ul>');
            }
            if (formattedMessage.includes('</ul>') && !formattedMessage.includes('</ul></p>')) {
                formattedMessage = formattedMessage.replace(/<\/ul>/g, '</ul>') + '</p>';
            }
            if (!formattedMessage.includes('<p>')) {
                formattedMessage = '<p>' + formattedMessage + '</p>';
            }
            
            messageDiv.innerHTML = formattedMessage;
            messagesContainer.appendChild(messageDiv);
            scrollToBottom();
        }
        
        // Show crisis warning
        function showCrisisWarning() {
            const warningDiv = document.createElement('div');
            warningDiv.className = 'message crisis-warning';
            warningDiv.innerHTML = `
                <strong>⚠️ Crisis Detected:</strong> If you are in immediate danger or 
                experiencing thoughts of self-harm, please contact emergency services 
                or a crisis hotline immediately. In the US, call or text 988.
            `;
            messagesContainer.appendChild(warningDiv);
            scrollToBottom();
        }
        
        // Scroll to bottom of chat
        function scrollToBottom() {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Auto-scroll as new content is added
        const observer = new MutationObserver(scrollToBottom);
        observer.observe(messagesContainer, {
            childList: true,
            subtree: true
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/chat', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    """Handle chat messages"""
    # get_json(silent=True) returns None instead of raising on a missing or
    # malformed body, so a bad request can't crash the process anymore.
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '')

    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({'error': 'message must be a non-empty string'}), 400

    if len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({
            'error': f'message must be under {MAX_MESSAGE_LENGTH} characters'
        }), 400

    entry = _get_session_entry()
    with entry.lock:
        response = entry.chatbot.process_input(user_message)
        crisis_level = entry.chatbot.crisis_level.value

    return jsonify({
        'response': response,
        'crisis_level': crisis_level
    })


@app.route('/reset', methods=['POST'])
def reset():
    """Reset the current user's chatbot session (does not affect other users)"""
    entry = _get_session_entry()
    with entry.lock:
        entry.chatbot = PsychologyChatbot("MindCare")
    return jsonify({'status': 'reset'})


@app.route('/summary')
def summary():
    """Get conversation summary for the current user's session"""
    entry = _get_session_entry()
    with entry.lock:
        summary_text = entry.chatbot.get_conversation_summary()
    return jsonify({'summary': summary_text})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Debug mode is OFF by default. It enables the interactive Werkzeug
    # debugger, which allows arbitrary code execution from the browser on
    # any unhandled exception - never turn this on outside local development.
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    # Default to loopback-only; set HOST=0.0.0.0 explicitly (behind a real
    # WSGI server/reverse proxy) for anything beyond local development.
    host = os.environ.get('HOST', '127.0.0.1')

    print(f"Starting MindCare Web Interface on port {port}")
    print(f"Open your browser and navigate to: http://localhost:{port}")
    if debug_mode:
        print(
            "WARNING: FLASK_DEBUG is enabled. Do not use this in production - "
            "the interactive debugger allows remote code execution."
        )

    app.run(host=host, port=port, debug=debug_mode)
