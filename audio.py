import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# We use the same Groq client that powers the text chat!
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Converts a voice note into plain text using Groq's FREE Whisper model.
def transcribe_audio(audio_file_path: str):
    
    # Open the physical audio file and send it to Groq
    with open(audio_file_path, "rb") as audio_file:
        transcription = groq_client.audio.transcriptions.create(
            model="whisper-large-v3", 
            # Force the filename to end in .webm so Groq API doesn't reject it
            file=("voice_note.webm", audio_file.read())
        )
        
    # Return the translated/transcribed text!
    return transcription.text