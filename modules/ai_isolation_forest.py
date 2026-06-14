import pandas as pd
from sklearn.ensemble import IsolationForest

def isolation_forest_anomaly(spatio_temporal_df, contamination=0.05):
    """
    Detect anomalies using Isolation Forest on spatio-temporal data.
    Features used: centroid_lat, centroid_lon, case_count.
    """
    results = spatio_temporal_df.copy()
    results['if_anomaly'] = False
    
    if len(results) < 5:
        return results

    # Normalize features for better performance
    features = results[['centroid_lat', 'centroid_lon', 'case_count']].copy()
    for col in features.columns:
        if features[col].std() > 0:
            features[col] = (features[col] - features[col].mean()) / features[col].std()
        else:
            features[col] = 0.0
            
    # Train Isolation Forest
    model = IsolationForest(contamination=contamination, random_state=42)
    preds = model.fit_predict(features)
    
    # -1 indicates anomaly, 1 indicates normal
    results['if_anomaly'] = (preds == -1)
    
    return results
