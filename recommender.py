import joblib
import pandas as pd
import os

def get_ml_recommendations(target_user_id):
    # 1. Check if the model file even exists
    if not os.path.exists("model.pkl"):
        return [] # Returns empty array, triggers Node.js Rule-Based fallback
        
    try:
        # 2. Load the brain
        model_data = joblib.load("model.pkl")
        svd = model_data["svd_model"]
        ngo_ids = model_data["ngo_ids"]
        user_ids = model_data["user_ids"]
        matrix = model_data["matrix"]
        
        # 3. Check if the user is in our dataset (cold start check)
        if target_user_id not in user_ids:
            return [] # Returns empty array, triggers Node.js Rule-Based fallback
            
        # 4. we reconstruct the matrix using SVD to get the predicted scores for every NGO
        user_index = user_ids.index(target_user_id)
        user_row = matrix.iloc[user_index].values.reshape(1, -1)
        predicted_scores = svd.inverse_transform(svd.transform(user_row))[0]
        
        # 5. Create a list of NGOs and their predicted scores
        ngo_scores = []
        for i in range(len(ngo_ids)):
            # Don't recommend NGOs they have already interacted with!
            if user_row[0][i] == 0: 
                ngo_scores.append({"ngoId": ngo_ids[i], "score": predicted_scores[i]})
                
        # 6. Sort to find the Top 5
        ngo_scores.sort(key=lambda x: x["score"], reverse=True)
        top_5 = ngo_scores[:5]
        
        # 7. Extract just the IDs to send back
        recommended_ngo_ids = []
        for item in top_5:
            recommended_ngo_ids.append(item["ngoId"])
        return recommended_ngo_ids
        
    except Exception as e:
        print(f"Error in ML Engine: {e}")
        return [] # Returns empty array, triggers Node.js Rule-Based fallback