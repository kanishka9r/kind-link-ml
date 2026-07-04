from fastapi import FastAPI
from recommender import get_ml_recommendations

app = FastAPI()

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