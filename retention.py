import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from database import db
import requests

def run_retention_analysis():
    interactions_cursor = db.interactions.find({}, {"_id": 0, "userId": 1, "timestamp": 1})
    df = pd.DataFrame(list(interactions_cursor))

    if df.empty:
        return[]
    
    # Convert timestamp to datetime
    df['timestamp']  = pd.to_datetime(df['timestamp'])
    current_time = datetime.now()

    last_interaction = df.groupby('userId')['timestamp'].max()
    frequency = df.groupby('userId').size()

    rfm_df = pd.DataFrame({
    'Recency': (current_time - last_interaction).dt.days,
    'Frequency': frequency
}).reset_index()
    
    if len(rfm_df) < 3:
        return[]
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(rfm_df[['Recency', 'Frequency']])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    rfm_df['Cluster'] = kmeans.fit_predict(scaled_features)

    cluster_means = rfm_df.groupby('Cluster')['Recency'].mean().sort_values()

    loyal_cluster = cluster_means.index[0]
    at_risk_cluster = cluster_means.index[1] if len(cluster_means) > 1 else None
    churned_cluster = cluster_means.index[2] if len(cluster_means) > 2 else None

    def assign_label(cluster_id):
        if cluster_id == loyal_cluster:
            return "Loyal"
        elif cluster_id == at_risk_cluster:
            return "At Risk"
        else:
            return "Churned"
        
    rfm_df['Status'] = rfm_df['Cluster'].apply(assign_label)   
    
    at_risk_users = rfm_df[rfm_df['Status'] == 'At Risk']

    at_risk_user_ids = [str(uid) for uid in at_risk_users['userId'].tolist()]

    if at_risk_user_ids:
        try:
            # To send mails
            response = requests.post(
                "http://localhost:5000/api/retention/trigger-emails", 
                json={"at_risk_users": at_risk_user_ids}
            )
            if response.status_code == 200:
                print(" Emails successfully triggered via Node.js!")
            else:
                print(f" Node.js failed to send emails: {response.status_code}")
        except Exception as e:
            print(f" Failed to connect to Node.js backend: {e}")


if __name__ == "__main__":
       run_retention_analysis()