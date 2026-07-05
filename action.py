# chatbot.py
from database import db
from datetime import datetime

# These functions do the actual work in MongoDB when the AI decides to take action.

#Action 1: RAG - Searches MongoDB for NGOs matching the user's request.
def search_ngos(location: str = "", category: str = ""):
    print(f"AI triggered search: category='{category}', location='{location}'")
    
    query = {}
    if location:
        query["city"] = {"$regex": location, "$options": "i"} 
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
        
    # Find up to 3 matches and pull their data for the AI to read
    results = list(db.Ngos.find(query, {"_id": 1, "name": 1, "description": 1, "city": 1}).limit(3))
    
    if not results:
        return "No NGOs found matching those criteria."
        
    # Convert MongoDB results to a simple string so Llama 3 can read it
    for r in results:
        r["_id"] = str(r["_id"])
        
    return str(results)

 #Action 2: Saves an NGO to the user's favorites collection.
def save_to_favorites(user_id: str, user_name: str, ngo_id: str, ngo_name: str):
    db.Favorites.insert_one({
        "userId": user_id, "userName": user_name, 
        "ngoId": ngo_id, "ngoName": ngo_name, 
        "date": datetime.now()
    })
    return "Successfully saved to favorites."

#Action 3: Books a volunteer visit.
def book_visit(user_id: str, user_name: str, ngo_id: str, ngo_name: str, date : str):
    db.Visits.insert_one({
        "userId": user_id, "userName": user_name, 
        "ngoId": ngo_id, "ngoName": ngo_name, 
        "date": date, "status": "Pending"
    })
    return f"Visit successfully requested for {date}."

#Action 4: Logs a physical donation pledge (clothes, food).
def log_donation_pledge(user_id: str, user_name: str, ngo_id: str, ngo_name: str, items: str):
    db.Pledges.insert_one({
        "userId": user_id, "userName": user_name, 
        "ngoId": ngo_id, "ngoName": ngo_name, 
        "itemsDescription": items
    })
    return "Donation pledge recorded successfully."

#Action 5: Logs a request for the NGO to call the user back.
def request_callback(user_id: str, user_name: str, ngo_id: str, ngo_name: str, phone_number: str):
    db.Callbacks.insert_one({
        "userId": user_id, "userName": user_name, 
        "ngoId": ngo_id, "ngoName": ngo_name, 
        "phoneNumber": phone_number
    })
    return "Callback requested. The NGO will contact you shortly."