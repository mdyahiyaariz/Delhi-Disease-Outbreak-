from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_cluster(center_lat, center_lon, n, spread=0.01):
    return (
        np.random.normal(center_lat, spread, n),
        np.random.normal(center_lon, spread, n),
    )

def generate_csv_data():
    # np.random.seed(999) # Removed fixed seed for varied data
    diseases = ["Dengue", "Cholera", "Typhoid"]
    disease_clusters = {
        "Dengue":  [(28.62, 77.21), (28.65, 77.18)],
        "Cholera": [(28.60, 77.23)],
        "Typhoid": [(28.63, 77.20), (28.61, 77.25)],
    }

    records = []
    start_date = datetime(2024, 1, 1)
    patient_id = 1

    # ─── BASELINE: Normal patients spread across 20 weeks ─────────────────────
    for disease, centers in disease_clusters.items():
        for center in centers:
            cluster_size = np.random.randint(20, 35)
            home_lats, home_lons = generate_cluster(*center, cluster_size)
            work_lats, work_lons = generate_cluster(
                center[0] + np.random.uniform(-0.05, 0.05),
                center[1] + np.random.uniform(-0.05, 0.05),
                cluster_size, spread=0.02
            )
            for i in range(cluster_size):
                # Normal patients: evenly distributed across weeks 0-20
                week_offset = np.random.randint(0, 20)
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
                    "is_true_anomaly": False,
                })
                patient_id += 1

    # ─── MASSIVE OUTBREAK SPIKE: Dengue cluster 1, Week 6 ────────────────────
    # Inject 60 patients into a single tight cluster in week 6 - a clear spike
    dengue_center = (28.62, 77.21)
    spike_size = 60
    home_lats, home_lons = generate_cluster(*dengue_center, spike_size, spread=0.004)
    work_lats, work_lons = generate_cluster(*dengue_center, spike_size, spread=0.006)
    for i in range(spike_size):
        record_date = start_date + timedelta(weeks=6, days=np.random.randint(0, 7))
        records.append({
            "patient_id": f"P{patient_id:04d}",
            "home_lat": home_lats[i],
            "home_lon": home_lons[i],
            "work_lat": work_lats[i],
            "work_lon": work_lons[i],
            "predicted_disease": "Dengue",
            "confidence": round(np.random.uniform(0.88, 0.99), 2),
            "record_date": record_date.strftime("%Y-%m-%d"),
            "is_true_anomaly": True,
        })
        patient_id += 1

    # ─── MASSIVE OUTBREAK SPIKE: Cholera cluster, Week 12 ────────────────────
    cholera_center = (28.60, 77.23)
    spike_size = 55
    home_lats, home_lons = generate_cluster(*cholera_center, spike_size, spread=0.004)
    work_lats, work_lons = generate_cluster(*cholera_center, spike_size, spread=0.006)
    for i in range(spike_size):
        record_date = start_date + timedelta(weeks=12, days=np.random.randint(0, 7))
        records.append({
            "patient_id": f"P{patient_id:04d}",
            "home_lat": home_lats[i],
            "home_lon": home_lons[i],
            "work_lat": work_lats[i],
            "work_lon": work_lons[i],
            "predicted_disease": "Cholera",
            "confidence": round(np.random.uniform(0.88, 0.99), 2),
            "record_date": record_date.strftime("%Y-%m-%d"),
            "is_true_anomaly": True,
        })
        patient_id += 1

    # ─── MASSIVE OUTBREAK SPIKE: Typhoid cluster 1, Week 16 ──────────────────
    typhoid_center = (28.63, 77.20)
    spike_size = 50
    home_lats, home_lons = generate_cluster(*typhoid_center, spike_size, spread=0.004)
    work_lats, work_lons = generate_cluster(*typhoid_center, spike_size, spread=0.006)
    for i in range(spike_size):
        record_date = start_date + timedelta(weeks=16, days=np.random.randint(0, 7))
        records.append({
            "patient_id": f"P{patient_id:04d}",
            "home_lat": home_lats[i],
            "home_lon": home_lons[i],
            "work_lat": work_lats[i],
            "work_lon": work_lons[i],
            "predicted_disease": "Typhoid",
            "confidence": round(np.random.uniform(0.88, 0.99), 2),
            "record_date": record_date.strftime("%Y-%m-%d"),
            "is_true_anomaly": True,
        })
        patient_id += 1

    # ─── Random noise patients ────────────────────────────────────────────────
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
            "is_true_anomaly": False,
        })
        patient_id += 1

    patient_df = pd.DataFrame(records)
    output_path = Path("inputs") / "input_patients.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    patient_df.to_csv(output_path, index=False)
    true_anomalies = int(patient_df['is_true_anomaly'].sum())
    print(f"Successfully generated {output_path} with {len(patient_df)} patient records.")
    print(f"  True outbreak patients injected : {true_anomalies}")
    print(f"  Normal/baseline patients        : {len(patient_df) - true_anomalies}")

if __name__ == "__main__":
    generate_csv_data()
