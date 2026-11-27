import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ---------------------------------------
# 1. GENERATE SYNTHETIC CLOUD TELEMETRY
# ---------------------------------------

def generate_demo_telemetry():
    """
    Creates sample CPU usage data for three simulated cloud regions.
    This is synthetic data, not real cloud-provider telemetry.
    """

    np.random.seed(42)

    regions = ["Region A", "Region B", "Region C"]
    records = []

    for region_id, region in enumerate(regions):

        total_records = 1500

        for i in range(total_records):

            # Simulate changing CPU usage over time
            daily_pattern = 15 * np.sin(i / 24)
            workload_pattern = 10 * np.sin(i / 7)

            base_usage = 40 + (region_id * 5)

            noise = np.random.normal(0, 5)

            cpu_usage = base_usage + daily_pattern + workload_pattern + noise
            cpu_usage = np.clip(cpu_usage, 5, 95)

            memory_usage = np.clip(
                cpu_usage * 0.7 + np.random.normal(10, 5),
                5,
                95
            )

            network_usage = np.clip(
                cpu_usage * 0.5 + np.random.normal(15, 8),
                1,
                100
            )

            records.append({
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=i),
                "region": region,
                "region_id": region_id,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "network_usage": network_usage
            })

    return pd.DataFrame(records)


# ---------------------------------------
# 2. PREPARE FEATURES FOR THE MODEL
# ---------------------------------------

def prepare_forecasting_data(data):

    prepared_data = []

    for region in data["region"].unique():

        region_data = data[data["region"] == region].copy()
        region_data = region_data.sort_values("timestamp").reset_index(drop=True)

        # Previous CPU readings become model inputs
        region_data["cpu_lag_1"] = region_data["cpu_usage"].shift(1)
        region_data["cpu_lag_2"] = region_data["cpu_usage"].shift(2)
        region_data["cpu_lag_3"] = region_data["cpu_usage"].shift(3)

        # Average of the previous three readings
        region_data["cpu_rolling_mean"] = (
            region_data["cpu_usage"]
            .rolling(window=3)
            .mean()
        )

        # Target: CPU usage in the next hour
        region_data["next_cpu"] = region_data["cpu_usage"].shift(-1)

        region_data["hour"] = region_data["timestamp"].dt.hour

        prepared_data.append(region_data)

    final_data = pd.concat(prepared_data, ignore_index=True)

    final_data = final_data.dropna().sort_values("timestamp")

    return final_data


# ---------------------------------------
# 3. TRAIN RANDOM FOREST MODEL
# ---------------------------------------

def train_forecasting_model():

    telemetry = generate_demo_telemetry()

    data = prepare_forecasting_data(telemetry)

    features = [
        "cpu_usage",
        "cpu_lag_1",
        "cpu_lag_2",
        "cpu_lag_3",
        "cpu_rolling_mean",
        "memory_usage",
        "network_usage",
        "hour",
        "region_id"
    ]

    target = "next_cpu"

    # Chronological split: earlier records for training,
    # later records for testing.
    split_index = int(len(data) * 0.8)

    train_data = data.iloc[:split_index]
    test_data = data.iloc[split_index:]

    X_train = train_data[features]
    y_train = train_data[target]

    X_test = test_data[features]
    y_test = test_data[target]

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    # Model evaluation
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    results = {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2 Score": round(r2, 4)
    }

    # Keep actual and predicted values together for plotting
    prediction_results = test_data[
        ["timestamp", "region", target]
    ].copy()

    prediction_results["predicted_cpu"] = predictions

    return model, telemetry, prediction_results, results


# ---------------------------------------
# 4. FORECAST NEXT CPU USAGE
# ---------------------------------------

def forecast_next_cpu(model, telemetry, region_name):

    region_data = telemetry[
        telemetry["region"] == region_name
    ].sort_values("timestamp")

    latest = region_data.tail(4)

    if len(latest) < 4:
        raise ValueError("Not enough telemetry records to forecast.")

    latest_cpu = latest["cpu_usage"].to_numpy()

    latest_row = latest.iloc[-1]

    input_data = pd.DataFrame([{
        "cpu_usage": latest_cpu[3],
        "cpu_lag_1": latest_cpu[2],
        "cpu_lag_2": latest_cpu[1],
        "cpu_lag_3": latest_cpu[0],
        "cpu_rolling_mean": np.mean(latest_cpu),
        "memory_usage": latest_row["memory_usage"],
        "network_usage": latest_row["network_usage"],
        "hour": (latest_row["timestamp"].hour + 1) % 24,
        "region_id": int(latest_row["region_id"])
    }])

    prediction = model.predict(input_data)[0]

    return round(float(np.clip(prediction, 0, 100)), 2)