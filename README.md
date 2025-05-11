# Gemini Next Sentence Prediction Chatbot (Skeleton)

This is a basic web application skeleton for a chatbot that aims to use Gemini for next sentence prediction. It includes a Flask backend and a simple HTML/CSS/JavaScript frontend.

**Note:** The actual Gemini API integration is not implemented. A placeholder function in `app.py` simulates the AI responses.

## Project Structure

```
/
|-- app.py               # Flask backend logic
|-- templates/
|   |-- index.html       # HTML for the chat interface
|-- static/
|   |-- style.css        # CSS for styling
|   |-- script.js        # JavaScript for frontend logic
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

3.  **Run the Flask application:**
    ```bash
    python app.py
    ```

4.  Open your web browser and go to `http://127.0.0.1:5000/`.

## Gemini Integration

To connect this chatbot to the actual Gemini API:

1.  You'll need to sign up for API access with Google and get an API key.
2.  Install the `google-generativeai` Python library:
    ```bash
    pip install google-generativeai
    ```
3.  Modify the `get_gemini_prediction(prompt_text)` function in `app.py` to use the Gemini API. You will need to handle API key management securely.
    Refer to the official Google Generative AI SDK documentation for details on how to make API calls. 