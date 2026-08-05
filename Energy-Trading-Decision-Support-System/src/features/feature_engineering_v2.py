from pathlib import Path
import pandas as pd
import numpy as np


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


INPUT_DIR = (
    BASE_DIR /
    "data" /
    "processed"
)


OUTPUT_DIR = (
    BASE_DIR /
    "data" /
    "features"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]



# ==========================================================
# CYCLICAL TIME FEATURES
# ==========================================================

def add_time_features(df):


    df["hour_sin"] = np.sin(
        2*np.pi*df["hour"]/24
    )

    df["hour_cos"] = np.cos(
        2*np.pi*df["hour"]/24
    )


    df["dow_sin"] = np.sin(
        2*np.pi*df["day_of_week"]/7
    )

    df["dow_cos"] = np.cos(
        2*np.pi*df["day_of_week"]/7
    )


    df["month_sin"] = np.sin(
        2*np.pi*df["month"]/12
    )

    df["month_cos"] = np.cos(
        2*np.pi*df["month"]/12
    )


    return df




# ==========================================================
# PRICE FEATURES
# ==========================================================

def add_price_features(df):


    price = "day_ahead_price"


    # lag features

    lags = [
        1,
        2,
        3,
        6,
        24,
        48,
        168
    ]


    for lag in lags:

        df[f"{price}_lag_{lag}"] = (
            df[price]
            .shift(lag)
        )



    # rolling statistics

    windows = [
        6,
        24,
        48,
        168
    ]


    for window in windows:

        df[
            f"{price}_rolling_mean_{window}"
        ] = (

            df[price]
            .shift(1)
            .rolling(window)
            .mean()

        )


        df[
            f"{price}_rolling_std_{window}"
        ] = (

            df[price]
            .shift(1)
            .rolling(window)
            .std()

        )



    # price spikes

    df["price_spike"] = (

        df[price] >

        df[price]
        .rolling(168)
        .mean()
        +

        2 *

        df[price]
        .rolling(168)
        .std()

    ).astype(int)



    # negative prices

    df["negative_price_flag"] = (

        df[price] < 0

    ).astype(int)


    return df




# ==========================================================
# LOAD FEATURES
# ==========================================================

def add_load_features(df):


    df["load_lag_1"] = (
        df["load_mw"]
        .shift(1)
    )


    df["load_lag_24"] = (
        df["load_mw"]
        .shift(24)
    )


    df["load_lag_168"] = (
        df["load_mw"]
        .shift(168)
    )


    df["load_ramp"] = (
        df["load_mw"]
        .diff()
    )


    df["load_change_pct"] = (

        df["load_mw"]
        .pct_change()

    )


    return df




# ==========================================================
# RENEWABLE FEATURES
# ==========================================================

def add_renewable_features(df):


    cols = [

        "wind_generation",
        "solar_generation",
        "renewable_generation"

    ]


    for col in cols:


        df[f"{col}_lag_1"] = (

            df[col]
            .shift(1)

        )


        df[f"{col}_lag_24"] = (

            df[col]
            .shift(24)

        )


        df[f"{col}_ramp"] = (

            df[col]
            .diff()

        )



    df["renewable_share_change"] = (

        df["renewable_share"]
        .diff()

    )


    return df




# ==========================================================
# RISK FEATURES
# ==========================================================

def add_risk_features(df):


    df["price_volatility_24h"] = (

        df["day_ahead_price"]
        .rolling(24)
        .std()

    )


    df["price_volatility_168h"] = (

        df["day_ahead_price"]
        .rolling(168)
        .std()

    )


    df["residual_load_change"] = (

        df["residual_load"]
        .diff()

    )


    return df




# ==========================================================
# PROCESS COUNTRY
# ==========================================================

def process_country(country):


    print("\n")
    print("="*70)
    print(country.upper())
    print("="*70)



    file = (

        INPUT_DIR /
        f"{country}_clean.csv"

    )


    df = pd.read_csv(
        file,
        parse_dates=[
            "timestamp"
        ]
    )


    df = df.sort_values(
        "timestamp"
    )


    df = df.set_index(
        "timestamp"
    )

    df["hour"] = df.index.hour

    df["day_of_week"] = df.index.dayofweek

    df["month"] = df.index.month

    df["weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    print(
        "Original:",
        df.shape
    )



    df = add_price_features(df)

    df = add_load_features(df)

    df = add_renewable_features(df)

    df = add_risk_features(df)

    df = add_time_features(df)



    # Fill delayed operational data
    df = df.ffill()


    # Remove only rows where price is missing
    df = df.dropna(
        subset=[
            "day_ahead_price"
        ]
    )



    output = (

        OUTPUT_DIR /
        f"{country}_features.csv"

    )


    df.to_csv(
        output
    )


    print(
        "Saved:",
        output
    )


    print(
        "Final shape:",
        df.shape
    )




# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:

        try:

            process_country(
                country
            )


        except Exception as e:

            print(
                country,
                "FAILED"
            )

            print(e)