import openai
import re
import os
from dotenv import load_dotenv
load_dotenv()

# Load the role file
try:
    with open('AI_role.txt', 'r', encoding='utf-8') as file:
        AI_role = file.read()
except FileNotFoundError:
    print("AI_role.txt not found.")
except Exception as e:
    print(f"An error occurred: {e}")    
AI_role = AI_role.replace('\n', '')

request_message = [
    {"role": "system", "content": AI_role}
]

def get_ai_response(user_input):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key
    
    request_message.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=request_message
        )
    except openai.api_resources.completion.CompletionError as e:
        print(f"An error occurred with the OpenAI API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    ai_response = response['choices'][0]['message']['content']
    print("AI Response:", ai_response)

    with open('output/AI_response.txt', 'w', encoding="utf-8") as file:
        separated_text = separate_sentences(ai_response)
        file.write(separated_text)
        
def separate_sentences(text):
    # Define common sentence-ending punctuation marks
    sentence_enders = re.compile(r'[.!?]+')

    # Replace any newline characters with spaces
    text = text.replace('\n', ' ')

    # Split text into list of strings at each sentence-ending punctuation mark
    sentences = sentence_enders.split(text)

    # Join sentences with newline character
    result = '\n'.join(sentences)

    return result