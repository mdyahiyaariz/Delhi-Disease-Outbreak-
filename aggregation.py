"""Spatio-temporal aggregation functions."""

import pandas as pd


def aggregate_clusters(clustered_df, timestamp_col='record_date', freq='W'):
    """Aggregate patient data by cluster and time window."""
    df = clustered_df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df['time_window'] = df[timestamp_col].dt.to_period(freq)
    agg = df.groupby(['cluster_id', 'time_window', 'disease']).agg(
        case_count=('patient_id', 'count'),
        avg_confidence=('confidence', 'mean'),
        centroid_lat=('lat', 'mean'),
        centroid_lon=('lon', 'mean'),
        weighted_count=('weight', 'sum'),
    ).reset_index()
    return agg[agg['cluster_id'] != -1]


def aggregate_spatio_temporal(clustered_dfs):
    """Combine aggregations from all disease clusters."""
    records = [aggregate_clusters(df) for df in clustered_dfs.values()]
    return pd.concat(records, ignore_index=True)
