import pandas as pd


# ==========================================
# STRATOS INTELLIGENT WORKLOAD PLACEMENT
# ==========================================

def get_cloud_regions(anomaly_data=None):

    regions = pd.DataFrame({

        "region": ["Region A", "Region B", "Region C"],

        "cpu_capacity": [120, 90, 150],
        "memory_capacity": [120, 96, 140],

        "cpu_usage": [58, 72, 41],
        "memory_usage": [64, 55, 48],

        "latency": [25, 45, 15],
        "cost": [0.08, 0.06, 0.12],

        "anomaly_risk": [0.10, 0.20, 0.05]

    })

    # Calculate regional anomaly risk
    if anomaly_data is not None:

        regional_risk = (
            anomaly_data.assign(
                is_anomaly=(
                    anomaly_data["status"] == "Anomaly"
                ).astype(int)
            )
            .groupby("region")["is_anomaly"]
            .mean()
        )

        regions["anomaly_risk"] = (
            regions["region"]
            .map(regional_risk)
            .fillna(regions["anomaly_risk"])
        )

    return regions


# ==========================================
# CALCULATE AVAILABLE RESOURCES
# ==========================================

def calculate_available_resources(regions):

    regions = regions.copy()

    regions["effective_cpu_usage"] = regions["cpu_usage"]

    regions["available_cpu"] = (
        regions["cpu_capacity"] *
        (1 - regions["effective_cpu_usage"] / 100)
    )

    regions["available_memory"] = (
        regions["memory_capacity"] *
        (1 - regions["memory_usage"] / 100)
    )

    return regions


# ==========================================
# INTELLIGENT PLACEMENT ALGORITHM
# ==========================================

def recommend_region(
    workload_cpu,
    workload_memory,
    regions=None,
    latency_weight=0.25,
    cost_weight=0.25,
    resource_weight=0.30,
    risk_weight=0.20,
    predicted_cpu=None
):
    if workload_cpu <= 0 or workload_memory <= 0:
        raise ValueError("Workload requirements must be positive.")

    if regions is None:
        regions = get_cloud_regions()

    regions = regions.copy()

    # Convert numeric columns to float
    numeric_columns = [
        "cpu_usage",
        "memory_usage",
        "cpu_capacity",
        "memory_capacity",
        "latency",
        "cost",
        "anomaly_risk"
    ]

    for column in numeric_columns:
        regions[column] = pd.to_numeric(
            regions[column],
            errors="raise"
        ).astype(float)

    # Validate and normalize weights
    weights = [
        latency_weight,
        cost_weight,
        resource_weight,
        risk_weight
    ]

    if any(weight < 0 for weight in weights):
        raise ValueError("Weights cannot be negative.")

    total = sum(weights)

    if total == 0:
        raise ValueError("At least one weight must be positive.")

    latency_weight /= total
    cost_weight /= total
    resource_weight /= total
    risk_weight /= total

    # Apply predicted CPU usage
    if predicted_cpu is not None:
        if not isinstance(predicted_cpu, dict):
            raise TypeError("predicted_cpu must be a dictionary.")

        for region_name, prediction in predicted_cpu.items():
            prediction = float(prediction)

            if not 0 <= prediction <= 100:
                raise ValueError(
                    "Predicted CPU must be between 0 and 100."
                )

            mask = regions["region"] == region_name

            if not mask.any():
                raise ValueError(f"Unknown cloud region: {region_name}")

            current_usage = float(
                regions.loc[mask, "cpu_usage"].iloc[0]
            )

            regions.loc[mask, "cpu_usage"] = max(
                current_usage,
                prediction
            )

    # Calculate available resources
    regions = calculate_available_resources(regions)

    # Filter eligible regions
    eligible = regions[
        (regions["available_cpu"] >= workload_cpu) &
        (regions["available_memory"] >= workload_memory)
    ].copy()

    if eligible.empty:
        return None, regions

    # Normalize latency and cost
    latency_max = max(regions["latency"].max(), 1)
    cost_max = max(regions["cost"].max(), 0.000001)

    eligible["latency_score"] = (
        1 - eligible["latency"] / latency_max
    )

    eligible["cost_score"] = (
        1 - eligible["cost"] / cost_max
    )

    # Resource availability score
    eligible["resource_score"] = (
        0.5 * eligible["available_cpu"] /
        regions["cpu_capacity"].max()
        +
        0.5 * eligible["available_memory"] /
        regions["memory_capacity"].max()
    )

    # Anomaly risk score
    eligible["risk_score"] = (
        1 - eligible["anomaly_risk"].clip(0, 1)
    )

    # Final weighted placement score
    eligible["placement_score"] = (
        latency_weight * eligible["latency_score"]
        + cost_weight * eligible["cost_score"]
        + resource_weight * eligible["resource_score"]
        + risk_weight * eligible["risk_score"]
    ) * 100

    eligible = eligible.sort_values(
        "placement_score",
        ascending=False
    )

    best_region = eligible.iloc[0]

    return best_region, eligible


# ==========================================
# PLACEMENT EXPLANATION
# ==========================================

def explain_placement(region):

    return {

        "Selected Region": region["region"],

        "Placement Score": round(
            float(region["placement_score"]), 2
        ),

        "Available CPU": round(
            float(region["available_cpu"]), 2
        ),

        "Available Memory": round(
            float(region["available_memory"]), 2
        ),

        "Latency": float(region["latency"]),

        "Hourly Cost": float(region["cost"]),

        "Anomaly Risk": float(region["anomaly_risk"]),

        "Predicted CPU Usage": round(
            float(region["effective_cpu_usage"]), 2
        )

    }