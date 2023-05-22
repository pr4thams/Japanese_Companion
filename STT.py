import whisper

def transcribe(audio_file, language):
    model = whisper.load_model("small")
    result = model.transcribe(audio_file, language=language)
    return result["text"]

