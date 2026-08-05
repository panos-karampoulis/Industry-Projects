from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)

from xgboost import XGBRegressor


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


MODEL_DIR = (
    BASE_DIR
    /
    "models"
)

RESULTS_DIR = (
    BASE_DIR
    /
    "results"
)


MODEL_DIR.mkdir(
    exist_ok=True
)

RESULTS_DIR.mkdir(
    exist_ok=True
)



# ==========================================================
# CONFIG
# ==========================================================

COUNTRY = "germany"


TARGET = "load_mw"



# ==========================================================
# LOAD DATA
# ==========================================================

print("=" * 70)
print("GERMANY LOAD FORECASTING ENGINE")
print("=" * 70)


df = pd.read_csv(
    DATA_FILE,
    parse_dates=[
        "timestamp"
    ]
)


df = df.sort_values(
    "timestamp"
)


print(
    "Original shape:",
    df.shape
)



# ==========================================================
# CREATE FORECAST TARGET
# ==========================================================

print("\nCreating target...")


# 24 hours ahead
# data is hourly

df["load_target"] = (
    df[TARGET]
    .shift(-24)
)



# Remove last 24 rows

df = df.dropna()



print(
    "After target creation:",
    df.shape
)



# ==========================================================
# FEATURES
# ==========================================================

FEATURES = [

    # Load history
    "load_mw",
    "load_lag_1",
    "load_lag_24",
    "load_lag_168",

    # Renewable impact
    "wind_generation",
    "solar_generation",
    "renewable_generation",
    "renewable_share",

    # Residual demand
    "residual_load",

    # Price information
    "day_ahead_price",
    "day_ahead_price_lag_1",
    "day_ahead_price_lag_24",

    # Calendar
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



X = df[FEATURES]

y = df["load_target"]



# ==========================================================
# TIME BASED SPLIT
# ==========================================================


split = int(
    len(df) * 0.8
)


X_train = X.iloc[:split]

X_test = X.iloc[split:]


y_train = y.iloc[:split]

y_test = y.iloc[split:]



print(
    "\nTrain:",
    X_train.shape
)


print(
    "Test:",
    X_test.shape
)



# ==========================================================
# METRICS FUNCTION
# ==========================================================


def evaluate(
        name,
        y_true,
        y_pred
):


    mae = mean_absolute_error(
        y_true,
        y_pred
    )


    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )


    mape = (
        mean_absolute_percentage_error(
            y_true,
            y_pred
        )
    )


    print("\n")
    print(name)

    print(
        "MAE:",
        round(mae,2)
    )

    print(
        "RMSE:",
        round(rmse,2)
    )

    print(
        "MAPE:",
        round(mape,4)
    )


    return {

        "model": name,

        "MAE": mae,

        "RMSE": rmse,

        "MAPE": mape

    }




# ==========================================================
# 1. BASELINE
# ==========================================================


print("\nRunning baseline...")


baseline_prediction = (

    df[TARGET]
    .shift(24)
    .iloc[split:]

)


baseline_prediction = baseline_prediction.fillna(
    y_train.mean()
)



results = []


results.append(

    evaluate(
        "Persistence Baseline",
        y_test,
        baseline_prediction
    )

)



# ==========================================================
# 2. RANDOM FOREST
# ==========================================================


print("\nTraining Random Forest...")


rf = RandomForestRegressor(

    n_estimators=200,

    max_depth=15,

    random_state=42,

    n_jobs=-1

)



rf.fit(

    X_train,

    y_train

)



rf_pred = rf.predict(
    X_test
)



results.append(

    evaluate(
        "Random Forest",
        y_test,
        rf_pred
    )

)



# Save RF

joblib.dump(

    rf,

    MODEL_DIR
    /
    f"{COUNTRY}_load_rf.pkl"

)



# ==========================================================
# 3. XGBOOST
# ==========================================================


print("\nTraining XGBoost...")


xgb = XGBRegressor(

    n_estimators=500,

    learning_rate=0.05,

    max_depth=6,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="reg:squarederror",

    random_state=42,

    n_jobs=-1

)



xgb.fit(

    X_train,

    y_train

)



xgb_pred = xgb.predict(
    X_test
)



results.append(

    evaluate(
        "XGBoost",
        y_test,
        xgb_pred
    )

)



# Save model

joblib.dump(

    xgb,

    MODEL_DIR
    /
    f"{COUNTRY}_load_xgb.pkl"

)



# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================


importance = pd.DataFrame({

    "feature": FEATURES,

    "importance": xgb.feature_importances_

})


importance = importance.sort_values(

    "importance",

    ascending=False

)


importance.to_csv(

    RESULTS_DIR
    /
    f"{COUNTRY}_load_feature_importance.csv",

    index=False

)



print("\nTop Features")

print(
    importance.head(10)
)



# ==========================================================
# SAVE METRICS
# ==========================================================


metrics = pd.DataFrame(
    results
)


metrics.to_csv(

    RESULTS_DIR
    /
    "load_forecast_metrics.csv",

    index=False

)



print("\n")
print("=" * 70)
print("LOAD FORECASTING COMPLETED")
print("=" * 70)


print(
    metrics
)


print("\nSaved models:")
print(
    MODEL_DIR
    /
    f"{COUNTRY}_load_xgb.pkl"
)

print(
    MODEL_DIR
    /
    f"{COUNTRY}_load_rf.pkl"
)