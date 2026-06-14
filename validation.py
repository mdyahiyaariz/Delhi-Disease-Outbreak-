"""Map structure validation functions."""


def validate_map_data(clustered_df, anomalies_df, disease_name):
    """Validate and summarize map data for a given disease."""
    subset = clustered_df[clustered_df['disease'] == disease_name]
    markers = anomalies_df[anomalies_df['disease'] == disease_name]
    return {
        'disease': disease_name,
        'heatmap_points': len(subset),
        'map_center': [subset['lat'].mean(), subset['lon'].mean()],
        'total_markers': len(markers),
        'anomaly_markers': (
            int(markers['is_anomaly'].sum()) if 'is_anomaly' in markers else 0
        ),
        'normal_markers': (
            int((~markers['is_anomaly']).sum())
            if 'is_anomaly' in markers
            else len(markers)
        ),
    }
