import pandas as pd
import numpy as np

from pathlib import Path
import joblib



# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


DATA_FILE = (
    BASE_DIR
    /
    "data"
    /
    "features"
    /
    "germany_features.csv"
)


MODEL_FILE = (
    BASE_DIR
    /
    "models"
    /
    "germany_load_xgb.pkl"
)


RESULT_DIR = (
    BASE_DIR
    /
    "results"
)


RESULT_DIR.mkdir(
    exist_ok=True
)



# ==========================================================
# LOAD DATA
# ==========================================================


print("="*70)
print("GERMANY IMBALANCE RISK ENGINE")
print("="*70)



df = pd.read_csv(
    DATA_FILE
)



print(
    "Dataset:",
    df.shape
)



# ==========================================================
# LOAD MODEL
# ==========================================================


print("\nLoading load forecasting model...")


model = joblib.load(
    MODEL_FILE
)



print(
    "Model loaded"
)



# ==========================================================
# PREPARE FEATURES
# ==========================================================


LOAD_FEATURES = [

    "load_mw",
    "load_lag_1",
    "load_lag_24",
    "load_lag_168",

    "wind_generation",
    "solar_generation",
    "renewable_generation",

    "renewable_share",
    "residual_load",

    "day_ahead_price",

    "day_ahead_price_lag_1",
    "day_ahead_price_lag_24",

    "hour",
    "day_of_week",
    "month",
    "weekend",

    "hour_sin",
    "hour_cos",

    "dow_sin",
    "dow_cos",

    "month_sin",
    "month_cos"

]


X = df[
    LOAD_FEATURES
]


actual_load = df["load_mw"]

# ==========================================================
# FORECAST LOAD
# ==========================================================


print("\nGenerating forecasts...")


forecast_load = model.predict(
    X
)



df["forecast_load"] = (
    forecast_load
)



# ==========================================================
# IMBALANCE CALCULATION
# ==========================================================


print(
    "\nCalculating imbalance..."
)



df["imbalance_mw"] = (

    df["load_mw"]

    -

    df["forecast_load"]

)



df["abs_imbalance_mw"] = (

    df["imbalance_mw"]
    .abs()

)



# ==========================================================
# FINANCIAL RISK
# ==========================================================


df["imbalance_cost_eur"] = (

    df["abs_imbalance_mw"]

    *

    df["day_ahead_price"]

)



# ==========================================================
# RISK SCORE
# ==========================================================


percentile_90 = (

    df["abs_imbalance_mw"]
    .quantile(0.90)

)



df["risk_score"] = (

    df["abs_imbalance_mw"]

    /

    percentile_90

    *

    10

)



df["risk_score"] = (

    df["risk_score"]
    .clip(
        0,
        10
    )

)



# Risk category


def risk_level(x):

    if x < 3:
        return "LOW"

    elif x < 7:
        return "MEDIUM"

    else:
        return "HIGH"



df["risk_level"] = (

    df["risk_score"]
    .apply(
        risk_level
    )

)



# ==========================================================
# SAVE RESULTS
# ==========================================================


output = (

    RESULT_DIR
    /
    "germany_imbalance_risk.csv"

)



df[

    [

        "timestamp",

        "load_mw",

        "forecast_load",

        "imbalance_mw",

        "abs_imbalance_mw",

        "day_ahead_price",

        "imbalance_cost_eur",

        "risk_score",

        "risk_level"

    ]

].to_csv(

    output,

    index=False

)



# ==========================================================
# SUMMARY
# ==========================================================


print("\n")
print("="*70)
print("IMBALANCE RISK COMPLETED")
print("="*70)



print(
    df[
        [
            "imbalance_mw",
            "imbalance_cost_eur",
            "risk_score"
        ]
    ]
    .describe()
)



print("\nRisk distribution")

print(
    df["risk_level"]
    .value_counts()
)



print("\nSaved:")

print(output)