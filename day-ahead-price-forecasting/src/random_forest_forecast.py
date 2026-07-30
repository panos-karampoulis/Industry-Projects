# ============================================================
# RANDOM FOREST FORECASTING
# Day Ahead Price Forecasting
# Multi Country Version
# ============================================================

import pandas as pd
import numpy as np
import os
import argparse
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


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
    f"{MODEL_DIR}/random_forest_model.pkl"
)


RESULT_PATH = (
    f"{RESULT_DIR}/random_forest_results.csv"
)


PRED_PATH = (
    f"{RESULT_DIR}/random_forest_predictions.csv"
)



# ============================================================
# LOAD DATA
# ============================================================

print("="*70)
print("RANDOM FOREST FORECASTING")
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



# ============================================================
# REMOVE NON NUMERIC
# ============================================================

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
print(X_train.shape)


print("Test:")
print(X_test.shape)



# ============================================================
# MODEL
# ============================================================

print("\nTraining Random Forest...")


model = RandomForestRegressor(

    n_estimators=200,

    max_depth=15,

    random_state=42,

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

    f"results/{country}/random_forest_feature_importance.csv",

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
        "Random Forest"
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
# SAVE FORECASTS
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