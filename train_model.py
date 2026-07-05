# train_model.py
import pandas as pd
from sklearn.decomposition import TruncatedSVD
import joblib
from database import db

def train_model():
    
    # 1. fetch data from the 'Interactions' collection
    interactions_cursor = db.interactions.find({}, {"_id": 0, "userId": 1, "ngoId": 1, "action": 1})

    df = pd.DataFrame(list(interactions_cursor))
    if df.empty:
        #rule based
        return
    
    action_weights = {
        "view": 1,
        "like": 5,
        "donate": 8
    }

    df['weight'] = df['action'].map(action_weights).fillna(0)
    
     # 2. create the user-item matrix
    user_item_matrix = df.pivot_table(index='userId', columns='ngoId', values='weight', fill_value=0 , aggfunc = 'sum')
    num_components = min(20, len(user_item_matrix.columns) - 1)
    
    if num_components < 1:
        #rule based
        return
    
     # 3. train
    svd = TruncatedSVD(n_components=num_components)
    matrix_factorization_model = svd.fit(user_item_matrix)
    
    # 4. save
    model_data = {
        "svd_model": matrix_factorization_model,
        "ngo_ids": user_item_matrix.columns.tolist(),
        "user_ids": user_item_matrix.index.tolist(), # ADDED THIS
        "matrix": user_item_matrix
    }
    
    # joblib saves the python objects into a physical file on your hard drive
    joblib.dump(model_data, "model.pkl")

if __name__ == "__main__":
    train_model()