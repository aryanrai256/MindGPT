#!/usr/bin/env python3
"""
MindCare Web Interface
A simple web interface for the psychology chatbot using Flask
"""

from flask import Flask, request, jsonify, render_template_string
from main import PsychologyChatbot
import datetime
import os

app = Flask(__name__)

# Create a global chatbot instance
chatbot = PsychologyChatbot("MindCare")

# HTML template for the web interface
HTML_TEMPLATE = """
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
        
        // Send message on Enter key
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
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
        
        // Add bot message to chat
        function addBotMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot-message';
            
            // Convert newlines to <br> and format lists
            let formattedMessage = message
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
def chat():
    """Handle chat messages"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Process the message
    response = chatbot.process_input(user_message)
    
    # Get crisis level
    crisis_level = chatbot.crisis_level.value
    
    return jsonify({
        'response': response,
        'crisis_level': crisis_level
    })


@app.route('/reset')
def reset():
    """Reset the chatbot"""
    global chatbot
    chatbot = PsychologyChatbot("MindCare")
    return jsonify({'status': 'reset'})


@app.route('/summary')
def summary():
    """Get conversation summary"""
    summary = chatbot.get_conversation_summary()
    return jsonify({'summary': summary})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting MindCare Web Interface on port {port}")
    print("Open your browser and navigate to: http://localhost:{}".format(port))
    app.run(host='0.0.0.0', port=port, debug=True)
