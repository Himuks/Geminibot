import os # Added for environment variables
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai # Added for Google Generative AI
import json
import random
import re

app = Flask(__name__)

# --- Google Generative AI API Integration ---
# IMPORTANT: Store your API key securely. Using an environment variable is recommended.
# Example: Set an environment variable named GOOGLE_API_KEY with your key.
# In your terminal:
# export GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY' (on Linux/macOS)
# set GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY' (on Windows Command Prompt)
# $env:GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY' (on Windows PowerShell)

try:
    # Attempt to get the API key from an environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        # Fallback for local testing if environment variable is not set
        # WARNING: Do NOT commit your API key directly into your code for production or shared repositories!
        # print("WARNING: GOOGLE_API_KEY environment variable not found. Using placeholder (will fail).")
        # print("Please set the GOOGLE_API_KEY environment variable with your actual API key.")
        # api_key = "AIzaSyC2uech1aUixZNYQG8dc8jVp-Goy7Cqhf0" # Replace with your key ONLY for temporary local testing if needed
                                 # and ensure it's not committed.
        raise ValueError("ERROR: GOOGLE_API_KEY environment variable not set. "
                         "The application cannot start without a valid API key. "
                         "Please set this environment variable in your production environment.")

    genai.configure(api_key=api_key)

    # Create the model
    # See https://ai.google.dev/gemini-api/docs/models/gemini for model names
    model = genai.GenerativeModel(model_name='gemini-1.5-flash') # Or another suitable model

except Exception as e:
    print(f"Error configuring Google Generative AI API: {e}")
    print("The application might not work correctly if the API is not configured.")
    model = None
# --- End Google Generative AI API Integration ---

# Sample recipes database (in a real app, this would be a proper database)
sample_recipes = [
    {
        "name": "Quick Pasta Primavera",
        "ingredients": ["pasta", "olive oil", "garlic", "bell peppers", "zucchini", "cherry tomatoes", "parmesan cheese", "basil"],
        "steps": [
            "Cook pasta according to package directions.",
            "Heat olive oil in a large skillet over medium heat.",
            "Add minced garlic and sauté until fragrant, about 30 seconds.",
            "Add sliced bell peppers and zucchini, cook for 3-4 minutes until slightly softened.",
            "Add halved cherry tomatoes and cook for another 2 minutes.",
            "Drain pasta and add to the skillet with vegetables.",
            "Toss with grated parmesan cheese and torn basil leaves.",
            "Season with salt and pepper to taste."
        ],
        "time": 20,
        "difficulty": "Easy",
        "tips": "You can use any vegetables you have on hand."
    },
    {
        "name": "Simple Omelette",
        "ingredients": ["eggs", "butter", "salt", "pepper", "cheese"],
        "steps": [
            "Whisk eggs in a bowl with a pinch of salt and pepper.",
            "Melt butter in a non-stick pan over medium heat.",
            "Pour in egg mixture and let it cook until edges begin to set.",
            "Sprinkle cheese over half of the omelette.",
            "Using a spatula, fold the omelette in half.",
            "Cook for another minute, then slide onto a plate."
        ],
        "time": 10,
        "difficulty": "Easy",
        "tips": "Add any fillings you like - ham, mushrooms, spinach, etc."
    },
    {
        "name": "Chicken Stir Fry",
        "ingredients": ["chicken breast", "soy sauce", "garlic", "ginger", "bell peppers", "broccoli", "carrots", "vegetable oil", "rice"],
        "steps": [
            "Cut chicken into bite-sized pieces and marinate in soy sauce for 10 minutes.",
            "Prepare rice according to package instructions.",
            "Heat oil in a wok or large pan over high heat.",
            "Add minced garlic and ginger, stir for 30 seconds.",
            "Add chicken and cook until no longer pink, about 5-6 minutes.",
            "Add chopped vegetables and stir-fry for 3-4 minutes until crisp-tender.",
            "Add a splash more soy sauce if needed.",
            "Serve hot over rice."
        ],
        "time": 25,
        "difficulty": "Medium",
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
    }
]

def clean_markdown_formatting(text):
    """Remove markdown formatting like ** for bold and * for italic"""
    # Replace markdown bold with plain text
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Replace markdown italic with plain text
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text

def get_cooking_response(message, ingredients=None):
    """
    Generate a cooking-related response based on user message and ingredients.
    In a production app, this would use the AI model to generate actual responses.
    """
    if not model:
        return {"response": "Error: AI model not initialized. Please check API key and configuration."}

    try:
        # First, check if we should return a recipe based on ingredients
        if ingredients and len(ingredients) >= 2:
            # In a real app, you'd use the AI to find or generate a matching recipe
            # For this demo, we'll use a simple matching algorithm with our sample recipes
            recipe = find_matching_recipe(ingredients)
            
            if recipe:
                return {"recipe": recipe}
        
        # For general cooking inquiries
        prompt = create_cooking_prompt(message, ingredients)
        response = model.generate_content(prompt)
        
        # If we get a valid response from the model
        if response and response.parts:
            # Clean any markdown formatting from the AI response
            cleaned_response = clean_markdown_formatting(response.text)
            return {"response": cleaned_response}
        elif response and response.prompt_feedback:
            return {"response": f"Blocked by API. Reason: {response.prompt_feedback}"}
        else:
            # Fallback responses if no AI response
            fallbacks = [
                "I'd recommend looking up recipes that use those ingredients, perhaps something like a simple stir-fry or pasta dish.",
                "Those ingredients could work well in a salad or quick sauté.",
                "Have you considered making a soup or stew with those ingredients?",
                "You might try roasting some of those vegetables and serving with a simple protein."
            ]
            return {"response": random.choice(fallbacks)}

    except Exception as e:
        print(f"Error calling Google Generative AI API: {e}")
        return {"response": f"Sorry, I couldn't generate a recipe suggestion right now: {e}"}

def create_cooking_prompt(message, ingredients=None):
    """Create a prompt for the cooking assistant."""
    base_prompt = "You are a helpful cooking assistant that helps users create meals with the ingredients they have."
    
    if ingredients and len(ingredients) > 0:
        ingredient_list = ", ".join(ingredients)
        prompt = f"{base_prompt}\n\nThe user has the following ingredients: {ingredient_list}\n\nUser message: {message}\n\nProvide a helpful response about cooking with these ingredients. If they're asking for a recipe, suggest a dish that can be made with these ingredients or suggest substitutions for missing ingredients."
    else:
        prompt = f"{base_prompt}\n\nUser message: {message}\n\nProvide a helpful response about cooking."
    
    return prompt

def find_matching_recipe(ingredients):
    """
    Find a recipe that matches the user's ingredients.
    In a real app, this would be more sophisticated, using AI or a proper algorithm.
    """
    # Convert all ingredients to lowercase for case-insensitive matching
    user_ingredients = [ing.lower() for ing in ingredients]
    
    best_match = None
    highest_match_count = 1  # Require at least 2 matching ingredients
    
    for recipe in sample_recipes:
        recipe_ingredients = [ing.lower() for ing in recipe["ingredients"]]
        
        # Count how many user ingredients are in this recipe
        match_count = sum(1 for ing in user_ingredients if any(ing in r_ing for r_ing in recipe_ingredients))
        
        if match_count > highest_match_count:
            highest_match_count = match_count
            best_match = recipe
    
    return best_match

def get_substitution_suggestion(ingredient):
    """
    Get substitution suggestions for a missing ingredient.
    In a real app, this would use the AI model to generate proper substitutions.
    """
    substitutions = {
        "butter": ["olive oil", "coconut oil", "margarine"],
        "milk": ["almond milk", "soy milk", "oat milk", "coconut milk"],
        "eggs": ["applesauce", "mashed banana", "flax seeds mixed with water"],
        "flour": ["almond flour", "coconut flour", "oat flour", "gluten-free flour blend"],
        "sugar": ["honey", "maple syrup", "agave nectar", "stevia"],
        "soy sauce": ["tamari", "coconut aminos", "Worcestershire sauce"],
        "rice": ["quinoa", "cauliflower rice", "bulgur", "couscous"],
        "pasta": ["zucchini noodles", "spaghetti squash", "rice noodles", "bean pasta"]
    }
    
    for key, options in substitutions.items():
        if key in ingredient.lower():
            return options
    
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_message = data.get('message', '')
    ingredients = data.get('ingredients', [])
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response = get_cooking_response(user_message, ingredients)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True) 