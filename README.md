# Kind-Link ML Engine

This repository powers the "brain" behind the **Kind-Link** platform. It acts as the intelligent backend that helps connect passionate volunteers and donors with NGOs that match their interests and location. 

## Features
- **Smart NGO Recommendations**: Instead of generic lists, the system learns from what users like, view, and donate to. It then suggests personalized NGOs that are a perfect match for them, similar to how Netflix recommends movies.
- **AI Chatbot Assistant**: A friendly conversational assistant built right into the platform. Users can chat with it to discover NGOs, schedule volunteer visits, or log donation pledges effortlessly.
- **Voice Interactions**: Not in the mood to type? Users can record voice notes, and the system will automatically transcribe them and chat back naturally.
- **Automated Retention System**: Keeps the community active by analyzing user behavior and sending gentle, automated reminder emails to users who haven't engaged in a while.
- **Self-Learning Capabilities**: The recommendation engine isn't static. It automatically wakes up every night to retrain itself on new user data, ensuring suggestions keep getting smarter over time.

## Tech Stack
- **Framework**: FastAPI (Python)
- **Database**: MongoDB (PyMongo)
- **AI/LLM**: Groq API
- **Machine Learning**: Scikit-Learn, Pandas

## Setup & Run Locally

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI="your_mongodb_atlas_connection_string"
   GROQ_API_KEY="your_groq_api_key"
   ENABLE_AUTO_TRAINING=true
   ```

3. **Start the Server**
   ```bash
   uvicorn main:app --reload
   ```
   The server will run at `http://127.0.0.1:8000`.

## Deployment
This service is configured to be easily deployable on platforms like **Render** as a Python Web Service.
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
