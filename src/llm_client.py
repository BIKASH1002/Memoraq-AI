import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def generate_decision_memo(prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("API Key not found.")

    client = genai.Client(api_key = api_key)

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )

    if not response.text:
        raise ValueError("Empty response returned by model.")
    
    return response.text
