import numpy as np
import pandas as pd

from modules.forecasting import (
    train_forecasting_model,
    forecast_next_cpu
)

from modules.anomaly_detection import detect_anomalies

from modules.placement import (
    get_cloud_regions,
    calculate_available_resources
)


# ==========================================
# 1. GENERATE COMMON WORKLOADS
# ==========================================

def generate_workloads(num_workloads=100, seed=42):

    rng = np.random.default_rng(seed)

    workloads = pd.DataFrame({
        "workload_id": [
            f"WL-{i:03d}" for i in range(1, num_workloads + 1)
        ],
        "cpu_required": rng.uniform(
            0.5, 3.0, num_workloads
        ),
        "memory_required": rng.uniform(
            1.0, 2.5, num_workloads
        ),
        "duration_hours": rng.uniform(
            1.0, 3.0, num_workloads
        )
    })

    return workloads


# ==========================================
# 2. REGION SCORING
# ==========================================

def calculate_strategy_score(region, max_latency, max_cost):

    latency_score = 1 - (
        region["latency"] / max_latency
    )

    cost_score = 1 - (
        region["cost"] / max_cost
    )

    resource_score = (
        0.5 * region["available_cpu"] /
        region["cpu_capacity"]
        +
        0.5 * region["available_memory"] /
        region["memory_capacity"]
    )

    risk_score = 1 - region["anomaly_risk"]

    score = (
        0.25 * latency_score
        + 0.20 * cost_score
        + 0.30 * resource_score
        + 0.25 * risk_score
    )

    return score


# ==========================================
# 3. SELECT REGION USING STRATEGY
# ==========================================

def select_region(
    strategy,
    eligible,
    regions,
    round_robin_index=0
):

    if eligible.empty:
        return None, round_robin_index

    if strategy == "Round Robin":

        region_order = regions["region"].tolist()

        for offset in range(len(region_order)):

            index = (
                round_robin_index + offset
            ) % len(region_order)

            region_name = region_order[index]

            matches = eligible[
                eligible["region"] == region_name
            ]

            if not matches.empty:
                return matches.iloc[0], (
                    index + 1
                ) % len(region_order)

    elif strategy == "First Fit":

        return eligible.iloc[0], round_robin_index

    elif strategy == "Best Fit":

        candidates = eligible.copy()

        candidates["fit_score"] = (
            (candidates["available_cpu"] -
             candidates["workload_cpu"]) /
            candidates["cpu_capacity"]
            +
            (candidates["available_memory"] -
             candidates["workload_memory"]) /
            candidates["memory_capacity"]
        )

        selected = candidates.sort_values(
            "fit_score"
        ).iloc[0]

        return selected, round_robin_index

    elif strategy == "Greedy Cost":

        selected = eligible.sort_values(
            "cost"
        ).iloc[0]

        return selected, round_robin_index

    elif strategy in [
        "Reactive STRATOS",
        "Full STRATOS"
    ]:

        candidates = eligible.copy()

        max_latency = max(
            regions["latency"].max(), 1
        )

        max_cost = max(
            regions["cost"].max(), 0.000001
        )

        candidates["strategy_score"] = candidates.apply(
            lambda row: calculate_strategy_score(
                row,
                max_latency,
                max_cost
            ),
            axis=1
        )

        selected = candidates.sort_values(
            "strategy_score",
            ascending=False
        ).iloc[0]

        return selected, round_robin_index

    return None, round_robin_index


# ==========================================
# 4. RUN ONE SCHEDULING STRATEGY
# ==========================================

def run_strategy(
    strategy,
    workloads,
    initial_regions
):

    regions = calculate_available_resources(
        initial_regions
    )

    regions = regions.copy()

    # Keep decimal resource values
    regions["available_cpu"] = (
        regions["available_cpu"].astype(float)
    )

    regions["available_memory"] = (
        regions["available_memory"].astype(float)
    )

    initial_cpu = regions["available_cpu"].sum()
    initial_memory = regions["available_memory"].sum()

    total_cost = 0.0
    sla_violations = 0
    successful_placements = 0

    latencies = []
    round_robin_index = 0

    for _, workload in workloads.iterrows():

        cpu_required = float(
            workload["cpu_required"]
        )

        memory_required = float(
            workload["memory_required"]
        )

        eligible = regions[
            (regions["available_cpu"] >= cpu_required)
            &
            (regions["available_memory"] >= memory_required)
        ].copy()

        # Add workload requirements for Best Fit
        eligible["workload_cpu"] = cpu_required
        eligible["workload_memory"] = memory_required

        selected, round_robin_index = select_region(
            strategy,
            eligible,
            regions,
            round_robin_index
        )

        # No eligible region
        if selected is None:

            sla_violations += 1
            continue

        region_index = selected.name

        # Allocate resources
        regions.loc[
            region_index, "available_cpu"
        ] -= cpu_required

        regions.loc[
            region_index, "available_memory"
        ] -= memory_required

        successful_placements += 1

        latency = float(selected["latency"])
        hourly_cost = float(selected["cost"])
        duration = float(workload["duration_hours"])

        latencies.append(latency)

        total_cost += hourly_cost * duration

        # Simulated latency SLA threshold
        if latency > 40:
            sla_violations += 1

    # Calculate final metrics
    average_latency = (
        float(np.mean(latencies))
        if latencies else 0.0
    )

    placement_success_rate = (
        successful_placements / len(workloads)
    ) * 100

    cpu_utilization = (
        (initial_cpu - regions["available_cpu"].sum())
        / initial_cpu * 100
        if initial_cpu > 0 else 0
    )

    memory_utilization = (
        (initial_memory - regions["available_memory"].sum())
        / initial_memory * 100
        if initial_memory > 0 else 0
    )

    resource_utilization = (
        cpu_utilization + memory_utilization
    ) / 2

    return {
        "Strategy": strategy,
        "SLA Violations": sla_violations,
        "Latency (ms)": round(average_latency, 2),
        "Total Cost ($)": round(total_cost, 2),
        "Placement Success (%)": round(
            placement_success_rate, 2
        ),
        "Resource Utilization (%)": round(
            resource_utilization, 2
        )
    }


# ==========================================
# 5. COMPLETE SIMULATION ENGINE
# ==========================================

def run_simulation(num_workloads=100, seed=42):

    # Generate identical workloads for all strategies
    workloads = generate_workloads(
        num_workloads,
        seed
    )

    # Train forecasting model
    forecast_model, telemetry, _, forecast_metrics = (
        train_forecasting_model()
    )

    # Detect anomalies
    anomaly_model, anomaly_data, anomaly_summary = (
        detect_anomalies()
    )

    # Obtain regional infrastructure data
    base_regions = get_cloud_regions(
        anomaly_data
    )

    # Obtain next-hour CPU forecasts
    predicted_cpu = {}

    for region_name in base_regions["region"]:

        predicted_cpu[region_name] = (
            forecast_next_cpu(
                forecast_model,
                telemetry,
                region_name
            )
        )

    # Create forecast-adjusted regions
    forecast_regions = base_regions.copy()

    forecast_regions["cpu_usage"] = (
        forecast_regions["cpu_usage"].astype(float)
    )

    for region_name, prediction in predicted_cpu.items():

        mask = (
            forecast_regions["region"] == region_name
        )

        forecast_regions.loc[mask, "cpu_usage"] = max(
            float(
                forecast_regions.loc[
                    mask, "cpu_usage"
                ].iloc[0]
            ),
            float(prediction)
        )

    # Six scheduling strategies
    strategies = [
        "Round Robin",
        "First Fit",
        "Best Fit",
        "Greedy Cost",
        "Reactive STRATOS",
        "Full STRATOS"
    ]

    results = []

    for strategy in strategies:

        if strategy == "Full STRATOS":

            starting_regions = forecast_regions

        else:

            starting_regions = base_regions

        result = run_strategy(
            strategy,
            workloads,
            starting_regions
        )

        results.append(result)

    comparison = pd.DataFrame(results)

    return (
        comparison,
        workloads,
        predicted_cpu,
        anomaly_summary,
        forecast_metrics
    )