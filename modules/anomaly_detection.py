import pandas as pd
import numpy as np

def zscore_anomaly(agg_df, threshold=2.5):
    results = []
    for (cluster_id, disease), group in agg_df.groupby(['cluster_id', 'disease']):
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
    return pd.concat(results)

def residual_anomaly(series, threshold=2.0):
    """Rolling-mean based residual anomaly detection (STL substitute)."""
    if len(series) < 4:
        return pd.Series(False, index=series.index)
    rolling_mean = series.rolling(window=3, center=True, min_periods=1).mean()
    residuals = series - rolling_mean
    mad = np.median(np.abs(residuals - np.median(residuals)))
    modified_z = 0.6745 * (residuals - np.median(residuals)) / (mad + 1e-9)
    return np.abs(modified_z) > threshold

def spatial_scan_statistic(agg_df, anomalies_zscore):
    total_cases = agg_df['case_count'].sum()
    results = []
    for _, row in agg_df.iterrows():
        observed = row['case_count']
        expected = total_cases * (observed / total_cases)
        if expected > 0 and observed > 0:
            llr = observed * np.log(observed / expected) - (observed - expected)
        else:
            llr = 0
            
        z_score_matches = anomalies_zscore.loc[
            (anomalies_zscore['cluster_id'] == row['cluster_id']) &
            (anomalies_zscore['disease'] == row['disease']) &
            (anomalies_zscore['time_window'] == row['time_window'])
        ]
        
        z_is_anom = z_score_matches['is_anomaly'].values[0] if len(z_score_matches) > 0 else False
        z_score_val = z_score_matches['z_score'].values[0] if len(z_score_matches) > 0 else np.nan
        res_is_anom = row.get('residual_anomaly', False)
        
        is_anomaly = (llr > 3.84) or z_is_anom or res_is_anom
            
        results.append({
            'cluster_id': row['cluster_id'],
            'disease': row['disease'],
            'time_window': row['time_window'],
            'centroid_lat': row['centroid_lat'],
            'centroid_lon': row['centroid_lon'],
            'case_count': row['case_count'],
            'observed': observed,
            'expected': round(expected, 2),
            'llr': round(llr, 4),
            'is_anomaly': is_anomaly,
            'z_score': z_score_val
        })
    return pd.DataFrame(results)
