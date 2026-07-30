import os
import pandas as pd
import numpy as np
import joblib


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = r"D:\Portfolio\Intraday Market Forecasting"


COUNTRIES = [
    "france",
    "germany",
    "italy",
    "netherlands",
    "spain"
]


MODEL_NAME = "Linear_Regression.joblib"



MODEL_FEATURES = [

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



# ==========================================================
# TIMESTAMP HANDLER
# ==========================================================


def create_timestamp(df):


    timestamp_columns = [

        "timestamp",
        "datetime",
        "local_timestamp",
        "time",
        "Unnamed: 0"

    ]


    for col in timestamp_columns:


        if col in df.columns:


            df["timestamp"] = pd.to_datetime(
                df[col],
                errors="coerce"
            )


            return df



    raise Exception(
        f"No timestamp column. Columns: {df.columns.tolist()}"
    )




# ==========================================================
# LOAD DATA
# ==========================================================


def load_country(country):


    print("Loading datasets")


    feature_path = os.path.join(

        BASE_DIR,
        "data",
        "features",
        f"{country}_features.csv"

    )


    clean_path = os.path.join(

        BASE_DIR,
        "data",
        "processed",
        f"{country}_clean.csv"

    )


    weather_path = os.path.join(

        BASE_DIR,
        "data",
        "raw",
        "weather",
        f"{country}_weather.csv"

    )



    features = pd.read_csv(
        feature_path
    )


    clean = pd.read_csv(
        clean_path
    )


    weather = pd.read_csv(
        weather_path
    )



    print("Features:", features.shape)
    print("Clean:", clean.shape)
    print("Weather:", weather.shape)



    features = create_timestamp(features)

    clean = create_timestamp(clean)

    weather = create_timestamp(weather)



    # remove duplicates

    features = features.drop_duplicates(
        "timestamp"
    )


    clean = clean.drop_duplicates(
        "timestamp"
    )


    weather = weather.drop_duplicates(
        "timestamp"
    )



    # keep only required clean columns


    clean = clean[
        [
            "timestamp",
            "day_ahead_price"
        ]
    ]



    # remove old price if exists


    if "day_ahead_price" in features.columns:

        features = features.drop(
            columns=["day_ahead_price"]
        )



    # merge price


    df = features.merge(

        clean,

        on="timestamp",

        how="left"

    )



    # merge weather


    df = df.merge(

        weather,

        on="timestamp",

        how="left"

    )



    df=df.sort_values(
        "timestamp"
    )



    print(
        "Final dataset:",
        df.shape
    )



    return df





# ==========================================================
# FEATURE ENGINEERING
# ==========================================================


def build_features(df):


    df=df.copy()


    price="day_ahead_price"



    # TIME FEATURES


    df["hour"] = (
        df.timestamp.dt.hour
    )


    df["day_of_week"] = (
        df.timestamp.dt.dayofweek
    )


    df["month"] = (
        df.timestamp.dt.month
    )


    df["weekend"] = (
        df.day_of_week >= 5
    ).astype(int)



    # DST

    df["dst_flag"]=0



    # PEAK FEATURES


    df["is_peak"] = (

        (df.hour>=8)
        &
        (df.hour<=20)

    ).astype(int)



    df["is_off_peak"] = (
        1-df.is_peak
    )



    df["night_period"] = (

        df.hour < 6

    ).astype(int)



    df["morning_ramp"] = (

        (df.hour>=6)
        &
        (df.hour<=9)

    ).astype(int)



    df["evening_peak"] = (

        (df.hour>=17)
        &
        (df.hour<=21)

    ).astype(int)



    # LAGS


    df["lag_1"] = (
        df[price].shift(1)
    )


    df["lag_4"] = (
        df[price].shift(4)
    )


    df["lag_96"] = (
        df[price].shift(96)
    )


    df["lag_672"] = (
        df[price].shift(672)
    )



    # ROLLING


    df["rolling_mean_96"] = (

        df[price]
        .rolling(96)
        .mean()

    )


    df["rolling_std_96"] = (

        df[price]
        .rolling(96)
        .std()

    )


    df["rolling_mean_672"] = (

        df[price]
        .rolling(672)
        .mean()

    )



    df=df.dropna()



    return df





# ==========================================================
# FORECAST
# ==========================================================


def forecast(country):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    try:


        df = load_country(
            country
        )



        df = build_features(
            df
        )



        print(
            "Rows:",
            len(df)
        )



        model_path = os.path.join(

            BASE_DIR,

            "models",

            country,

            MODEL_NAME

        )



        model = joblib.load(
            model_path
        )



        print(
            "Loaded model:",
            model_path
        )



        missing = [

            c for c in MODEL_FEATURES

            if c not in df.columns

        ]



        if missing:

            raise Exception(
                f"Missing features: {missing}"
            )



        X=df[
            MODEL_FEATURES
        ]



        prediction = model.predict(
            X
        )



        results=pd.DataFrame({

            "timestamp":
                df.timestamp,

            "actual_price":
                df.day_ahead_price,

            "predicted_price":
                prediction

        })



        output_dir=os.path.join(

            BASE_DIR,

            "data",

            "results",

            "next_day_forecasts"

        )


        os.makedirs(

            output_dir,

            exist_ok=True

        )



        output=os.path.join(

            output_dir,

            f"{country}_next_day_forecast.csv"

        )



        results.to_csv(

            output,

            index=False

        )



        print(
            "Saved:",
            output
        )



    except Exception as e:


        print(
            "ERROR:",
            country,
            e
        )





# ==========================================================
# MAIN
# ==========================================================


if __name__=="__main__":


    for country in COUNTRIES:


        forecast(
            country
        )



    print("\n")
    print("="*60)
    print("NEXT DAY FORECAST COMPLETED")
    print("="*60)