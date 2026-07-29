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


from src.config.countries import (
    get_active_countries
)



# ============================================================
# PATHS
# ============================================================


PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


MODEL_DIR = (
    BASE_DIR
    /
    "models"
    /
    "load_forecasting"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "balancing"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# LOAD DATA
# ============================================================


def load_country_data(
        country
):


    path = (
        PROCESSED_DIR
        /
        f"{country}_load_features.csv"
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
# LOAD MODEL
# ============================================================


def load_model(
        country
):


    model_path = (
        MODEL_DIR
        /
        country
        /
        "xgboost.pkl"
    )


    model = joblib.load(
        model_path
    )


    return model





# ============================================================
# CREATE FORECAST ERROR
# ============================================================


def calculate_imbalance(
        country
):


    print()
    print("="*70)

    print(
        f"PROCESSING {country.upper()}"
    )

    print("="*70)



    df = load_country_data(
        country
    )



    model = load_model(
        country
    )



    target = "load_mw"



    drop_columns = [

        "timestamp",
        "country",
        target

    ]



    X = df.drop(

        columns=[
            c for c in drop_columns
            if c in df.columns
        ]

    )



    y = df[target]



    # remove missing

    data = pd.concat(

        [
            X,
            y,
            df["timestamp"]
        ],

        axis=1

    ).dropna()



    X = data.drop(

        columns=[
            target,
            "timestamp"
        ]

    )


    actual = data[target]



    timestamps = data["timestamp"]



    # prediction

    forecast = model.predict(
        X
    )



    result = pd.DataFrame({

        "timestamp": timestamps,

        "country": country,

        "actual_load_mw": actual,

        "forecast_load_mw": forecast

    })



    # imbalance

    result["imbalance_mw"] = (

        result["actual_load_mw"]

        -

        result["forecast_load_mw"]

    )



    result["absolute_error_mw"] = (

        result["imbalance_mw"]
        .abs()

    )



    # time features

    result["hour"] = (

        result["timestamp"]
        .dt.hour

    )


    result["weekday"] = (

        result["timestamp"]
        .dt.weekday

    )


    result["month"] = (

        result["timestamp"]
        .dt.month

    )



    output = (

        OUTPUT_DIR
        /
        f"{country}_imbalance.csv"

    )



    result.to_csv(

        output,

        index=False

    )



    print(
        "Saved:",
        output
    )



    print(
        result.head()
    )



# ============================================================
# MAIN
# ============================================================


def main():


    countries = get_active_countries()



    for country in countries:


        try:

            calculate_imbalance(
                country
            )


        except Exception as e:

            print()

            print(
                "FAILED:",
                country
            )

            print(
                repr(e)
            )



    print()

    print("="*70)

    print(
        "IMBALANCE CALCULATION COMPLETED"
    )

    print("="*70)




if __name__ == "__main__":

    main()