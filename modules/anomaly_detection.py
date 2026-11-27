
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest


# ---------------------------------------
# 1. GENERATE DEMO CLOUD TELEMETRY
# ---------------------------------------

def generate_anomaly_telemetry():

    np.random.seed(42)

    total_records = 1000

    data = pd.DataFrame({
        "timestamp": pd.date_range(
            start="2026-01-01",
            periods=total_records,
            freq="h"
        ),

        "cpu_usage": np.random.normal(45, 10, total_records),

        "memory_usage": np.random.normal(55, 12, total_records),

        "network_usage": np.random.normal(40, 15, total_records)
    })
    # Assign each telemetry record to a cloud region
    data["region"] = np.random.choice(
        ["Region A", "Region B", "Region C"],
        size=total_records
    )

    # Keep normal readings within realistic limits
    for column in ["cpu_usage", "memory_usage", "network_usage"]:
        data[column] = data[column].clip(1, 100)

    # Add deliberately unusual readings for demonstration
    anomaly_indices = np.random.choice(
        total_records,
        size=50,
        replace=False
    )

    data.loc[anomaly_indices, "cpu_usage"] = np.random.uniform(
        90, 100, 50
    )

    data.loc[anomaly_indices, "memory_usage"] = np.random.uniform(
        90, 100, 50
    )

    data.loc[anomaly_indices, "network_usage"] = np.random.uniform(
        85, 100, 50
    )

    return data


# ---------------------------------------
# 2. TRAIN ISOLATION FOREST
# ---------------------------------------

def detect_anomalies():

    data = generate_anomaly_telemetry()

    features = [
        "cpu_usage",
        "memory_usage",
        "network_usage"
    ]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    # Train and classify records
    data["anomaly_label"] = model.fit_predict(
        data[features]
    )

    # -1 means anomaly; 1 means normal
    data["status"] = data["anomaly_label"].map({
        -1: "Anomaly",
        1: "Normal"
    })

    # Anomaly scores: lower values are more unusual
    data["anomaly_score"] = model.decision_function(
        data[features]
    )

    total_anomalies = int(
        (data["status"] == "Anomaly").sum()
    )

    total_normal = int(
        (data["status"] == "Normal").sum()
    )

    summary = {
        "Total Records": len(data),
        "Anomalies": total_anomalies,
        "Normal Records": total_normal,
        "Anomaly Percentage": round(
            total_anomalies / len(data) * 100, 2
        )
    }

    return model, data, summary


# ---------------------------------------
# 3. DETECT UNUSUAL RESOURCE BEHAVIOUR
# ---------------------------------------

def classify_resource_usage(model, cpu, memory, network):

    sample = pd.DataFrame([{
        "cpu_usage": cpu,
        "memory_usage": memory,
        "network_usage": network
    }])

    prediction = model.predict(sample)[0]

    score = model.decision_function(sample)[0]

    if prediction == -1:
        status = "Anomaly Detected"
    else:
        status = "Normal Behaviour"

    return status, round(float(score), 4)
