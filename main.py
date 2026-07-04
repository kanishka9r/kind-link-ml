from fastapi import FastAPI
from recommender import get_ml_recommendations
from apscheduler.schedulers.background import BackgroundScheduler
from train_model import train_model
import os


app = FastAPI()

@app.on_event("startup")
def start_scheduler():
    should_run = os.getenv("ENABLE_AUTO_TRAINING", "false")
    if should_run.lower() == "true":
        scheduler = BackgroundScheduler()
        # Schedule the math to run every single night at 2:00 AM!
        scheduler.add_job(train_model, 'cron', hour=2, minute=0)
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