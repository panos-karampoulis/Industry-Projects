import pandas as pd
import numpy as np

from pathlib import Path

import joblib

from feature_engineering import create_features


# -------------------------
# Paths
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


DATA_FILE = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "renewable_forecasting_dataset.csv"
)


MODEL_FILE = (
    BASE_DIR
    /
    "models"
    /
    "xgboost_renewable_forecaster.pkl"
)


FEATURE_FILE = (
    BASE_DIR
    /
    "models"
    /
    "model_features.pkl"
)


REPORT_DIR = (
    BASE_DIR
    /
    "reports"
)


REPORT_DIR.mkdir(
    exist_ok=True
)


OUTPUT_FILE = (
    REPORT_DIR
    /
    "renewable_forecast_results.csv"
)


# -------------------------
# Load Data
# -------------------------

print("Loading dataset...")


df = pd.read_csv(
    DATA_FILE,
    parse_dates=["datetime"]
)


# -------------------------
# Feature Engineering
# -------------------------

print("Creating features...")


df = create_features(df)



# -------------------------
# Select Forecast Period
# -------------------------

forecast = df[
    df["datetime"] >= "2025-01-01"
].copy()



# -------------------------
# Prepare Features
# -------------------------

target = "renewable_total_mwh"


drop_cols = [

    "datetime",
    "country",

    target,

    "solar_mwh",
    "wind_onshore_mwh",
    "wind_offshore_mwh",
    "wind_total_mwh"

]


X = forecast.drop(
    columns=drop_cols,
    errors="ignore"
)



# -------------------------
# Load Model
# -------------------------

print("Loading model...")


model = joblib.load(
    MODEL_FILE
)


features = joblib.load(
    FEATURE_FILE
)


X = X[features]



# -------------------------
# Prediction
# -------------------------

print("Generating forecast...")


prediction = model.predict(
    X
)



# -------------------------
# Create Report
# -------------------------

result = pd.DataFrame({

    "datetime":
        forecast["datetime"].values,

    "renewable_total_mwh":
        forecast[target].values,

    "prediction_mwh":
        prediction

})


result["error_mwh"] = (
    result["renewable_total_mwh"]
    -
    result["prediction_mwh"]
)


result["absolute_error"] = (
    result["error_mwh"]
    .abs()
)



# -------------------------
# Save
# -------------------------

result.to_csv(
    OUTPUT_FILE,
    index=False
)



print()
print("Forecast generated successfully")
print(
    OUTPUT_FILE
)


print()
print(result.head(10))