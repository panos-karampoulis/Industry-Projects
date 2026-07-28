import os
import sys
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score
)

from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor

import joblib



# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


sys.path.append(BASE_DIR)



# ==========================================================
# PATHS
# ==========================================================

FEATURE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "features"
)


RESULT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "results",
    "day_ahead"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "day_ahead"
)


os.makedirs(
    RESULT_DIR,
    exist_ok=True
)


os.makedirs(
    MODEL_DIR,
    exist_ok=True
)



# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]



# ==========================================================
# FEATURES
# ==========================================================

FEATURES = [

    "hour",

    "day_of_week",

    "month",

    "day_of_year",

    "lag_1",

    "lag_24",

    "lag_48",

    "lag_168",

    "rolling_mean_24",

    "rolling_std_24"

]



TARGET = "target"



# ==========================================================
# TRAIN FUNCTION
# ==========================================================

def train_country(country):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    file_path = os.path.join(

        FEATURE_DIR,

        f"{country}_day_ahead_features.csv"

    )



    df = pd.read_csv(

        file_path

    )



    df["timestamp"] = pd.to_datetime(

        df["timestamp"]

    )



    df = df.sort_values(

        "timestamp"

    )



    X = df[FEATURES]

    y = df[TARGET]



    # ------------------------------------------------------
    # TIME SPLIT
    # ------------------------------------------------------

    split = int(

        len(df) * 0.8

    )



    X_train = X.iloc[:split]

    X_test = X.iloc[split:]


    y_train = y.iloc[:split]

    y_test = y.iloc[split:]



    results = []



    # ======================================================
    # BASELINE
    # ======================================================

    baseline_pred = (

        df["lag_24"]

        .iloc[split:]

    )


    baseline_mae = mean_absolute_error(

        y_test,

        baseline_pred

    )


    results.append(

        {

        "country":country,

        "model":"Baseline",

        "MAE":baseline_mae

        }

    )



    # ======================================================
    # RANDOM FOREST
    # ======================================================

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



    # ======================================================
    # XGBOOST
    # ======================================================

    xgb = XGBRegressor(

        n_estimators=500,

        learning_rate=0.05,

        max_depth=6,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42,

        objective="reg:squarederror",

        n_jobs=-1

    )


    xgb.fit(

        X_train,

        y_train

    )


    xgb_pred = xgb.predict(

        X_test

    )



    # ======================================================
    # METRICS
    # ======================================================

    models = {

        "Random_Forest": rf_pred,

        "XGBoost": xgb_pred

    }



    for name, pred in models.items():


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


        mape = mean_absolute_percentage_error(

            y_test,

            pred

        )


        r2 = r2_score(

            y_test,

            pred

        )



        print()

        print(name)

        print(
            "MAE:",
            round(mae,3)
        )

        print(
            "RMSE:",
            round(rmse,3)
        )

        print(
            "MAPE:",
            round(mape,4)
        )

        print(
            "R2:",
            round(r2,4)
        )



        results.append(

            {

            "country":country,

            "model":name,

            "MAE":mae,

            "RMSE":rmse,

            "MAPE":mape,

            "R2":r2

            }

        )



    # ======================================================
    # SAVE BEST MODEL
    # ======================================================

    best_model = xgb



    model_path = os.path.join(

        MODEL_DIR,

        f"{country}_xgb_day_ahead.pkl"

    )


    joblib.dump(

        best_model,

        model_path

    )



    print()

    print(
        "Saved model:",
        model_path
    )



    # ======================================================
    # SAVE TEST FORECASTS
    # ======================================================

    forecast = pd.DataFrame(

        {

        "timestamp":
        df["timestamp"].iloc[split:].values,

        "actual":
        y_test.values,

        "prediction":
        xgb_pred

        }

    )


    forecast.to_csv(

        os.path.join(

            RESULT_DIR,

            f"{country}_day_ahead_predictions.csv"

        ),

        index=False

    )



    return results





# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    all_results = []


    for country in COUNTRIES:


        res = train_country(

            country

        )


        all_results.extend(

            res

        )



    metrics = pd.DataFrame(

        all_results

    )


    metrics.to_csv(

        os.path.join(

            RESULT_DIR,

            "day_ahead_metrics.csv"

        ),

        index=False

    )


    print("\n")
    print("="*60)
    print("DAY AHEAD FORECASTING COMPLETED")
    print("="*60)