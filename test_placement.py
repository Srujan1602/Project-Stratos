from modules.forecasting import (
    train_forecasting_model,
    forecast_next_cpu
)

from modules.anomaly_detection import detect_anomalies

from modules.placement import (
    get_cloud_regions,
    recommend_region,
    explain_placement
)

print("\n===== PROJECT STRATOS =====")
print("PREDICTIVE AUTONOMOUS PLACEMENT")

# Train forecasting model
model, telemetry, predictions, results = train_forecasting_model()

# Generate CPU forecasts for each region
forecasts = {}

for region in ["Region A", "Region B", "Region C"]:
    forecasts[region] = forecast_next_cpu(
        model, telemetry, region
    )

# Run anomaly detection
anomaly_model, anomaly_data, anomaly_summary = detect_anomalies()

# Connect anomaly results to placement
regions = get_cloud_regions(anomaly_data)

# Example workload
workload_cpu = 8
workload_memory = 16

print("\nForecasting Results:")
print(results)

print("\nPredicted CPU Demand:")
for region, value in forecasts.items():
    print(f"{region}: {value}%")

print("\nAnomaly Summary:")
print(anomaly_summary)

# Use the highest regional forecast as a conservative
# shared forecast adjustment for this prototype.
predicted_cpu = max(forecasts.values())

best_region, eligible = recommend_region(
    workload_cpu,
    workload_memory,
    regions,
    predicted_cpu=predicted_cpu
)

print("\nPlacement Decision:")

if best_region is not None:

    result = explain_placement(best_region)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nRegional Ranking:")
    print(
        eligible[
            ["region", "available_cpu", "placement_score"]
        ].to_string(index=False)
    )

else:
    print("No suitable cloud region found.")

print("\nSTRATOS predictive placement test completed!")