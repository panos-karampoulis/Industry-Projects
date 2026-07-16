import pandas as pd
import numpy as np

from pathlib import Path

import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

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


# -------------------------
# Load Data
# -------------------------

print("Loading dataset...")


df = pd.read_csv(
    DATA_FILE,
    parse_dates=["datetime"]
)


df = create_features(df)


# -------------------------
# Test Period
# -------------------------

test = df[
    df["datetime"] >= "2025-01-01"
].copy()


target = "renewable_total_mwh"



# -------------------------
# Prepare Features
# -------------------------

drop_cols = [

    "datetime",
    "country",

    "renewable_total_mwh",

    "solar_mwh",
    "wind_onshore_mwh",
    "wind_offshore_mwh",
    "wind_total_mwh"

]


X_test = test.drop(
    columns=drop_cols,
    errors="ignore"
)


y_test = test[target]



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


X_test = X_test[features]



# -------------------------
# Prediction
# -------------------------

prediction = model.predict(
    X_test
)



# -------------------------
# Metrics
# -------------------------

mae = mean_absolute_error(
    y_test,
    prediction
)


rmse = np.sqrt(
    mean_squared_error(
        y_test,
        prediction
    )
)


r2 = r2_score(
    y_test,
    prediction
)


metrics = pd.DataFrame({

    "MAE": [mae],

    "RMSE": [rmse],

    "R2": [r2]

})


metrics.to_csv(
    REPORT_DIR /
    "model_metrics.csv",
    index=False
)



print()
print("MODEL METRICS")
print("----------------")
print(metrics)



# -------------------------
# Residual Analysis
# -------------------------

residuals = (
    y_test.values
    -
    prediction
)


residual_report = pd.DataFrame({

    "datetime":
        test["datetime"],

    "actual":
        y_test.values,

    "prediction":
        prediction,

    "error":
        residuals,

    "absolute_error":
        np.abs(residuals)

})


residual_report.to_csv(
    REPORT_DIR /
    "residual_analysis.csv",
    index=False
)



# -------------------------
# Feature Importance
# -------------------------

importance = pd.DataFrame({

    "feature":
        features,

    "importance":
        model.feature_importances_

})


importance = importance.sort_values(
    "importance",
    ascending=False
)


importance.to_csv(
    REPORT_DIR /
    "feature_importance.csv",
    index=False
)



print()
print("Reports saved successfully")