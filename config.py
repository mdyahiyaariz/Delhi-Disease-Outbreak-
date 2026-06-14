"""Configuration and constants for the outbreak detection pipeline."""

from datetime import datetime
from pathlib import Path

# Output directory
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Disease and location configuration
DISEASES = ['Dengue', 'Cholera', 'Typhoid']
DISEASE_CLUSTERS = {
    'Dengue': [(28.62, 77.21), (28.65, 77.18)],
    'Cholera': [(28.60, 77.23)],
    'Typhoid': [(28.63, 77.20), (28.61, 77.25)],
}

# Temporal configuration
START_DATE = datetime(2024, 1, 1)

# Data generation parameters
NOISE_COUNT = 30
SEED = 42

# Clustering parameters
DBSCAN_EPS_KM = 1.5
DBSCAN_MIN_SAMPLES = 3

# Anomaly detection thresholds
ZSCORE_THRESHOLD = 2.5
RESIDUAL_THRESHOLD = 2.0
SPATIAL_SCAN_THRESHOLD = 3.84

# AI model parameters
AI_N_ESTIMATORS = 200
AI_CONTAMINATION = 0.05
AI_RANDOM_STATE = 42
