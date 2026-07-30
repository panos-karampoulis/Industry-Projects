# ============================================================
# INTRADAY FORECAST GENERATOR
# Energy Market Forecasting Engine
# XGBoost Intraday Price Forecast
# ============================================================


import os
import joblib
import pandas as pd
import numpy as np



# ============================================================
# PATHS
# ============================================================


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "europe_intraday_weather_features.csv"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "forecasts",
    "intraday"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)



# ============================================================
# CONFIG
# ============================================================


COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]


# 96 x 15 minutes = next 24 hours

FORECAST_STEPS = 96



# ============================================================
# MODEL FEATURES
# ============================================================


FEATURES = [

    "hour",
    "day_of_week",
    "month",
    "weekend",
    "dst_flag",
    "is_peak",
    "is_off_peak",
    "night_period",
    "morning_ramp",
    "evening_peak",
    "lag_1",
    "lag_4",
    "lag_96",
    "lag_672",
    "rolling_mean_96",
    "rolling_std_96",
    "rolling_mean_672",
    "temperature_2m",
    "wind_speed_10m",
    "shortwave_radiation",
    "cloud_cover",
    "precipitation"

]



# ============================================================
# LOAD DATA
# ============================================================


def load_data():


    df = pd.read_csv(
        DATA_FILE
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.sort_values(
        [
            "country",
            "timestamp"
        ]
    )


    return df




# ============================================================
# LOAD MODEL
# ============================================================


def load_model(country):


    path = os.path.join(

        MODEL_DIR,

        country,

        "XGBoost.joblib"

    )


    if not os.path.exists(path):

        raise FileNotFoundError(
            path
        )


    return joblib.load(
        path
    )




# ============================================================
# FEATURE PREPARATION
# ============================================================


def prepare_features(row):


    features = row.copy()



    remove_cols = [

        "price_eur_mwh",
        "timestamp",
        "country",
        "resolution",
        "local_timestamp"

    ]



    features = features.drop(

        labels=[

            c for c in remove_cols

            if c in features.index

        ]

    )



    # Ensure DST exists

    if "dst_flag" not in features.index:


        timestamp = pd.to_datetime(
            row["timestamp"]
        )


        features["dst_flag"] = int(

            timestamp.dst() is not None

            and

            timestamp.dst().total_seconds() != 0

        )



    # Numeric conversion

    features = pd.to_numeric(

        features,

        errors="coerce"

    )


    features = features.fillna(0)



    # Force exact model features

    for col in FEATURES:


        if col not in features.index:

            features[col] = 0



    features = features[FEATURES]



    return features




# ============================================================
# CREATE FUTURE ROW
# ============================================================


def create_future_row(history):


    last = history.iloc[-1].copy()



    next_time = (

        pd.to_datetime(
            last["timestamp"]
        )

        +

        pd.Timedelta(
            minutes=15
        )

    )



    last["timestamp"] = next_time



    # Calendar features

    last["hour"] = next_time.hour


    last["day_of_week"] = (
        next_time.dayofweek
    )


    last["month"] = (
        next_time.month
    )


    last["weekend"] = int(

        next_time.dayofweek >= 5

    )



    # DST feature

    last["dst_flag"] = int(

        next_time.dst() is not None

        and

        next_time.dst().total_seconds() != 0

    )



    return last




# ============================================================
# FORECAST COUNTRY
# ============================================================


def forecast_country(
        df,
        country
):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    model = load_model(
        country
    )



    data = df[

        df["country"] == country

    ].copy()



    data = data.sort_values(
        "timestamp"
    )



    print(

        "Last actual:",

        data["timestamp"].iloc[-1]

    )



    forecasts = []


    history = data.copy()



    for step in range(
        FORECAST_STEPS
    ):


        future_row = create_future_row(
            history
        )



        X = prepare_features(
            future_row
        )



        prediction = model.predict(

            X.values.reshape(
                1,
                -1
            )

        )[0]



        future_row["price_eur_mwh"] = prediction



        forecasts.append(

            {

                "timestamp":
                    future_row["timestamp"],

                "country":
                    country,

                "forecast_price":
                    prediction,

                "step":
                    step + 1

            }

        )



        history = pd.concat(

            [

                history,

                pd.DataFrame(
                    [future_row]
                )

            ],

            ignore_index=True

        )




    result = pd.DataFrame(
        forecasts
    )



    output_file = os.path.join(

        OUTPUT_DIR,

        f"{country}_intraday_forecast.csv"

    )



    result.to_csv(

        output_file,

        index=False

    )



    print(

        "Forecast rows:",

        len(result)

    )


    print(

        "Saved:",

        output_file

    )





# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    df = load_data()



    for country in COUNTRIES:


        try:


            forecast_country(

                df,

                country

            )


        except Exception as e:


            print(

                "ERROR:",

                country,

                e

            )



    print("\n")
    print(
        "INTRADAY FORECAST COMPLETED"
    )