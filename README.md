# Delhi Outbreak Detection System

An AI-powered disease outbreak detection pipeline that combines geospatial clustering, statistical anomaly detection, and machine learning to identify emerging disease outbreaks across Delhi. The system is designed for pharmaceutical market intelligence, healthcare analytics, public health surveillance, and inventory planning.

---

# Overview

Pharmaceutical companies and public health organizations often struggle to identify disease hotspots early enough to optimize medicine supply, inventory allocation, and intervention planning.

The Delhi Outbreak Detection System addresses this challenge by:

- Generating or ingesting patient-level health data
- Performing geospatial clustering of disease cases
- Creating spatio-temporal summaries
- Detecting abnormal disease activity using statistical and AI-based techniques
- Generating actionable outbreak alerts
- Exporting results for visualization and analysis

---

# Problem Statement

Disease outbreaks frequently emerge at the locality level before becoming visible at larger geographic scales. Traditional reporting systems may not detect these trends early enough for effective response.

This project provides an automated outbreak detection framework that:

- Identifies disease hotspots geographically
- Detects unusual increases in case counts
- Applies machine learning for anomaly discovery
- Supports pharmaceutical demand forecasting
- Enables proactive public health monitoring

---

# Key Features

### Geospatial Disease Clustering
Uses DBSCAN-based spatial clustering to group nearby disease cases into outbreak regions.

### Spatio-Temporal Analysis
Aggregates disease incidence over time and location for trend monitoring.

### Multi-Method Outbreak Detection
Supports four complementary detection approaches:

| Method | Description |
|----------|-------------|
| Z-Score Detection | Statistical anomaly detection using standard deviations |
| Residual Analysis | Rolling mean residual-based anomaly detection |
| Spatial Scan Statistic | Kulldorff-style log-likelihood ratio hotspot detection |
| Isolation Forest | AI-driven unsupervised anomaly detection |

### Automated Alert Generation
Produces outbreak alerts when abnormal activity is detected.

### CSV-Based Outputs
Exports results for dashboards, GIS systems, and further analysis.

---

# Project Architecture

```text
test_outbreak.py

└── pipeline.py

    ├── config.py           # Constants and thresholds
    ├── data_generation.py  # Synthetic patient data generation
    ├── spatial.py          # DBSCAN geo-clustering
    ├── aggregation.py      # Weekly spatio-temporal aggregation
    ├── detection.py        # Statistical & AI anomaly detection
    ├── validation.py       # Cluster/map validation
    ├── alerts.py           # Alert generation and export
    └── utils.py            # Helper functions
```

---

# Installation

## Requirements

- Python 3.7+
- pandas
- numpy
- scipy
- scikit-learn

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Quick Start

Run the complete outbreak detection pipeline:

```bash
python test_outbreak.py
```

Generated outputs will be saved in:

```text
outputs/
```

---

# Running the Pipeline

## Full Pipeline Execution

```python
from pipeline import run_pipeline

run_pipeline()
```

This will:

1. Generate or load patient data
2. Build geospatial nodes
3. Perform disease clustering
4. Aggregate temporal statistics
5. Detect anomalies
6. Generate outbreak alerts
7. Export results to CSV files

---

# Module-Level Usage

You can use individual modules independently.

## Generate Synthetic Data

```python
from data_generation import generate_synthetic_data

patients = generate_synthetic_data(seed=42)
```

---

## Build Geographic Nodes

```python
from data_generation import build_nodes

nodes = build_nodes(patients)
```

---

## Disease-Based Clustering

```python
from spatial import cluster_by_disease

clustered = cluster_by_disease(nodes, 'Dengue')
```

---

## AI-Based Anomaly Detection

```python
from detection import ai_anomaly_detection

results = ai_anomaly_detection(clustered)
```

---

# Using Your Own Dataset

You may replace the synthetic data with real patient records.

Example:

```python
import pandas as pd

from data_generation import build_nodes
from spatial import cluster_by_disease
from aggregation import aggregate_clusters
from detection import zscore_anomaly

patients = pd.read_csv('my_patients.csv')

nodes = build_nodes(patients)

clustered = cluster_by_disease(
    nodes,
    disease='Dengue'
)

aggregated = aggregate_clusters(clustered)

anomalies = zscore_anomaly(
    aggregated,
    threshold=3.0
)
```

---

# Detection Algorithms

## 1. Z-Score Detection

Measures how far current case counts deviate from historical averages.

Suitable for:

- Sudden spikes
- Seasonal monitoring
- Fast statistical screening

---

## 2. Residual-Based Detection

Uses rolling averages and residual calculations to identify unusual increases.

Suitable for:

- Trend-aware anomaly detection
- Moderate outbreak growth patterns

---

## 3. Spatial Scan Statistic

Implements a Kulldorff-style likelihood ratio approach to identify geographic disease hotspots.

Suitable for:

- Localized outbreaks
- Cluster significance assessment

---

## 4. Isolation Forest

Machine learning-based anomaly detection using unsupervised learning.

Suitable for:

- Complex outbreak patterns
- Unknown anomaly structures
- High-dimensional feature spaces

---

# Output Files

After execution, the system generates the following files:

| File | Description |
|--------|-------------|
| `outputs/spatio_temporal_data.csv` | Weekly disease counts per cluster |
| `outputs/anomaly_results.csv` | Spatial scan likelihood-ratio scores |
| `outputs/ai_anomaly_results.csv` | Isolation Forest anomaly scores |
| `outputs/alerts.csv` | Final outbreak alerts |

---

# Configuration

All configurable parameters are located in:

```python
config.py
```

Default settings:

```python
DBSCAN_EPS_KM = 1.5
ZSCORE_THRESHOLD = 2.5
AI_CONTAMINATION = 0.05
SEED = 42
```

### Parameter Descriptions

| Parameter | Purpose |
|------------|----------|
| `DBSCAN_EPS_KM` | Radius used for spatial clustering |
| `ZSCORE_THRESHOLD` | Sensitivity threshold for Z-score anomalies |
| `AI_CONTAMINATION` | Expected anomaly percentage for Isolation Forest |
| `SEED` | Random seed for reproducibility |

---

# Troubleshooting

| Issue | Solution |
|---------|-----------|
| No anomalies detected | Lower `ZSCORE_THRESHOLD` or `AI_CONTAMINATION` |
| Too many anomalies | Increase thresholds for stricter detection |
| Import errors | Ensure all Python files are in the same directory |
| Memory issues | Reduce `NOISE_COUNT` or process diseases individually |
| Empty clusters | Increase DBSCAN radius (`DBSCAN_EPS_KM`) |

---

# Example Workflow

```text
Patient Records
       │
       ▼
Geospatial Node Creation
       │
       ▼
Disease-Specific Clustering
       │
       ▼
Weekly Aggregation
       │
       ▼
Anomaly Detection
       │
       ├── Z-Score
       ├── Residual Analysis
       ├── Spatial Scan
       └── Isolation Forest
       │
       ▼
Alert Generation
       │
       ▼
CSV Reports & Visualization
```

---

# Applications

### Pharmaceutical Industry

- Inventory planning
- Regional medicine demand forecasting
- Supply chain optimization
- Market intelligence

### Public Health

- Early outbreak surveillance
- Disease hotspot identification
- Resource allocation
- Epidemiological monitoring

### Research & Analytics

- Spatial epidemiology
- Disease trend analysis
- Health data science
- AI-based outbreak prediction

---

# Future Enhancements

- Real-time streaming data ingestion
- Interactive GIS dashboard
- Weather and environmental integration
- Forecasting using LSTM/Transformer models
- Automated health authority notifications
- Multi-city outbreak monitoring
- Cloud deployment support

---

# License

MIT License

Free to use, modify, and distribute for academic, research, and commercial applications.