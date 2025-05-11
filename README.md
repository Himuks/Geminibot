# Cooking Assistant Chatbot

A modern web application chatbot that helps users create recipes with ingredients they have on hand. The chatbot provides recipe suggestions, cooking guidance, and ingredient substitutions using Google's Gemini AI.

![Cooking Assistant Preview](https://images.unsplash.com/photo-1556911220-e15b29be8c8f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80)

## Features

- **Ingredient Management**: Automatically detects and tracks ingredients mentioned in user messages
- **Recipe Suggestions**: Matches available ingredients to possible recipes
- **Step-by-Step Cooking Instructions**: Provides detailed cooking guidance
- **Substitution Ideas**: Suggests alternatives for missing ingredients
- **Modern UI**: Clean, responsive interface with animations and intuitive design
- **Visual Recipe Cards**: Displays formatted recipes with ingredients, steps, and cooking times

## Project Structure

```
/
|-- app.py               # Flask backend with recipe matching and AI integration
|-- templates/
|   |-- index.html       # HTML for the cooking assistant interface
|-- static/
|   |-- style.css        # CSS with cooking-themed styling
|   |-- script.js        # JavaScript for ingredient tracking and UI interactions
|-- requirements.txt     # Python dependencies
|-- README.md            # This file
```

## Setup and Running

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the Google Generative AI API key:**
    ```bash
    # On Linux/macOS
    export GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY'
    
    # On Windows Command Prompt
    set GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY'
    
    # On Windows PowerShell
    $env:GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY'
    ```

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```

5.  Open your web browser and go to `http://127.0.0.1:5000/`.

## How to Use

1. **Enter your ingredients**: Type "I have eggs, cheese, and spinach" (or whatever ingredients you have)
2. **Ask for suggestions**: The assistant will suggest recipes using those ingredients
3. **Get cooking guidance**: Ask specific cooking questions like "How do I make an omelette?"
4. **Request substitutions**: Ask "What can I use instead of butter?"

## Google Generative AI Integration

This chatbot is designed to work with Google's Gemini AI. To ensure proper functioning:

1. Sign up for API access with Google and get an API key
2. Set the API key as an environment variable as shown in the setup section
3. The chatbot uses the `gemini-1.5-flash` model by default, but you can change this in `app.py`

Even without an API key, the application will work with a limited set of sample recipes and responses.

## Example Interaction

**User**: I have eggs, butter, cheese, and spinach.

**Assistant**: *[Creates ingredient tags for eggs, butter, cheese, and spinach]*

**User**: What can I make?

**Assistant**: *[Displays a recipe card for a spinach and cheese omelette with ingredients, steps, and cooking time]*

## Customization

You can expand the sample recipes in `app.py` or modify the interface styling in `style.css` to match your preferences. The application is designed to be easily customizable. 