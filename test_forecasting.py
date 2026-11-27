from modules.forecasting import (
    train_forecasting_model,
    forecast_next_cpu
)

# Train the model
model, telemetry, predictions, results = train_forecasting_model()

print("\n========== STRATOS CPU FORECASTING ==========")

print("\nModel: Random Forest Regressor")

print("\nModel Evaluation:")
for metric, value in results.items():
    print(f"{metric}: {value}")

print("\nNext CPU Usage Forecast:")

for region in ["Region A", "Region B", "Region C"]:
    forecast = forecast_next_cpu(model, telemetry, region)
    print(f"{region}: {forecast}%")

print("\nForecasting test completed successfully!")