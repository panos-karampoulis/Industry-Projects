import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

import joblib


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


INPUT_FILE = (
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

RESULT_DIR = (
    BASE_DIR
    /
    "results"
)


MODEL_DIR.mkdir(
    exist_ok=True
)

RESULT_DIR.mkdir(
    exist_ok=True
)



# ==========================================================
# LOAD DATA
# ==========================================================


print("="*70)
print("GERMANY DAY AHEAD PRICE FORECASTING ENGINE")
print("="*70)


df = pd.read_csv(
    INPUT_FILE
)


print(
    "Original shape:",
    df.shape
)



# ==========================================================
# TARGET CREATION
# ==========================================================

print("\nCreating target...")


# forecast next day price

df["target_price"] = (
    df["day_ahead_price"]
    .shift(-24)
)



df = df.dropna()


print(
    "After target creation:",
    df.shape
)



# ==========================================================
# FEATURES
# ==========================================================


drop_cols = [

    "timestamp",

    "target_price"

]


X = df.drop(
    columns=drop_cols
)


y = df["target_price"]



# keep numerical only

X = X.select_dtypes(
    include=[
        np.number
    ]
)



# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================


split = int(
    len(df)*0.8
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
# BASELINE
# ==========================================================


print("\nRunning baseline...\n")


baseline_pred = (
    df["day_ahead_price"]
    .iloc[split:]
)


baseline_mae = mean_absolute_error(
    y_test,
    baseline_pred
)


baseline_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        baseline_pred
    )
)



baseline_mape = np.mean(
    np.abs(
        (y_test-baseline_pred)
        /
        y_test
    )
)



print("Persistence Baseline")

print(
    "MAE:",
    round(baseline_mae,2)
)

print(
    "RMSE:",
    round(baseline_rmse,2)
)

print(
    "MAPE:",
    round(baseline_mape,4)
)




# ==========================================================
# RANDOM FOREST
# ==========================================================


print("\nTraining Random Forest...\n")


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



rf_mae = mean_absolute_error(
    y_test,
    rf_pred
)


rf_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        rf_pred
    )
)


rf_mape = np.mean(
    np.abs(
        (y_test-rf_pred)
        /
        y_test
    )
)



print("Random Forest")

print(
    "MAE:",
    round(rf_mae,2),
)

print(
    "RMSE:",
    round(rf_rmse,2)
)

print(
    "MAPE:",
    round(rf_mape,4)
)



# ==========================================================
# XGBOOST
# ==========================================================


print("\nTraining XGBoost...\n")


xgb = XGBRegressor(

    n_estimators=500,

    learning_rate=0.03,

    max_depth=6,

    subsample=0.8,

    colsample_bytree=0.8,

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



xgb_mae = mean_absolute_error(
    y_test,
    xgb_pred
)


xgb_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        xgb_pred
    )
)


xgb_mape = np.mean(
    np.abs(
        (y_test-xgb_pred)
        /
        y_test
    )
)



print("XGBoost")

print(
    "MAE:",
    round(xgb_mae,2)
)


print(
    "RMSE:",
    round(xgb_rmse,2)
)


print(
    "MAPE:",
    round(xgb_mape,4)
)



# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================


importance = pd.DataFrame({

    "feature":
    X.columns,

    "importance":
    xgb.feature_importances_

})


importance = importance.sort_values(
    "importance",
    ascending=False
)



print("\nTop Features")

print(
    importance.head(10)
)



# ==========================================================
# SAVE MODELS
# ==========================================================


joblib.dump(

    rf,

    MODEL_DIR /
    "germany_price_rf.pkl"

)


joblib.dump(

    xgb,

    MODEL_DIR /
    "germany_price_xgb.pkl"

)



# ==========================================================
# SAVE RESULTS
# ==========================================================


results = pd.DataFrame({

    "model":[

        "Persistence Baseline",

        "Random Forest",

        "XGBoost"

    ],


    "MAE":[

        baseline_mae,

        rf_mae,

        xgb_mae

    ],


    "RMSE":[

        baseline_rmse,

        rf_rmse,

        xgb_rmse

    ],


    "MAPE":[

        baseline_mape,

        rf_mape,

        xgb_mape

    ]

})


results.to_csv(

    RESULT_DIR /
    "germany_price_forecast_metrics.csv",

    index=False

)



print("\n")
print("="*70)
print("PRICE FORECASTING COMPLETED")
print("="*70)


print(results)


print("\nSaved models:")

print(
    MODEL_DIR /
    "germany_price_rf.pkl"
)

print(
    MODEL_DIR /
    "germany_price_xgb.pkl"
)