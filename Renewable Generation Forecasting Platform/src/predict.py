import pandas as pd
import joblib
import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def predict_generation(country, forecast_date=None):

    if forecast_date is None:
        forecast_date = (
            pd.Timestamp.now()
            .date()
        )

    # -----------------------
    # Load config
    # -----------------------

    config_file = (
        BASE_DIR
        /
        "configs"
        /
        f"{country}.yaml"
    )


    with open(config_file, "r") as f:
        config = yaml.safe_load(f)



    # -----------------------
    # Load model
    # -----------------------

    model_file = (
        BASE_DIR
        /
        "models"
        /
        country
        /
        "xgboost_renewable_forecaster.pkl"
    )


    model = joblib.load(
        model_file
    )



    # -----------------------
    # Load latest features
    # -----------------------

    features_file = (
        BASE_DIR
        /
        "data"
        /
        "processed"
        /
        country
        /
        "features.csv"
    )


    df = pd.read_csv(
        features_file,
        parse_dates=["datetime"]
    )



    # τελευταίες 24 ώρες
    future = df[
    df["datetime"].dt.date ==
    pd.to_datetime(forecast_date).date()
    ].copy()



    drop_cols = [

        "datetime",
        "country",

        "renewable_total_mwh",

        "solar_mwh",
        "wind_onshore_mwh",
        "wind_offshore_mwh",
        "wind_total_mwh"

    ]


    X = future.drop(
        columns=drop_cols,
        errors="ignore"
    )


    prediction = model.predict(
        X
    )


    result = future[
    [
        "datetime",
        "solar_mwh",
        "wind_total_mwh",
        "renewable_total_mwh"
    ]
].copy()


    result["prediction_mwh"] = prediction


    result["error_mwh"] = (
        result["renewable_total_mwh"]
        -
        result["prediction_mwh"]
    )


    result["absolute_error"] = (
        result["error_mwh"]
        .abs()
    )


    return result