# ============================================================
# XGBOOST FORECASTING
# Day Ahead Price Forecasting
# Multi Country Version
# ============================================================

import pandas as pd
import numpy as np
import os
import argparse
import pickle

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)



# ============================================================
# ARGUMENTS
# ============================================================

parser = argparse.ArgumentParser()

parser.add_argument(
    "--country",
    required=True,
    type=str
)


args = parser.parse_args()

country = args.country.lower()



# ============================================================
# PATHS
# ============================================================

DATA_FILE = (
    f"data/features/{country}_features.csv"
)


MODEL_DIR = (
    f"models/{country}"
)


RESULT_DIR = (
    f"results/{country}"
)


os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


os.makedirs(
    RESULT_DIR,
    exist_ok=True
)



MODEL_PATH = (
    f"{MODEL_DIR}/xgboost_model.pkl"
)


RESULT_PATH = (
    f"{RESULT_DIR}/xgboost_results.csv"
)


PRED_PATH = (
    f"{RESULT_DIR}/xgboost_predictions.csv"
)



# ============================================================
# LOAD DATA
# ============================================================

print("="*70)
print("XGBOOST FORECASTING")
print("="*70)


print(
    f"\nCountry: {country}"
)


df = pd.read_csv(
    DATA_FILE,
    index_col=0,
    parse_dates=True
)


df = df.sort_index()


print("\nDataset:")
print(df.shape)



# ============================================================
# TARGET
# ============================================================

target = "price_eur_mwh"


X = df.drop(
    columns=[target]
)


y = df[target]



# Keep numerical features only

X = X.select_dtypes(
    include=np.number
)


print("\nFeatures:")
print(
    X.shape[1]
)



# ============================================================
# TRAIN TEST SPLIT
# ============================================================

split = int(
    len(df) * 0.8
)



X_train = X.iloc[:split]

X_test = X.iloc[split:]


y_train = y.iloc[:split]

y_test = y.iloc[split:]



print("\nTrain:")
print(
    X_train.shape
)


print("Test:")
print(
    X_test.shape
)



# ============================================================
# MODEL
# ============================================================

print("\nTraining XGBoost...")


model = XGBRegressor(

    n_estimators=300,

    learning_rate=0.05,

    max_depth=6,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42,

    objective="reg:squarederror",

    n_jobs=-1

)



model.fit(

    X_train,

    y_train

)


print(
    "Training completed"
)

# ============================================================
# FEATURE IMPORTANCE
# ============================================================


importance = pd.DataFrame({

    "feature": X_train.columns,

    "importance": model.feature_importances_

})


importance = importance.sort_values(

    by="importance",

    ascending=False

)



importance.to_csv(

    f"results/{country}/xgboost_feature_importance.csv",

    index=False

)


# ============================================================
# FORECAST
# ============================================================

forecast = model.predict(
    X_test
)



# ============================================================
# METRICS
# ============================================================

mae = mean_absolute_error(

    y_test,

    forecast

)


rmse = np.sqrt(

    mean_squared_error(

        y_test,

        forecast

    )

)



print("\nRESULTS")

print(
    f"MAE: {mae:.4f}"
)


print(
    f"RMSE: {rmse:.4f}"
)



# ============================================================
# FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({

    "feature":
        X.columns,

    "importance":
        model.feature_importances_

})


importance = importance.sort_values(

    "importance",

    ascending=False

)



print("\nTOP FEATURES")

print(
    importance.head(10)
)



# ============================================================
# SAVE MODEL
# ============================================================

with open(

    MODEL_PATH,

    "wb"

) as f:

    pickle.dump(

        model,

        f

    )



# ============================================================
# SAVE RESULTS
# ============================================================

results = pd.DataFrame({

    "model":[
        "XGBoost"
    ],

    "country":[
        country
    ],

    "MAE":[
        mae
    ],

    "RMSE":[
        rmse
    ]

})


results.to_csv(

    RESULT_PATH,

    index=False

)



# ============================================================
# SAVE PREDICTIONS
# ============================================================

predictions = pd.DataFrame({

    "actual":
        y_test,

    "forecast":
        forecast

})


predictions.to_csv(

    PRED_PATH

)



print("\nSaved:")

print(
    MODEL_PATH
)

print(
    RESULT_PATH
)

print(
    PRED_PATH
)



print("\nDONE")