class ZoalAIChat {
    constructor() {
        this.sessionId = null;
        this.modelChoice = 'openai';
        this.isTyping = false;
        
        this.initializeElements();
        this.bindEvents();
        this.loadChatHistory();
    }

    initializeElements() {
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.chatMessages = document.getElementById('chat-messages');
        this.modelSelector = document.getElementById('model-choice');
        this.typingIndicator = document.getElementById('typing-indicator');
    }

    bindEvents() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.modelSelector.addEventListener('change', (e) => {
            this.modelChoice = e.target.value;
            this.showModelChangeNotification();
        });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;

        // Clear input
        this.messageInput.value = '';
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await this.callChatAPI(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response to chat
            this.addMessage(response.response, 'bot');
            
            // Update session ID if new
            if (response.session_id) {
                this.sessionId = response.session_id;
            }
            
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            console.error('Chat error:', error);
        }
    }

    async callChatAPI(message) {
        const response = await fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                message: message,
                session_id: this.sessionId,
                model_choice: this.modelChoice
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        if (sender === 'user') {
            avatar.innerHTML = '<i class="fas fa-user"></i>';
        } else {
            avatar.innerHTML = '<i class="fas fa-robot"></i>';
        }
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.isTyping = true;
        this.sendButton.disabled = true;
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        this.sendButton.disabled = false;
        this.typingIndicator.style.display = 'none';
    }

    showModelChangeNotification() {
        const notification = document.createElement('div');
        notification.className = 'message bot';
        notification.style.animation = 'fadeInUp 0.5s ease';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = `Switched to ${this.modelChoice === 'openai' ? 'OpenAI GPT' : 'Google Gemini'} model.`;
        
        notification.appendChild(avatar);
        notification.appendChild(messageContent);
        
        this.chatMessages.appendChild(notification);
        this.scrollToBottom();
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    async loadChatHistory() {
        if (!this.sessionId) return;
        
        try {
            const response = await fetch('/history/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    session_id: this.sessionId
                })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.history && data.history.length > 0) {
                    // Remove welcome message
                    const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
                    if (welcomeMessage) {
                        welcomeMessage.remove();
                    }
                    
                    // Load history
                    data.history.forEach(item => {
                        this.addMessage(item.message, 'user');
                        this.addMessage(item.response, 'bot');
                    });
                }
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ZoalAIChat();
});

// Add some cultural elements and animations
document.addEventListener('DOMContentLoaded', () => {
    // Add floating cultural patterns
    const container = document.querySelector('.container');
    
    for (let i = 0; i < 5; i++) {
        const pattern = document.createElement('div');
        pattern.className = 'floating-pattern';
        pattern.style.cssText = `
            position: absolute;
            width: 20px;
            height: 20px;
            background: linear-gradient(45deg, rgba(139, 69, 19, 0.3), rgba(210, 105, 30, 0.3));
            border-radius: 50%;
            pointer-events: none;
            animation: float ${3 + i}s ease-in-out infinite;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        container.appendChild(pattern);
    }
});

// Add floating animation
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .floating-pattern {
        z-index: -1;
    }
`;
document.head.appendChild(style); 