import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_cluster(center_lat, center_lon, n, spread=0.01):
    return (
        np.random.normal(center_lat, spread, n),
        np.random.normal(center_lon, spread, n),
    )

def generate_synthetic_data():
    np.random.seed(42)
    diseases = ["Dengue", "Cholera", "Typhoid"]
    disease_clusters = {
        "Dengue":  [(28.62, 77.21), (28.65, 77.18)],
        "Cholera": [(28.60, 77.23)],
        "Typhoid": [(28.63, 77.20), (28.61, 77.25)],
    }

    records = []
    start_date = datetime(2024, 1, 1)
    patient_id = 1

    for disease, centers in disease_clusters.items():
        for center in centers:
            cluster_size = np.random.randint(25, 50)
            home_lats, home_lons = generate_cluster(*center, cluster_size)
            work_lats, work_lons = generate_cluster(
                center[0] + np.random.uniform(-0.05, 0.05),
                center[1] + np.random.uniform(-0.05, 0.05),
                cluster_size, spread=0.02
            )
            for i in range(cluster_size):
                # Add an outbreak spike in weeks 8-10 for one disease per cluster
                week_offset = np.random.randint(0, 20)
                if disease == "Dengue" and week_offset in range(8, 11):
                    week_offset = np.random.choice(range(8, 11), p=[0.4, 0.4, 0.2])

                record_date = start_date + timedelta(weeks=int(week_offset),
                                                      days=np.random.randint(0, 7))
                records.append({
                    "patient_id": f"P{patient_id:04d}",
                    "home_lat": home_lats[i],
                    "home_lon": home_lons[i],
                    "work_lat": work_lats[i],
                    "work_lon": work_lons[i],
                    "predicted_disease": disease,
                    "confidence": round(np.random.uniform(0.65, 0.99), 2),
                    "record_date": record_date.strftime("%Y-%m-%d"),
                })
                patient_id += 1

    # Add some random noise patients
    for _ in range(30):
        disease = np.random.choice(diseases)
        records.append({
            "patient_id": f"P{patient_id:04d}",
            "home_lat": np.random.uniform(28.55, 28.70),
            "home_lon": np.random.uniform(77.15, 77.30),
            "work_lat": np.random.uniform(28.55, 28.70),
            "work_lon": np.random.uniform(77.15, 77.30),
            "predicted_disease": disease,
            "confidence": round(np.random.uniform(0.50, 0.80), 2),
            "record_date": (start_date + timedelta(days=np.random.randint(0, 140))).strftime("%Y-%m-%d"),
        })
        patient_id += 1

    patient_df = pd.DataFrame(records)
    return patient_df, diseases

def load_data_from_csv(file_path):
    patient_df = pd.read_csv(file_path)
    diseases = patient_df['predicted_disease'].unique().tolist()
    return patient_df, diseases
