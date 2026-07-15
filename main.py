from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender import get_ml_recommendations
from apscheduler.schedulers.background import BackgroundScheduler
from train_model import train_model
import os
from pydantic import BaseModel
from fastapi import UploadFile, File
import shutil
import json
from typing import List, Dict, Any
from chatbot import get_ai_response
from audio import transcribe_audio
from retention import run_retention_analysis

app = FastAPI()

# Add CORS middleware to allow connections from frontend/backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your Vercel and Render URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def start_scheduler():
    should_run = os.getenv("ENABLE_AUTO_TRAINING", "false")
    if should_run.lower() == "true":
        scheduler = BackgroundScheduler()
        # Schedule the math to run every single night at 2:00 AM!
        scheduler.add_job(train_model, 'cron', hour=2, minute=0)
        scheduler.add_job(run_retention_analysis, 'cron', day_of_week='sun', hour=3, minute=0)
        scheduler.start()

@app.get("/")
def home():
    return {"message": "Welcome to the Kind Link ML Engine!"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: str):
    recommendations = get_ml_recommendations(user_id)
    
    if len(recommendations) == 0:
        return {
            "user_id": user_id,
            "status": "fallback",
            "recommendations": []
        }
    else:
        print(f"AI Success! Recommended NGOs for User {user_id}")
        return {
            "user_id": user_id,
            "status": "ai_success",
            "recommendations": recommendations
        }
    
# chatbot

# We need a Pydantic model so FastAPI knows how to read the JSON request
class ChatRequest(BaseModel):
    user_id: str = "guest_123"
    user_name: str = "Guest"
    message: str
    chat_history: List[Dict[str, Any]] = []

@app.post("/chat/text")
def chat_with_bot(request: ChatRequest):
    try:
        print(f" Received text chat from {request.user_name}: {request.message}")
        ai_reply = get_ai_response(request.message, request.user_id, request.user_name, request.chat_history)
        return {"status": "success", "reply": ai_reply}
        
    except Exception as e:
        return {
            "status": "error", 
            "reply": "I am so sorry, but my brain is having trouble connecting to the network right now. Please try again in a moment!"
        }

@app.post("/chat/voice")
async def chat_with_voice(user_id: str = "guest_123", user_name: str = "Guest", chat_history_str: str = "[]", audio_file: UploadFile = File(...)):
    try:
        print(f" Received voice note from {user_name}")
        
        temp_file_path = f"temp_{audio_file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
            
        transcribed_text = transcribe_audio(temp_file_path)
        os.remove(temp_file_path)
        
        chat_history = json.loads(chat_history_str)
        ai_reply = get_ai_response(transcribed_text, user_id, user_name, chat_history)
        
        return {
            "status": "success", 
            "heard_text": transcribed_text, 
            "reply": ai_reply
        }
    except Exception as e:
        print(f" CRITICAL ERROR in /chat/voice: {e}")
        return {
            "status": "error", 
            "reply": "I am so sorry, I couldn't process your voice note right now. Please try typing your message!"
        }