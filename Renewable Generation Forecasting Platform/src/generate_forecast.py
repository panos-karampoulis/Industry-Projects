import pandas as pd
import numpy as np
import argparse
import yaml

from pathlib import Path

import joblib

from feature_engineering import create_features


# -------------------------
# Paths
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------
# Arguments
# -------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--country",
    default="germany"
)

args = parser.parse_args()

COUNTRY = args.country



# -------------------------
# Load Config
# -------------------------

CONFIG_FILE = (
    BASE_DIR
    /
    "configs"
    /
    f"{COUNTRY}.yaml"
)


with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)


print(
    "Using configuration:",
    COUNTRY
)



# -------------------------
# Paths
# -------------------------

DATA_FILE = (
    BASE_DIR
    /
    config["data"]["file"]
)


MODEL_FILE = (
    BASE_DIR
    /
    "models"
    /
    COUNTRY
    /
    config["model"]["name"]
)


FEATURE_FILE = (
    BASE_DIR
    /
    "models"
    /
    COUNTRY
    /
    "model_features.pkl"
)


REPORT_DIR = (
    BASE_DIR
    /
    "reports"
    /
    COUNTRY
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

test_start = pd.to_datetime(
    config["split"]["test_start"]
)


forecast = df[
    df["datetime"] >= test_start
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


# -------------------------
# Create Daily Summary
# -------------------------

daily_summary = (
    result
    .assign(
        date=result["datetime"].dt.date
    )
    .groupby("date")
    .agg(
        actual_mwh=(
            "renewable_total_mwh",
            "sum"
        ),
        prediction_mwh=(
            "prediction_mwh",
            "sum"
        ),
        error_mwh=(
            "error_mwh",
            "sum"
        ),
        absolute_error_mwh=(
            "absolute_error",
            "sum"
        )
    )
    .reset_index()
)


DAILY_OUTPUT = (
    REPORT_DIR
    /
    "daily_summary.csv"
)


daily_summary.to_csv(
    DAILY_OUTPUT,
    index=False
)


print(
    "Daily summary saved:",
    DAILY_OUTPUT
)


print()
print("Forecast generated successfully")
print(
    OUTPUT_FILE
)


print()
print(result.head(10))