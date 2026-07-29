import pandas as pd
import numpy as np
import joblib
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

ROOT = Path(
    r"D:\Portfolio\European-Balancing-Market-Forecasting"
)


DATA_DIR = ROOT / "data" / "processed" / "risk_dataset"

MODEL_DIR = ROOT / "models" / "imbalance_forecasting"

OUTPUT_DIR = (
    ROOT
    /
    "data"
    /
    "analytics"
    /
    "forecasting"
    /
    "ml"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


# ============================================================
# MODEL FEATURES
# ============================================================

FEATURES = [

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


# ============================================================
# FEATURE CREATION
# ============================================================

def create_forecast_features(df):

    df = df.copy()


    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )


    df = df.sort_values(
        "timestamp"
    )


    # calendar

    df["hour"] = (
        df["timestamp"]
        .dt.hour
    )


    df["weekday"] = (
        df["timestamp"]
        .dt.weekday
    )


    df["month"] = (
        df["timestamp"]
        .dt.month
    )


    # imbalance history

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


    return df



# ============================================================
# CONFIDENCE INTERVAL
# ============================================================

def calculate_confidence_interval(
    df,
    predictions
):

    errors = (

        df["imbalance_mw"]

        -
        df["imbalance_mw"].shift(1)

    )


    error_std = (
        errors
        .std()
    )


    lower = (
        predictions
        -
        1.96 * error_std
    )


    upper = (
        predictions
        +
        1.96 * error_std
    )


    return lower, upper



# ============================================================
# RISK LEVEL
# ============================================================

def risk_classifier(
    prediction,
    lower,
    upper
):

    uncertainty = upper - lower


    if (
        abs(prediction) > 1000
        or uncertainty > 2000
    ):
        return "HIGH"


    elif (
        abs(prediction) > 500
        or uncertainty > 1000
    ):
        return "MEDIUM"


    else:

        return "LOW"



# ============================================================
# FORECAST COUNTRY
# ============================================================


def forecast_country(country):


    print()
    print("="*60)
    print(
        f"FORECASTING {country.upper()}"
    )
    print("="*60)


    # load data

    file = (

        DATA_DIR

        /
        f"{country}_risk_features.csv"

    )


    df = pd.read_csv(
        file
    )


    df = create_forecast_features(
        df
    )


    df = df.dropna()


    # load model

    model_file = (

        MODEL_DIR

        /
        country

        /
        "xgboost.pkl"

    )


    model = joblib.load(
        model_file
    )


    # last known point

    future = df.iloc[-1:].copy()


    predictions = []


    timestamps = []


    current_time = (

        future["timestamp"]

        .iloc[0]

    )


    # recursive forecasting

    temp = future.copy()


    for i in range(96):


        current_time = (

            current_time

            +

            pd.Timedelta(
                minutes=15
            )

        )


        temp["timestamp"] = current_time


        temp["hour"] = current_time.hour

        temp["weekday"] = current_time.weekday()

        temp["month"] = current_time.month



        X = temp[
            FEATURES
        ]


        pred = model.predict(
            X
        )[0]


        predictions.append(
            pred
        )


        timestamps.append(
            current_time
        )


        # update lags

        temp["imbalance_lag_96"] = (
            temp["imbalance_lag_96"]
        )


        temp["imbalance_lag_4"] = (
            pred
        )


        temp["imbalance_lag_1"] = (
            pred
        )


        temp["imbalance_mean_24"] = (
            pred
        )


        temp["imbalance_std_24"] = (
            df["imbalance_mw"]
            .std()
        )



    predictions = np.array(
        predictions
    )


    lower, upper = calculate_confidence_interval(
        df,
        predictions
    )


    result = pd.DataFrame({

        "timestamp": timestamps,

        "forecast_imbalance": predictions,

        "lower_bound": lower,

        "upper_bound": upper

    })


    result["risk_level"] = result.apply(

        lambda x:

        risk_classifier(

            x["forecast_imbalance"],

            x["lower_bound"],

            x["upper_bound"]

        ),

        axis=1

    )


    result["model_used"] = (
        "XGBoost"
    )


    output = (

        OUTPUT_DIR

        /
        f"{country}_ml_forecast.csv"

    )


    result.to_csv(
        output,
        index=False
    )


    print(
        "Saved:",
        output
    )



# ============================================================
# RUN ALL
# ============================================================

if __name__ == "__main__":


    for country in COUNTRIES:

        forecast_country(
            country
        )


    print()

    print(
        "ML NEXT DAY FORECAST COMPLETED"
    )