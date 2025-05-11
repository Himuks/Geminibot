import os # Added for environment variables
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai # Added for Google Generative AI

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


def get_ai_prediction(prompt_text):
    """
    Function to get a prediction from the Google Generative AI API.
    """
    if not model:
        return "Error: AI model not initialized. Please check API key and configuration."

    try:
        # For next sentence prediction, you might want to frame the prompt accordingly.
        # This is a simple example; you might need a more sophisticated prompt.
        # full_prompt = f"The user has typed the following conversation so far, predict the next sentence from the bot: \\nUser: {prompt_text}\\nBot:"
        # Or simply:
        full_prompt = f"Predict the next sentence or provide a relevant continuation for: \"{prompt_text}\""


        response = model.generate_content(full_prompt)
        
        # Debugging: print the full response object
        # print(f"API Response: {response}")

        if response and response.parts:
            return response.text
        elif response and response.prompt_feedback:
             return f"Blocked by API. Reason: {response.prompt_feedback}"
        else:
            return "Sorry, I couldn't generate a response. The API returned an empty result."

    except Exception as e:
        print(f"Error calling Google Generative AI API: {e}")
        # You might want to inspect `e` for specific API errors.
        # For example, if e contains information about authentication failure.
        if "API_KEY_INVALID" in str(e) or "API_KEY_MISSING" in str(e) or "PERMISSION_DENIED" in str(e):
            return "Sorry, there was an issue with the API key or permissions. Please check the server logs."
        return f"Sorry, an error occurred while contacting the AI: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # In a real app, you'd send more context if needed, not just the last message.
    bot_response = get_ai_prediction(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True) 