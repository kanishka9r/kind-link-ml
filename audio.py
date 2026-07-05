import os
from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Converts a voice note (.wav, .mp3, .m4a) into plain text using OpenAI Whisper.
def transcribe_audio(audio_file_path: str):
    
    # Open the physical audio file and send it to OpenAI
    with open(audio_file_path, "rb") as audio_file:
        transcription = openai_client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        
    # Return the translated/transcribed text!
    return transcription.text