import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

RETRYABLE_STATUS_CODES = {429, 503}


def generate_decision_memo(prompt, max_retries = 2, on_retry = None,):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("API Key not found.")

    client = genai.Client(api_key = api_key)

    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model = "gemini-2.5-flash",
                contents = prompt
            )
            break
        except APIError as error:
            if error.code not in RETRYABLE_STATUS_CODES or attempt == max_retries:
                raise

            delay = 2 ** attempt
            if on_retry:
                on_retry(attempt + 1, max_retries, delay)
            time.sleep(delay)

    if not response.text:
        raise ValueError("Empty response returned by model.")
    
    return response.text
