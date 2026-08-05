import pandas as pd
import numpy as np

from pathlib import Path
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from xgboost import XGBRegressor


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


FEATURES_DIR = (
    BASE_DIR
    /
    "data"
    /
    "features"
)


MODELS_DIR = (
    BASE_DIR
    /
    "models"
)


RESULTS_DIR = (
    BASE_DIR
    /
    "results"
)


RESULTS_DIR.mkdir(
    exist_ok=True
)



# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"

]



# ==========================================================
# FEATURES
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



# ==========================================================
# METRICS
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


    mape = np.mean(
        np.abs(
            (y_true - y_pred)
            /
            y_true
        )
    )


    print()
    print(name)

    print(
        f"MAE: {mae:.2f}"
    )

    print(
        f"RMSE: {rmse:.2f}"
    )

    print(
        f"MAPE: {mape:.4f}"
    )


    return {

        "model": name,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape

    }




# ==========================================================
# COUNTRY FORECASTING
# ==========================================================

def run_country(country):


    print("\n")
    print("="*70)
    print(
        country.upper(),
        "LOAD FORECASTING"
    )
    print("="*70)



    # ------------------------------------------------------
    # LOAD DATA
    # ------------------------------------------------------

    file = (

        FEATURES_DIR
        /
        f"{country}_features.csv"

    )


    df = pd.read_csv(
        file
    )


    print(
        "Original shape:",
        df.shape
    )



    # ------------------------------------------------------
    # TARGET
    # next hour load
    # ------------------------------------------------------

    df["target_load"] = (

        df["load_mw"]
        .shift(-1)

    )


    df = df.dropna()



    # ------------------------------------------------------
    # FEATURES
    # ------------------------------------------------------

    X = df[
        LOAD_FEATURES
    ]


    y = df[
        "target_load"
    ]



    # ------------------------------------------------------
    # TRAIN TEST SPLIT
    # time based
    # ------------------------------------------------------

    split = int(
        len(df)
        *
        0.8
    )


    X_train = X.iloc[:split]

    X_test = X.iloc[split:]


    y_train = y.iloc[:split]

    y_test = y.iloc[split:]



    print(
        "Train:",
        X_train.shape
    )


    print(
        "Test:",
        X_test.shape
    )



    results = []



    # ------------------------------------------------------
    # RANDOM FOREST
    # ------------------------------------------------------

    rf = RandomForestRegressor(

        n_estimators=200,

        random_state=42,

        n_jobs=-1

    )


    rf.fit(
        X_train,
        y_train
    )


    pred_rf = rf.predict(
        X_test
    )


    results.append(

        evaluate(
            "Random Forest",
            y_test,
            pred_rf
        )

    )



    # ------------------------------------------------------
    # XGBOOST
    # ------------------------------------------------------

    xgb = XGBRegressor(

        n_estimators=300,

        learning_rate=0.05,

        max_depth=6,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42,

        objective="reg:squarederror"

    )


    xgb.fit(

        X_train,

        y_train

    )


    pred_xgb = xgb.predict(
        X_test
    )



    results.append(

        evaluate(
            "XGBoost",
            y_test,
            pred_xgb
        )

    )



    # ------------------------------------------------------
    # SAVE MODELS
    # ------------------------------------------------------

    country_model_dir = (

        MODELS_DIR
        /
        country

    )


    country_model_dir.mkdir(

        exist_ok=True,

        parents=True

    )



    joblib.dump(

        rf,

        country_model_dir
        /
        f"{country}_load_rf.pkl"

    )


    joblib.dump(

        xgb,

        country_model_dir
        /
        f"{country}_load_xgb.pkl"

    )



    joblib.dump(

        LOAD_FEATURES,

        country_model_dir
        /
        f"{country}_load_features.pkl"

    )



    # ------------------------------------------------------
    # SAVE RESULTS
    # ------------------------------------------------------

    results_df = pd.DataFrame(
        results
    )


    results_df.to_csv(

        RESULTS_DIR
        /
        f"{country}_load_forecast_results.csv",

        index=False

    )



    print()

    print(
        "Saved models:"
    )


    print(
        country_model_dir
    )


    print(
        results_df
    )





# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:


        try:

            run_country(
                country
            )


        except Exception as e:


            print()

            print(
                country.upper(),
                "FAILED"
            )

            print(e)