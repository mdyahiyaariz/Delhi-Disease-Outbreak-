"""Alert generation and output persistence."""

from config import OUTPUT_DIR


def generate_alerts(anomalies_df):
    """Generate alerts from anomaly detection results."""
    alerts = anomalies_df[anomalies_df['is_anomaly'] == True].copy()
    return alerts


def save_outputs(spatio_temporal_df, scan_results, ai_results, alerts_df):
    """Save pipeline results to CSV files."""
    spatio_temporal_df.to_csv(OUTPUT_DIR / 'spatio_temporal_data.csv', index=False)
    scan_results.to_csv(OUTPUT_DIR / 'anomaly_results.csv', index=False)
    ai_results.to_csv(OUTPUT_DIR / 'ai_anomaly_results.csv', index=False)
    alerts_df.to_csv(OUTPUT_DIR / 'alerts.csv', index=False)
