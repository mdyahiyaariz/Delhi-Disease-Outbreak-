"""Main outbreak detection pipeline orchestrator."""

import numpy as np

from config import DISEASES
from data_generation import generate_synthetic_data, build_nodes
from spatial import cluster_by_disease
from aggregation import aggregate_spatio_temporal
from detection import (
    zscore_anomaly,
    detect_residual_anomalies,
    spatial_scan_statistic,
    ai_anomaly_detection,
)
from validation import validate_map_data
from alerts import generate_alerts, save_outputs
from utils import print_header, print_summary, format_alert


def run_pipeline():
    """Execute the complete outbreak detection pipeline."""
    print_header('GENERATING SYNTHETIC PATIENT DATA')
    patient_df = generate_synthetic_data()
    print(f'✅ Generated {len(patient_df)} patient records')
    print(f'   Diseases: {patient_df["predicted_disease"].value_counts().to_dict()}')
    print(f'   Date range: {patient_df["record_date"].min()} → {patient_df["record_date"].max()}\n')

    print_header('STEP 1: BUILD NODE STRUCTURE')
    nodes_df = build_nodes(patient_df)
    print(f'✅ Nodes created: {len(nodes_df)} (2× patients)')
    print(f'   Home nodes: {(nodes_df["location_type"] == "home").sum()}')
    print(f'   Work nodes: {(nodes_df["location_type"] == "work").sum()}\n')

    print_header('STEP 2: GEO-CLUSTERING WITH DBSCAN')
    clustered_dfs = {}
    for disease in nodes_df['disease'].unique():
        clustered_dfs[disease] = cluster_by_disease(nodes_df, disease)
        cdf = clustered_dfs[disease]
        n_clusters = cdf['cluster_id'].nunique() - (1 if -1 in cdf['cluster_id'].values else 0)
        noise = (cdf['cluster_id'] == -1).sum()
        print(f'   {disease}: {n_clusters} clusters found, {noise} noise points')
    print('✅ DBSCAN clustering complete\n')

    print_header('STEP 3: SPATIO-TEMPORAL AGGREGATION (Weekly)')
    spatio_temporal_df = aggregate_spatio_temporal(clustered_dfs)
    print(f'✅ Aggregated {len(spatio_temporal_df)} cluster-week records')
    print(f'   Diseases covered: {spatio_temporal_df["disease"].unique().tolist()}')
    print(f'   Cluster IDs: {sorted(spatio_temporal_df["cluster_id"].unique().tolist())}\n')

    print_header('STEP 4a: Z-SCORE ANOMALY DETECTION')
    anomalies_zscore = zscore_anomaly(spatio_temporal_df)
    zscore_count = anomalies_zscore['is_anomaly'].sum()
    print(f'✅ Z-score analysis complete')
    print(f'   Total windows analyzed: {len(anomalies_zscore)}')
    print(f'   Anomalies detected: {zscore_count}')
    if zscore_count > 0:
        top = anomalies_zscore[anomalies_zscore['is_anomaly']].nlargest(3, 'z_score')[
            ['disease', 'cluster_id', 'time_window', 'case_count', 'z_score']
        ]
        print(f'   Top anomalies:\n{top.to_string(index=False)}\n')
    else:
        print()

    print_header('STEP 4b: RESIDUAL ANOMALY DETECTION (numpy, replaces STL)')
    total_stl, stl_flags = detect_residual_anomalies(spatio_temporal_df)
    print(f'✅ Residual anomaly detection complete')
    print(f'   Anomalous time windows: {total_stl}')
    top_stl = sorted(stl_flags.items(), key=lambda item: -item[1])[:3]
    for (cid, dis), count in top_stl:
        if count > 0:
            print(f'   Cluster {cid} [{dis}]: {count} anomalous weeks')
    print()

    print_header('STEP 4c: SPATIAL SCAN STATISTIC (Kulldorff-style)')
    scan_results = spatial_scan_statistic(spatio_temporal_df, anomalies_zscore)
    scan_anomalies = scan_results[scan_results['is_anomaly']]
    print(f'✅ Spatial scan complete')
    print(f'   Records scanned: {len(scan_results)}')
    print(f'   Spatial anomalies flagged: {len(scan_anomalies)}\n')

    print_header('STEP 4d: AI-BASED ANOMALY DETECTION')
    ai_results = ai_anomaly_detection(spatio_temporal_df)
    ai_anomalies = ai_results[ai_results['ai_anomaly']]
    print(f'✅ AI-based anomaly detection complete')
    print(f'   AI anomalies flagged: {len(ai_anomalies)}')
    if len(ai_anomalies) > 0:
        print('   Top AI anomalies:')
        print(
            ai_anomalies.sort_values('ai_score', ascending=False).head(3)[
                ['disease', 'cluster_id', 'time_window', 'case_count', 'ai_score']
            ].to_string(index=False)
        )
    print()

    print_header('STEP 5: MAP STRUCTURE VALIDATION')
    for disease in DISEASES:
        result = validate_map_data(clustered_dfs[disease], scan_results, disease)
        print(
            f'   {disease}: {result["heatmap_points"]} heatmap pts | '
            f'{result["anomaly_markers"]} 🔴 anomaly markers | '
            f'{result["normal_markers"]} 🔵 normal markers | '
            f'center {result["map_center"][0]:.3f}, {result["map_center"][1]:.3f}'
        )
    print('✅ Map structure validated (folium rendering skipped — not installed)\n')

    print_header('STEP 6: ALERT GENERATION')
    alerts = generate_alerts(scan_anomalies)
    if alerts.empty:
        print('   ℹ️  No alerts to generate.')
    else:
        for _, alert in alerts.iterrows():
            print(format_alert(alert))
    print(f'\n✅ {len(alerts)} alert(s) generated')

    save_outputs(spatio_temporal_df, scan_results, ai_results, alerts)
    print_summary({
        'Total patients': len(patient_df),
        'Total nodes': len(nodes_df),
        'Diseases tracked': len(DISEASES),
        'Cluster-week records': len(spatio_temporal_df),
        'Z-score anomalies': int(zscore_count),
        'Residual anomalies': total_stl,
        'Spatial scan anomalies': len(scan_anomalies),
        'AI anomalies': int(ai_results['ai_anomaly'].sum()),
        'Alerts generated': len(alerts),
    })
    print('\n✅ Outputs saved:')
    print('   - spatio_temporal_data.csv')
    print('   - anomaly_results.csv')
    print('   - ai_anomaly_results.csv')
    print('   - alerts.csv')
