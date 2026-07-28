import pandas as pd
import numpy as np
import os

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)



# ============================================================
# PATHS
# ============================================================

INPUT_FILE = (
    "data/features/germany_features.csv"
)


OUTPUT_FILE = (
    "results/baseline_results.csv"
)



# ============================================================
# LOAD DATA
# ============================================================

print("="*70)
print("BASELINE FORECASTING MODELS")
print("="*70)


df = pd.read_csv(
    INPUT_FILE,
    index_col=0,
    parse_dates=True
)


df = df.sort_index()


print("\nDataset:")
print(df.shape)



# ============================================================
# TRAIN TEST SPLIT
# ============================================================

print("\nCreating train/test split...")


# last 20% for testing

split = int(
    len(df) * 0.8
)


train = df.iloc[:split]


test = df.iloc[split:]


print(
    "Train:",
    train.shape
)


print(
    "Test:",
    test.shape
)



# ============================================================
# TARGET
# ============================================================

y_test = test[
    "price_eur_mwh"
]



# ============================================================
# MODEL 1
# NAIVE LAST HOUR
# ============================================================


print("\nModel 1: Previous Hour")


pred_previous = (
    test["price_lag_1"]
)



# ============================================================
# MODEL 2
# SAME HOUR YESTERDAY
# ============================================================


print("Model 2: Previous Day")


pred_day = (
    test["price_lag_24"]
)



# ============================================================
# MODEL 3
# SAME HOUR LAST WEEK
# ============================================================


print("Model 3: Previous Week")


pred_week = (
    test["price_lag_168"]
)



# ============================================================
# EVALUATION FUNCTION
# ============================================================


def evaluate(
    actual,
    prediction,
    name
):


    mae = mean_absolute_error(
        actual,
        prediction
    )


    rmse = np.sqrt(
        mean_squared_error(
            actual,
            prediction
        )
    )


    mape = mean_absolute_percentage_error(
        actual,
        prediction
    )


    return {

        "model": name,

        "MAE": mae,

        "RMSE": rmse,

        "MAPE": mape

    }



# ============================================================
# RESULTS
# ============================================================


results = []


results.append(
    evaluate(
        y_test,
        pred_previous,
        "Previous Hour"
    )
)


results.append(
    evaluate(
        y_test,
        pred_day,
        "Previous Day"
    )
)


results.append(
    evaluate(
        y_test,
        pred_week,
        "Previous Week"
    )
)



results_df = pd.DataFrame(
    results
)



# ============================================================
# PRINT RESULTS
# ============================================================


print("\nRESULTS")

print(
    results_df
)



# ============================================================
# SAVE
# ============================================================


os.makedirs(
    "results",
    exist_ok=True
)


results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved:")
print(
    OUTPUT_FILE
)


print("\nDONE")