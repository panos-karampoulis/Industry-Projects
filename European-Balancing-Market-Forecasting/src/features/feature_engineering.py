import pandas as pd
import numpy as np

from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


RAW_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
)


PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# FEATURE CREATION
# ============================================================


def create_time_features(df):


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df["hour"] = (
        df["timestamp"]
        .dt.hour
    )


    df["day_of_week"] = (
        df["timestamp"]
        .dt.dayofweek
    )


    df["month"] = (
        df["timestamp"]
        .dt.month
    )


    df["year"] = (
        df["timestamp"]
        .dt.year
    )


    df["weekend"] = (
        df["day_of_week"]
        >= 5
    ).astype(int)


    return df




# ============================================================
# LOAD FEATURES
# ============================================================


def create_load_features(df):


    df = create_time_features(
        df
    )


    df = df.sort_values(
        "timestamp"
    )


    df["load_lag_1"] = (
        df["load_mw"]
        .shift(1)
    )


    df["load_lag_4"] = (
        df["load_mw"]
        .shift(4)
    )


    df["load_lag_96"] = (
        df["load_mw"]
        .shift(96)
    )


    df["load_rolling_mean_24h"] = (
        df["load_mw"]
        .rolling(96)
        .mean()
    )


    df["load_rolling_std_24h"] = (
        df["load_mw"]
        .rolling(96)
        .std()
    )


    return df




# ============================================================
# PRICE FEATURES
# ============================================================


def create_price_features(df):


    df = create_time_features(
        df
    )


    df = df.sort_values(
        "timestamp"
    )


    df["price_lag_1"] = (
        df["price_eur_mwh"]
        .shift(1)
    )


    df["price_lag_24"] = (
        df["price_eur_mwh"]
        .shift(24)
    )


    df["price_lag_168"] = (
        df["price_eur_mwh"]
        .shift(168)
    )


    df["price_rolling_mean_24h"] = (
        df["price_eur_mwh"]
        .rolling(24)
        .mean()
    )


    df["price_volatility_24h"] = (
        df["price_eur_mwh"]
        .rolling(24)
        .std()
    )


    df["negative_price"] = (
        df["price_eur_mwh"]
        < 0
    ).astype(int)



    df["price_spike"] = (
        df["price_eur_mwh"]
        >
        df["price_eur_mwh"]
        .rolling(168)
        .quantile(0.95)
    ).astype(int)


    return df




# ============================================================
# COUNTRY PROCESSING
# ============================================================


def process_country(country):


    print(
        "\nProcessing:",
        country.upper()
    )


    country_dir = (
        RAW_DIR
        /
        country
    )


    load_file = (
        country_dir
        /
        "load.csv"
    )


    price_file = (
        country_dir
        /
        "day_ahead_prices.csv"
    )



    load = pd.read_csv(
        load_file
    )


    prices = pd.read_csv(
        price_file
    )



    load_features = create_load_features(
        load
    )


    price_features = create_price_features(
        prices
    )



    load_features.to_csv(
        PROCESSED_DIR
        /
        f"{country}_load_features.csv",
        index=False
    )


    price_features.to_csv(
        PROCESSED_DIR
        /
        f"{country}_price_features.csv",
        index=False
    )


    print(
        "Saved processed features"
    )





# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    countries = [

        "germany",
        "france",
        "italy",
        "netherlands",
        "spain"

    ]


    for country in countries:

        process_country(
            country
        )


    print("\nFEATURE ENGINEERING COMPLETED")