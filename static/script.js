document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearChatButton = document.getElementById('clear-chat');
    const typingIndicator = document.getElementById('typing-indicator');

    // Auto-resize textarea as user types
    userInput.addEventListener('input', function() {
        // Reset height to auto to get correct scrollHeight
        this.style.height = 'auto';
        // Set new height based on scrollHeight (with max height constraint handled in CSS)
        this.style.height = (this.scrollHeight) + 'px';
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender + '-message');
        
        // Create avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        const avatarIcon = document.createElement('i');
        
        if (sender === 'user') {
            avatarIcon.classList.add('fas', 'fa-user');
        } else {
            avatarIcon.classList.add('fas', 'fa-robot');
        }
        
        avatarDiv.appendChild(avatarIcon);
        messageDiv.appendChild(avatarDiv);
        
        // Create message content
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        const p = document.createElement('p');
        p.textContent = text;
        contentDiv.appendChild(p);
        messageDiv.appendChild(contentDiv);
        
        chatBox.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function showTypingIndicator() {
        typingIndicator.classList.remove('hidden');
        scrollToBottom();
    }
    
    function hideTypingIndicator() {
        typingIndicator.classList.add('hidden');
    }
    
    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessage(messageText, 'user');
        userInput.value = ''; // Clear input field
        userInput.style.height = 'auto'; // Reset height
        
        // Show typing indicator
        showTypingIndicator();

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText }),
            });

            // Hide typing indicator
            hideTypingIndicator();

            if (!response.ok) {
                const errorData = await response.json();
                addMessage(`Error: ${errorData.error || response.statusText}`, 'bot');
                return;
            }

            const data = await response.json();
            addMessage(data.response, 'bot');

        } catch (error) {
            hideTypingIndicator();
            console.error('Error sending message:', error);
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
        }
    }

    // Clear chat history
    clearChatButton.addEventListener('click', () => {
        // Remove all messages except the initial greeting
        while (chatBox.children.length > 1) {
            chatBox.removeChild(chatBox.lastChild);
        }
    });

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent newline in textarea
            sendMessage();
        }
    });
}); 