"""Data generation and node building functions."""

import numpy as np
import pandas as pd
from datetime import timedelta

from config import DISEASES, DISEASE_CLUSTERS, START_DATE, SEED, NOISE_COUNT


def generate_cluster(center_lat, center_lon, n, spread=0.01):
    """Generate random cluster of coordinates around a center point."""
    return np.random.normal(center_lat, spread, n), np.random.normal(center_lon, spread, n)


def generate_synthetic_data(seed=SEED, noise_count=NOISE_COUNT):
    """Generate synthetic patient records for disease outbreak simulation."""
    np.random.seed(seed)
    records = []
    patient_id = 1

    for disease, centers in DISEASE_CLUSTERS.items():
        for center in centers:
            cluster_size = np.random.randint(25, 50)
            home_lats, home_lons = generate_cluster(*center, cluster_size)
            work_lats, work_lons = generate_cluster(
                center[0] + np.random.uniform(-0.05, 0.05),
                center[1] + np.random.uniform(-0.05, 0.05),
                cluster_size,
                spread=0.02,
            )
            for i in range(cluster_size):
                week_offset = np.random.randint(0, 20)
                if disease == 'Dengue' and week_offset in range(8, 11):
                    week_offset = np.random.choice(range(8, 11), p=[0.4, 0.4, 0.2])
                record_date = START_DATE + timedelta(
                    weeks=int(week_offset), days=np.random.randint(0, 7)
                )
                records.append({
                    'patient_id': f'P{patient_id:04d}',
                    'home_lat': home_lats[i],
                    'home_lon': home_lons[i],
                    'work_lat': work_lats[i],
                    'work_lon': work_lons[i],
                    'predicted_disease': disease,
                    'confidence': round(np.random.uniform(0.65, 0.99), 2),
                    'record_date': record_date.strftime('%Y-%m-%d'),
                })
                patient_id += 1

    # Add noise patients
    for _ in range(noise_count):
        disease = np.random.choice(DISEASES)
        records.append({
            'patient_id': f'P{patient_id:04d}',
            'home_lat': np.random.uniform(28.55, 28.70),
            'home_lon': np.random.uniform(77.15, 77.30),
            'work_lat': np.random.uniform(28.55, 28.70),
            'work_lon': np.random.uniform(77.15, 77.30),
            'predicted_disease': disease,
            'confidence': round(np.random.uniform(0.50, 0.80), 2),
            'record_date': (
                START_DATE + timedelta(days=np.random.randint(0, 140))
            ).strftime('%Y-%m-%d'),
        })
        patient_id += 1

    return pd.DataFrame(records)


def build_nodes(patient_df):
    """Build spatial node graph from patient home and work locations."""
    nodes = []
    for _, row in patient_df.iterrows():
        nodes.append({
            'patient_id': row['patient_id'],
            'lat': row['home_lat'],
            'lon': row['home_lon'],
            'disease': row['predicted_disease'],
            'confidence': row['confidence'],
            'location_type': 'home',
            'weight': 0.7,
            'record_date': row['record_date'],
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
        })
    return pd.DataFrame(nodes)
