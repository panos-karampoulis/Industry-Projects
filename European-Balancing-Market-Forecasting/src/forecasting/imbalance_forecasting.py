import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


import pandas as pd
import numpy as np

import joblib


from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor


from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


from src.config.countries import (
    get_active_countries
)



# ============================================================
# PATHS
# ============================================================


DATA_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "balancing"
)


MODEL_DIR = (
    BASE_DIR
    /
    "models"
    /
    "imbalance_forecasting"
)


MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# LOAD DATA
# ============================================================


def load_data(country):


    path = (
        DATA_DIR
        /
        f"{country}_imbalance.csv"
    )


    df = pd.read_csv(
        path
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )


    df = df.sort_values(
        "timestamp"
    )


    return df




# ============================================================
# FEATURE CREATION
# ============================================================


def create_features(df):


    df = df.copy()



    # lag imbalance

    df["imbalance_lag_1"] = (
        df["imbalance_mw"]
        .shift(1)
    )


    df["imbalance_lag_4"] = (
        df["imbalance_mw"]
        .shift(4)
    )


    df["imbalance_lag_96"] = (
        df["imbalance_mw"]
        .shift(96)
    )



    # rolling behaviour

    df["imbalance_mean_24"] = (

        df["imbalance_mw"]
        .rolling(24)
        .mean()

    )


    df["imbalance_std_24"] = (

        df["imbalance_mw"]
        .rolling(24)
        .std()

    )



    return df.dropna()





# ============================================================
# TRAIN MODELS
# ============================================================


def train_country(country):


    print()
    print("="*70)
    print(
        f"TRAINING IMBALANCE: {country.upper()}"
    )
    print("="*70)



    df = load_data(
        country
    )


    df = create_features(
        df
    )



    target = (
        "imbalance_mw"
    )



    features = [

        "forecast_load_mw",

        "hour",

        "weekday",

        "month",

        "imbalance_lag_1",

        "imbalance_lag_4",

        "imbalance_lag_96",

        "imbalance_mean_24",

        "imbalance_std_24"

    ]



    X = df[features]

    y = df[target]



    split = int(
        len(df) * 0.8
    )


    X_train = X.iloc[:split]

    X_test = X.iloc[split:]


    y_train = y.iloc[:split]

    y_test = y.iloc[split:]




    models = {


        "linear_regression":
            LinearRegression(),


        "random_forest":
            RandomForestRegressor(

                n_estimators=100,

                random_state=42,

                n_jobs=-1

            ),



        "xgboost":
            XGBRegressor(

                n_estimators=300,

                learning_rate=0.05,

                max_depth=6,

                random_state=42,

                n_jobs=-1

            )

    }



    results = []



    country_dir = (
        MODEL_DIR
        /
        country
    )


    country_dir.mkdir(
        parents=True,
        exist_ok=True
    )




    for name, model in models.items():


        print(
            f"Training {name}"
        )


        model.fit(

            X_train,

            y_train

        )


        prediction = model.predict(
            X_test
        )



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



        results.append({

            "model": name,

            "MAE": mae,

            "RMSE": rmse

        })



        joblib.dump(

            model,

            country_dir
            /
            f"{name}.pkl"

        )



    metrics = pd.DataFrame(
        results
    )


    metrics.to_csv(

        country_dir
        /
        "metrics.csv",

        index=False

    )



    print()

    print(metrics)



    print(
        "MODELS SAVED"
    )




# ============================================================
# MAIN
# ============================================================


def main():


    countries = get_active_countries()



    for country in countries:


        try:

            train_country(
                country
            )


        except Exception as e:


            print()

            print(
                "FAILED",
                country
            )


            print(
                repr(e)
            )



    print()

    print("="*70)

    print(
        "IMBALANCE FORECASTING COMPLETED"
    )

    print("="*70)





if __name__ == "__main__":

    main()