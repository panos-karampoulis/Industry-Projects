import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

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


MODEL_DIR = (
    BASE_DIR
    /
    "models"
)


MODEL_DIR.mkdir(
    exist_ok=True
)


MODEL_FILE = (
    MODEL_DIR
    /
    "xgboost_renewable_forecaster.pkl"
)


FEATURE_FILE = (
    MODEL_DIR
    /
    "model_features.pkl"
)


# -------------------------
# Load Data
# -------------------------

print("Loading dataset...")


df = pd.read_csv(
    DATA_FILE,
    parse_dates=["datetime"]
)


print(
    "Original shape:",
    df.shape
)


# -------------------------
# Feature Engineering
# -------------------------

print("Creating features...")


df = create_features(df)


print(
    "Feature dataset:",
    df.shape
)


# -------------------------
# Train / Test Split
# -------------------------

train = df[
    df["datetime"] < "2025-01-01"
].copy()


test = df[
    df["datetime"] >= "2025-01-01"
].copy()


print()
print("Train:")
print(
    train["datetime"].min(),
    train["datetime"].max()
)


print("Test:")
print(
    test["datetime"].min(),
    test["datetime"].max()
)



# -------------------------
# Target
# -------------------------

target = "renewable_total_mwh"



# -------------------------
# Remove non features
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


X_train = train.drop(
    columns=drop_cols,
    errors="ignore"
)


X_test = test.drop(
    columns=drop_cols,
    errors="ignore"
)


y_train = train[target]

y_test = test[target]


print()
print(
    "X_train:",
    X_train.shape
)

print(
    "X_test:",
    X_test.shape
)



# -------------------------
# XGBoost Model
# -------------------------

print()
print("Training XGBoost...")


model = XGBRegressor(

    n_estimators=500,

    learning_rate=0.05,

    max_depth=8,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="reg:squarederror",

    random_state=42,

    n_jobs=-1

)



model.fit(
    X_train,
    y_train
)



# -------------------------
# Evaluation
# -------------------------

pred = model.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    pred
)


rmse = np.sqrt(
    mean_squared_error(
        y_test,
        pred
    )
)


r2 = r2_score(
    y_test,
    pred
)


print()
print("MODEL RESULTS")
print("----------------")
print(f"MAE : {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²  : {r2:.4f}")



# -------------------------
# Feature Importance
# -------------------------

importance = (

    pd.Series(
        model.feature_importances_,
        index=X_train.columns
    )

    .sort_values(
        ascending=False
    )

)


print()
print("Top Features")
print(
    importance.head(20)
)



# -------------------------
# Save Model
# -------------------------

print()
print("Saving model...")


joblib.dump(
    model,
    MODEL_FILE
)


joblib.dump(
    X_train.columns.tolist(),
    FEATURE_FILE
)


print()
print("DONE")
print(
    "Model saved:",
    MODEL_FILE
)