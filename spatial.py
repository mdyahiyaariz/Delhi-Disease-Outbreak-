"""Spatial clustering and processing functions."""

import numpy as np
from sklearn.cluster import DBSCAN

from config import DBSCAN_EPS_KM, DBSCAN_MIN_SAMPLES


def cluster_by_disease(nodes_df, disease_name, eps_km=DBSCAN_EPS_KM, min_samples=DBSCAN_MIN_SAMPLES):
    """Cluster patient locations by disease using DBSCAN with haversine distance."""
    subset = nodes_df[nodes_df['disease'] == disease_name].copy()
    coords = np.radians(subset[['lat', 'lon']].values)
    eps_rad = eps_km / 6371.0
    db = DBSCAN(
        eps=eps_rad,
        min_samples=min_samples,
        algorithm='ball_tree',
        metric='haversine'
    )
    subset['cluster_id'] = db.fit_predict(coords)
    return subset
