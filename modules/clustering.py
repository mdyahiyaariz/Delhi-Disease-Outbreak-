import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

def build_nodes(df):
    nodes = []
    for _, row in df.iterrows():
        true_anom = row.get('is_true_anomaly', False)
        nodes.append({
            'patient_id': row['patient_id'],
            'lat': row['home_lat'],
            'lon': row['home_lon'],
            'disease': row['predicted_disease'],
            'confidence': row['confidence'],
            'location_type': 'home',
            'weight': 0.7,
            'record_date': row['record_date'],
            'is_true_anomaly': true_anom,
        })
        nodes.append({
            'patient_id': row['patient_id'],
            'lat': row['work_lat'],
            'lon': row['work_lon'],
            'disease': row['predicted_disease'],
            'confidence': row['confidence'],
            'location_type': 'work',
            'weight': 0.3,
            'record_date': row['record_date'],
            'is_true_anomaly': true_anom,
        })
    return pd.DataFrame(nodes)

def cluster_by_disease(nodes_df, disease_name, eps_km=1.5, min_samples=3):
    subset = nodes_df[nodes_df['disease'] == disease_name].copy()
    coords = np.radians(subset[['lat', 'lon']].values)
    eps_rad = eps_km / 6371.0
    db = DBSCAN(eps=eps_rad, min_samples=min_samples,
                algorithm='ball_tree', metric='haversine')
    subset['cluster_id'] = db.fit_predict(coords)
    return subset
