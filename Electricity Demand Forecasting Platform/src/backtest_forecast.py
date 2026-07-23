import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


BASE_DIR = Path(__file__).resolve().parent.parent

country = "germany"


# ---------------------------------------
# Backtest date
# ---------------------------------------

forecast_date = pd.to_datetime(
    "2025-12-31"
)



# ---------------------------------------
# Load dataset
# ---------------------------------------

data_file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    country
    /
    "load_weather_dataset.csv"
)


df = pd.read_csv(
    data_file,
    parse_dates=["datetime"]
)


df = (
    df
    .sort_values("datetime")
    .reset_index(drop=True)
)



# ---------------------------------------
# Create calendar features
# ---------------------------------------

df["hour"] = (
    df["datetime"]
    .dt.hour
)


df["day_of_week"] = (
    df["datetime"]
    .dt.dayofweek
)


df["month"] = (
    df["datetime"]
    .dt.month
)


df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)



# ---------------------------------------
# Create load lag features
# ---------------------------------------

df["load_lag_1"] = (
    df["load_mwh"]
    .shift(1)
)


df["load_lag_24"] = (
    df["load_mwh"]
    .shift(24)
)


df["load_lag_168"] = (
    df["load_mwh"]
    .shift(168)
)



# ---------------------------------------
# Rolling features
# ---------------------------------------

df["load_mean_24"] = (
    df["load_mwh"]
    .shift(1)
    .rolling(24)
    .mean()
)


df["load_std_24"] = (
    df["load_mwh"]
    .shift(1)
    .rolling(24)
    .std()
)



# Remove incomplete rows

df = df.dropna()



# ---------------------------------------
# Select backtest day
# ---------------------------------------

test_day = df[
    df["datetime"].dt.date
    ==
    forecast_date.date()
]


print(
    "Forecast rows:",
    len(test_day)
)



# ---------------------------------------
# Features
# EXACT SAME ORDER AS TRAINING
# ---------------------------------------

features = [

    "temperature_2m",

    "relative_humidity_2m",

    "wind_speed_10m",

    "cloud_cover",

    "surface_pressure",

    "shortwave_radiation",

    "hour",

    "day_of_week",

    "month",

    "is_weekend",

    "load_lag_1",

    "load_lag_24",

    "load_lag_168",

    "load_mean_24",

    "load_std_24"

]



X_test = test_day[
    features
]


y_test = test_day[
    "load_mwh"
]



# ---------------------------------------
# Load model
# ---------------------------------------

model_file = (

    BASE_DIR
    /
    "models"
    /
    country
    /
    "xgboost_load_forecaster.pkl"

)


model = joblib.load(
    model_file
)



# ---------------------------------------
# Prediction
# ---------------------------------------

prediction = model.predict(
    X_test
)



# ---------------------------------------
# Metrics
# ---------------------------------------

mae = mean_absolute_error(
    y_test,
    prediction
)


mse = mean_squared_error(
    y_test,
    prediction
)

rmse = mse ** 0.5


r2 = r2_score(
    y_test,
    prediction
)



print()

print("======================")

print("Backtest Results")

print("======================")

print()

print(
    f"Date: {forecast_date.date()}"
)


print(
    f"MAE: {mae:.2f} MW"
)


print(
    f"RMSE: {rmse:.2f} MW"
)


print(
    f"R2: {r2:.4f}"
)



# ---------------------------------------
# Save results
# ---------------------------------------

results = pd.DataFrame({

    "datetime":
    test_day["datetime"],

    "actual_load":
    y_test,

    "forecast_load":
    prediction

})


output = (

    BASE_DIR
    /
    "reports"
    /
    country
    /
    "backtest_results.csv"

)


results.to_csv(
    output,
    index=False
)



print()

print(
    f"Saved:\n{output}"
)