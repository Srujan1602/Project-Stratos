
from modules.anomaly_detection import (
    detect_anomalies,
    classify_resource_usage
)

model, data, summary = detect_anomalies()

print("\n========== STRATOS ANOMALY DETECTION ==========")

print("\nDetection Summary:")

for key, value in summary.items():
    print(f"{key}: {value}")

print("\nTesting Normal Resource Usage:")

status, score = classify_resource_usage(
    model, 40, 50, 35
)

print("Status:", status)
print("Anomaly Score:", score)

print("\nTesting Unusual Resource Usage:")

status, score = classify_resource_usage(
    model, 98, 97, 95
)

print("Status:", status)
print("Anomaly Score:", score)

print("\nAnomaly detection test completed!")
