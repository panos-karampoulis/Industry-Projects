import pandas as pd
import joblib
from pathlib import Path


# ==========================
# PATHS
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent


DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "renewable_forecasting_features.csv"
)


MODEL_FILE = (
    BASE_DIR
    / "models"
    / "xgboost_renewable_forecaster.pkl"
)


FEATURE_FILE = (
    BASE_DIR
    / "models"
    / "model_features.pkl"
)


REPORT_DIR = (
    BASE_DIR
    / "reports"
)


REPORT_DIR.mkdir(
    exist_ok=True
)


# ==========================
# LOAD DATA
# ==========================

print("Loading dataset...")


df = pd.read_csv(
    DATA_FILE,
    parse_dates=["datetime"]
)


print(
    "Dataset shape:",
    df.shape
)


# ==========================
# TEST PERIOD
# ==========================

test = df[
    df["datetime"] >= "2025-01-01"
].copy()


print(
    "Test samples:",
    len(test)
)


# ==========================
# LOAD MODEL
# ==========================

print("Loading model...")


model = joblib.load(
    MODEL_FILE
)


features = joblib.load(
    FEATURE_FILE
)


print(
    "Features used:",
    len(features)
)


# ==========================
# PREDICTION
# ==========================

print("Generating predictions...")


X_test = test[
    features
]


test["prediction_mwh"] = (
    model.predict(X_test)
)


# ==========================
# ERRORS
# ==========================

test["error_mwh"] = (
    test["renewable_total_mwh"]
    -
    test["prediction_mwh"]
)


test["absolute_error"] = (
    test["error_mwh"]
    .abs()
)


# ==========================
# SAVE HOURLY RESULTS
# ==========================

hourly_file = (
    REPORT_DIR
    /
    "renewable_forecast_results.csv"
)


test[
    [
        "datetime",
        "renewable_total_mwh",
        "prediction_mwh",
        "error_mwh",
        "absolute_error"
    ]
].to_csv(
    hourly_file,
    index=False
)


print(
    "Saved:",
    hourly_file
)


# ==========================
# DAILY SUMMARY
# ==========================

daily = (
    test
    .set_index("datetime")
    [
        [
            "renewable_total_mwh",
            "prediction_mwh"
        ]
    ]
    .resample("D")
    .sum()
)


daily["error_mwh"] = (
    daily["prediction_mwh"]
    -
    daily["renewable_total_mwh"]
)


daily["error_percent"] = (
    daily["error_mwh"]
    /
    daily["renewable_total_mwh"]
    *
    100
)


daily_file = (
    REPORT_DIR
    /
    "daily_forecast_summary.csv"
)


daily.to_csv(
    daily_file
)


print(
    "Saved:",
    daily_file
)


# ==========================
# SUMMARY
# ==========================

print("\nForecast completed!")

print(
    "\nFirst daily results:"
)

print(
    daily.head()
)


forecast = pd.read_csv(
    "reports/renewable_forecast_results.csv",
    parse_dates=["datetime"]
)

forecast.head(10)