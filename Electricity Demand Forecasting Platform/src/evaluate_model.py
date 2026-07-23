import pandas as pd
import joblib

from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"



# ---------------------------------------
# Load data
# ---------------------------------------

print("Loading test dataset...")


features_file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    country
    /
    "load_features.csv"
)


df = pd.read_csv(
    features_file,
    parse_dates=["datetime"]
)


df = df.sort_values(
    "datetime"
)



# ---------------------------------------
# Test period
# ---------------------------------------

test = df[
    df["datetime"] >= "2025-01-01"
].copy()



# ---------------------------------------
# Prepare features
# ---------------------------------------

target = "target_load"


drop_columns = [
    "datetime",
    "target_load",
    "load_mwh"
]


features = [
    col for col in df.columns
    if col not in drop_columns
]


X_test = test[features]

y_test = test[target]



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

print("Generating predictions...")


prediction = model.predict(
    X_test
)



# ---------------------------------------
# Results dataframe
# ---------------------------------------

results = pd.DataFrame({

    "datetime":
    test["datetime"],

    "actual_load_mwh":
    y_test,

    "prediction_mwh":
    prediction

})


results["error_mwh"] = (
    results["actual_load_mwh"]
    -
    results["prediction_mwh"]
)


results["absolute_error"] = (
    results["error_mwh"]
    .abs()
)



# ---------------------------------------
# Metrics
# ---------------------------------------

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



print()

print("Evaluation results")

print(
    f"MAE: {mae:.2f} MWh"
)

print(
    f"RMSE: {rmse:.2f} MWh"
)

print(
    f"R2: {r2:.4f}"
)



# ---------------------------------------
# Save results
# ---------------------------------------

output_dir = (
    BASE_DIR
    /
    "reports"
    /
    country
)


output_dir.mkdir(
    parents=True,
    exist_ok=True
)


output_file = (
    output_dir
    /
    "load_forecast_results.csv"
)


results.to_csv(
    output_file,
    index=False
)



print()

print(
    f"Saved:\n{output_file}"
)