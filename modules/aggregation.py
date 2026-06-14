import pandas as pd

def aggregate_clusters(clustered_df, timestamp_col='record_date', freq='W'):
    clustered_df = clustered_df.copy()
    clustered_df[timestamp_col] = pd.to_datetime(clustered_df[timestamp_col])
    clustered_df['time_window'] = clustered_df[timestamp_col].dt.to_period(freq)

    # Build aggregation dict dynamically so is_true_anomaly is handled at runtime
    agg_dict = {
        'case_count': ('patient_id', 'count'),
        'avg_confidence': ('confidence', 'mean'),
        'centroid_lat': ('lat', 'mean'),
        'centroid_lon': ('lon', 'mean'),
        'weighted_count': ('weight', 'sum'),
    }
    if 'is_true_anomaly' in clustered_df.columns:
        agg_dict['is_true_anomaly'] = ('is_true_anomaly', 'any')

    agg = clustered_df.groupby(['cluster_id', 'time_window', 'disease']).agg(**agg_dict).reset_index()

    # If no ground-truth column existed, add it as all-False
    if 'is_true_anomaly' not in agg.columns:
        agg['is_true_anomaly'] = False

    agg = agg[agg['cluster_id'] != -1]
    return agg
