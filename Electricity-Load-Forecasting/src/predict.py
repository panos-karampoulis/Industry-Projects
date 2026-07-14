from pathlib import Path
import json
import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent



def load_model(country="Germany"):
    """
    Load trained model for selected country.
    """

    model_path = (
        BASE_DIR
        / "models"
        / country
        / "xgboost_load_forecasting.pkl"
    )


    model = joblib.load(
        model_path
    )

    return model



def load_features(country="Germany"):
    """
    Load feature list used during training.
    """

    features_path = (
        BASE_DIR
        / "models"
        / country
        / "features.json"
    )


    with open(
        features_path,
        "r"
    ) as f:

        features = json.load(f)


    return features



def predict_load(
    model,
    df,
    country="Germany"
):
    """
    Generate load forecast.
    """


    features = load_features(
        country
    )


    X = df[features]


    predictions = model.predict(
        X
    )


    forecast = pd.DataFrame(
        {
            "datetime": df["datetime"],
            "forecast": predictions
        }
    )


    return forecast


import numpy as np


def create_future_features(df):

    data = df.copy()

    future = []

    last_loads = data["load"].tolist()

    last_time = data["datetime"].iloc[-1]


    for i in range(1, 25):

        future_time = (
            last_time
            + pd.Timedelta(hours=i)
        )


        row = {}

        row["datetime"] = future_time


        row["temperature"] = data["temperature"].iloc[-1]
        row["wind_speed"] = data["wind_speed"].iloc[-1]
        row["cloud_cover"] = data["cloud_cover"].iloc[-1]
        row["solar_radiation"] = data["solar_radiation"].iloc[-1]


        row["hour"] = future_time.hour
        row["month"] = future_time.month
        row["weekday"] = future_time.weekday()
        row["weekend"] = int(
            future_time.weekday() >= 5
        )


        row["load_lag_1"] = last_loads[-1]
        row["load_lag_24"] = last_loads[-24]
        row["load_lag_168"] = last_loads[-168]


        row["rolling_mean_24"] = np.mean(
            last_loads[-24:]
        )

        row["rolling_std_24"] = np.std(
            last_loads[-24:]
        )


        row["hour_sin"] = np.sin(
            2*np.pi*row["hour"]/24
        )

        row["hour_cos"] = np.cos(
            2*np.pi*row["hour"]/24
        )


        future.append(row)


        last_loads.append(
            last_loads[-1]
        )


    return pd.DataFrame(future)


def recursive_forecast(
    model,
    df,
    features,
    country=None
):

    data = df.copy()

    future = []

    history_loads = data["load"].tolist()

    last_time = data["datetime"].iloc[-1]


    for i in range(1,25):

        future_time = (
            last_time
            + pd.Timedelta(hours=i)
        )


        row = {}

        row["datetime"] = future_time


        # weather
        row["temperature"] = data["temperature"].iloc[-1]
        row["wind_speed"] = data["wind_speed"].iloc[-1]
        row["cloud_cover"] = data["cloud_cover"].iloc[-1]
        row["solar_radiation"] = data["solar_radiation"].iloc[-1]


        # time features

        row["hour"] = future_time.hour
        row["month"] = future_time.month
        row["weekday"] = future_time.weekday()
        row["weekend"] = int(
            future_time.weekday() >= 5
        )


        # lag features

        row["load_lag_1"] = history_loads[-1]

        row["load_lag_24"] = history_loads[-24]

        row["load_lag_168"] = history_loads[-168]


        row["rolling_mean_24"] = np.mean(
            history_loads[-24:]
        )

        row["rolling_std_24"] = np.std(
            history_loads[-24:]
        )


        row["hour_sin"] = np.sin(
            2*np.pi*row["hour"]/24
        )

        row["hour_cos"] = np.cos(
            2*np.pi*row["hour"]/24
        )


        X = pd.DataFrame(
            [row]
        )


        prediction = model.predict(
            X[features]
        )[0]


        future.append(
            {
                "datetime": future_time,
                "forecast": prediction
            }
        )


        # σημαντικό:
        # προσθέτουμε την πρόβλεψη στο ιστορικό

        history_loads.append(
            prediction
        )


    return pd.DataFrame(future)