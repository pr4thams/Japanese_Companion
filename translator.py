import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

def translate(text, target_lang):
    # Get the API key from environment variable
    deepl_api_key = os.getenv('DEEPL_API_KEY')

    # Define the API URL and headers
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {deepl_api_key}"
    }

    # Define the data to be sent in the request body
    data = {
        "text": text,
        "target_lang": target_lang
    }

    # Send the POST request
    print("Sending text To DeepL...")
    response = requests.post(url, headers=headers, data=data)

    # Check the response status code
    if response.status_code != 200:
        raise Exception(f"DeepL API request failed with status code {response.status_code}.")

    # Parse the response JSON
    response_json = response.json()

    # Extract the translated text from the response
    translated_text = response_json['translations'][0]['text']
    
    # Return the translated text
    return translated_text

