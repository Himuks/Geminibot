document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearChatButton = document.getElementById('clear-chat');
    const typingIndicator = document.getElementById('typing-indicator');
    const ingredientTags = document.getElementById('ingredient-tags');
    
    // Store ingredients
    let currentIngredients = [];

    // Auto-resize textarea as user types
    userInput.addEventListener('input', function() {
        // Reset height to auto to get correct scrollHeight
        this.style.height = 'auto';
        // Set new height based on scrollHeight (with max height constraint handled in CSS)
        this.style.height = (this.scrollHeight) + 'px';
    });

    function processAIResponse(text) {
        // Replace Markdown bold formatting with HTML
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                   .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    function addMessage(text, sender, isHtml = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender + '-message');
        
        // Create avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        const avatarIcon = document.createElement('i');
        
        if (sender === 'user') {
            avatarIcon.classList.add('fas', 'fa-user');
        } else {
            avatarIcon.classList.add('fas', 'fa-chef-hat');
        }
        
        avatarDiv.appendChild(avatarIcon);
        messageDiv.appendChild(avatarDiv);
        
        // Create message content
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        if (isHtml) {
            contentDiv.innerHTML = text;
        } else {
            // Process any markdown in text if it's from the bot
            if (sender === 'bot') {
                const p = document.createElement('p');
                p.innerHTML = processAIResponse(text);
                contentDiv.appendChild(p);
            } else {
                const p = document.createElement('p');
                p.textContent = text;
                contentDiv.appendChild(p);
            }
        }
        
        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function extractIngredients(message) {
        // Simple ingredient extraction (split by commas or 'and')
        let text = message.toLowerCase();
        
        // Check if the message looks like it contains a list of ingredients
        if (text.includes('i have') || text.includes('got') || text.includes('in my') || 
            text.includes('ingredient') || text.includes('pantry') || text.includes('fridge')) {
            
            // Remove common phrases
            text = text.replace(/i have/g, '')
                       .replace(/i've got/g, '')
                       .replace(/in my pantry/g, '')
                       .replace(/in my fridge/g, '')
                       .replace(/in my kitchen/g, '')
                       .replace(/i got/g, '')
                       .replace(/ingredients:/g, '')
                       .replace(/ingredients are/g, '')
                       .replace(/ingredients/g, '');
                       
            // Split by common separators
            const separators = [',', ' and ', ' & '];
            let ingredients = [];
            
            let workingText = text;
            for (const separator of separators) {
                if (workingText.includes(separator)) {
                    ingredients = workingText.split(separator).map(item => item.trim()).filter(item => item.length > 0);
                    break;
                }
            }
            
            // If no separators found, treat the whole text as potentially one ingredient
            if (ingredients.length === 0 && workingText.trim().length > 0) {
                ingredients = [workingText.trim()];
            }
            
            // Filter very short words and common stop words
            const stopWords = ['and', 'the', 'a', 'an', 'have', 'has', 'some', 'few'];
            ingredients = ingredients.filter(ingredient => 
                ingredient.length > 1 && !stopWords.includes(ingredient)
            );
            
            return ingredients;
        }
        
        return [];
    }
    
    function addIngredientTag(ingredient) {
        if (currentIngredients.includes(ingredient)) return;
        
        currentIngredients.push(ingredient);
        
        const tag = document.createElement('div');
        tag.classList.add('ingredient-tag');
        tag.dataset.ingredient = ingredient;
        
        const text = document.createElement('span');
        text.textContent = ingredient;
        tag.appendChild(text);
        
        const removeButton = document.createElement('button');
        removeButton.innerHTML = '&times;';
        removeButton.addEventListener('click', () => {
            ingredientTags.removeChild(tag);
            currentIngredients = currentIngredients.filter(item => item !== ingredient);
        });
        
        tag.appendChild(removeButton);
        ingredientTags.appendChild(tag);
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

    // Format recipe for display
    function formatRecipe(recipe) {
        if (!recipe) return 'Sorry, I couldn\'t find a suitable recipe with those ingredients.';
        
        return `
            <div class="recipe-card">
                <h3>${recipe.name}</h3>
                <p><strong>Time:</strong> ${recipe.time} minutes</p>
                <p><strong>Difficulty:</strong> ${recipe.difficulty}</p>
                <h4>Ingredients:</h4>
                <ul>
                    ${recipe.ingredients.map(ing => `<li>${ing}</li>`).join('')}
                </ul>
                <h4>Instructions:</h4>
                <ol>
                    ${recipe.steps.map(step => `<li>${step}</li>`).join('')}
                </ol>
                ${recipe.image ? `<img src="${recipe.image}" alt="${recipe.name}">` : ''}
                ${recipe.tips ? `<p><strong>Tip:</strong> ${recipe.tips}</p>` : ''}
            </div>
        `;
    }

    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessage(messageText, 'user');
        userInput.value = ''; // Clear input field
        userInput.style.height = 'auto'; // Reset height
        
        // Extract ingredients from user message
        const newIngredients = extractIngredients(messageText);
        newIngredients.forEach(ingredient => addIngredientTag(ingredient));
        
        // Show typing indicator
        showTypingIndicator();

        try {
            // Include both the message and current ingredient list
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: messageText,
                    ingredients: currentIngredients
                }),
            });

            // Hide typing indicator
            hideTypingIndicator();

            if (!response.ok) {
                const errorData = await response.json();
                addMessage(`Error: ${errorData.error || response.statusText}`, 'bot');
                return;
            }

            const data = await response.json();
            
            // Check if the response includes a formatted recipe
            if (data.recipe) {
                addMessage(formatRecipe(data.recipe), 'bot', true);
            } else {
                addMessage(data.response, 'bot');
            }

        } catch (error) {
            hideTypingIndicator();
            console.error('Error sending message:', error);
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
        }
    }

    // Clear chat history and ingredients
    clearChatButton.addEventListener('click', () => {
        // Remove all messages except the initial greeting
        while (chatBox.children.length > 1) {
            chatBox.removeChild(chatBox.lastChild);
        }
        
        // Clear ingredient tags
        ingredientTags.innerHTML = '';
        currentIngredients = [];
    });

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent newline in textarea
            sendMessage();
        }
    });
}); 