"""Anomaly detection methods (statistical and AI-based)."""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from config import (
    ZSCORE_THRESHOLD,
    RESIDUAL_THRESHOLD,
    SPATIAL_SCAN_THRESHOLD,
    AI_N_ESTIMATORS,
    AI_CONTAMINATION,
    AI_RANDOM_STATE,
)


def zscore_anomaly(agg_df, threshold=ZSCORE_THRESHOLD):
    """Detect anomalies using z-score analysis per cluster-disease pair."""
    results = []
    for _, group in agg_df.groupby(['cluster_id', 'disease']):
        group = group.sort_values('time_window').copy()
        mean = group['case_count'].mean()
        std = group['case_count'].std()
        if std == 0 or pd.isna(std):
            group['z_score'] = 0.0
            group['is_anomaly'] = False
        else:
            group['z_score'] = (group['case_count'] - mean) / std
            group['is_anomaly'] = group['z_score'].abs() > threshold
        results.append(group)
    return pd.concat(results, ignore_index=True)


def residual_anomaly(series, threshold=RESIDUAL_THRESHOLD):
    """Detect anomalies using rolling-mean residuals."""
    if len(series) < 4:
        return pd.Series(False, index=series.index)
    rolling_mean = series.rolling(window=3, center=True, min_periods=1).mean()
    residuals = series - rolling_mean
    mad = np.median(np.abs(residuals - np.median(residuals)))
    modified_z = 0.6745 * (residuals - np.median(residuals)) / (mad + 1e-9)
    return np.abs(modified_z) > threshold


def detect_residual_anomalies(agg_df):
    """Apply residual anomaly detection across all cluster-disease pairs."""
    stl_counts = {}
    for (cluster_id, disease), group in agg_df.groupby(['cluster_id', 'disease']):
        ts = group.sort_values('time_window').set_index('time_window')['case_count']
        stl_counts[(cluster_id, disease)] = residual_anomaly(ts).sum()
    return sum(stl_counts.values()), stl_counts


def spatial_scan_statistic(agg_df, anomalies_zscore=None, threshold=SPATIAL_SCAN_THRESHOLD):
    """Detect anomalies using Kulldorff-style spatial scan statistic."""
    if anomalies_zscore is None:
        anomalies_zscore = pd.DataFrame(
            columns=['cluster_id', 'disease', 'time_window', 'z_score']
        )
    scan_df = agg_df.merge(
        anomalies_zscore[['cluster_id', 'disease', 'time_window', 'z_score']],
        on=['cluster_id', 'disease', 'time_window'],
        how='left',
    )
    total_cases = scan_df['case_count'].sum()
    scan_df['expected'] = total_cases * (scan_df['case_count'] / total_cases)
    scan_df['llr'] = scan_df.apply(
        lambda row: row['case_count'] * np.log(row['case_count'] / row['expected'])
        - (row['case_count'] - row['expected'])
        if row['expected'] > 0 and row['case_count'] > 0
        else 0,
        axis=1,
    )
    scan_df['llr'] = scan_df['llr'].round(4)
    scan_df['expected'] = scan_df['expected'].round(2)
    scan_df['is_anomaly'] = scan_df['llr'] > threshold
    return scan_df


def ai_anomaly_detection(
    agg_df,
    n_estimators=AI_N_ESTIMATORS,
    contamination=AI_CONTAMINATION,
    random_state=AI_RANDOM_STATE,
):
    """Detect anomalies using Isolation Forest machine learning model."""
    features = agg_df.copy()
    features['time_window_start'] = features['time_window'].dt.to_timestamp()
    features['week_of_year'] = features['time_window_start'].dt.isocalendar().week
    features['month'] = features['time_window_start'].dt.month
    disease_dummies = pd.get_dummies(features['disease'], prefix='disease')
    features = pd.concat([features, disease_dummies], axis=1)
    feature_cols = [
        'case_count',
        'avg_confidence',
        'weighted_count',
        'week_of_year',
        'month',
        'centroid_lat',
        'centroid_lon',
    ] + disease_dummies.columns.tolist()
    model_data = features[feature_cols].fillna(0)
    clf = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=random_state,
    )
    clf.fit(model_data)
    results = features[
        ['cluster_id', 'disease', 'time_window', 'centroid_lat', 'centroid_lon', 'case_count']
    ].copy()
    results['ai_score'] = -clf.decision_function(model_data)
    results['ai_anomaly'] = clf.predict(model_data) == -1
    return results
