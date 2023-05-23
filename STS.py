import whisper
import requests
import os
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
load_dotenv()

def transcribe(audio_file, language):
    model = whisper.load_model("small")
    print("Sending Audio to Whisper...")
    result = model.transcribe(audio_file, language=language)
    return result["text"]

def text_to_speech(text_file):
    try:
        with open(text_file, 'r', encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("AI_response.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    voicevox_api_key = os.getenv('VOICEVOX_API_KEY')
    VOICEVOX_URL=f"https://deprecatedapis.tts.quest/v2/voicevox/audio/?key={voicevox_api_key}&text={text}"
    
    try:
        response = requests.request(
            "POST", VOICEVOX_URL)
         # Handle specific error messages from the API
        if response.text == "invalidApiKey":
            print("Invalid API key provided.")
        elif response.text == "failed":
            print("Synthesis failed.")
        elif response.text == "notEnoughPoints":
            print("Insufficient points.")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        
    print(f'response: {response}')
    wav_bytes = None
    wav_bytes = response.content
    with open("output/audioResponse.wav", "wb") as file:
        file.write(wav_bytes)
        
def audioPlayer(audio_file):
    # Load .wav file
    audio = AudioSegment.from_wav(audio_file)

    # Play the audio file
    play(audio)
    

