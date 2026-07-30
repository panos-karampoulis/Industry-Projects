from pathlib import Path
import pandas as pd
import numpy as np


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "data" / "features"

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
# CYCLICAL FEATURES
# ==========================================================

def add_cyclical_features(df):

    # Hour cycle (24h)

    df["hour_sin"] = np.sin(
        2 * np.pi * df["hour"] / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * df["hour"] / 24
    )


    # Day of week cycle

    df["dow_sin"] = np.sin(
        2 * np.pi * df["day_of_week"] / 7
    )

    df["dow_cos"] = np.cos(
        2 * np.pi * df["day_of_week"] / 7
    )


    # Month cycle

    df["month_sin"] = np.sin(
        2 * np.pi * df["month"] / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * df["month"] / 12
    )


    return df



# ==========================================================
# PRICE FEATURES
# ==========================================================

def add_price_features(df):


    price = "day_ahead_price"


    # Lags

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


    # Rolling mean

    windows = [
        6,
        24,
        48,
        168
    ]


    for window in windows:

        df[f"{price}_rolling_mean_{window}"] = (
            df[price]
            .rolling(window)
            .mean()
        )


        df[f"{price}_rolling_std_{window}"] = (
            df[price]
            .rolling(window)
            .std()
        )


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


    df["load_change"] = (
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


    for col in [
        "wind_generation",
        "solar_generation",
        "renewable_generation"
    ]:

        df[f"{col}_lag_1"] = (
            df[col]
            .shift(1)
        )


        df[f"{col}_lag_24"] = (
            df[col]
            .shift(24)
        )


        df[f"{col}_change"] = (
            df[col]
            .diff()
        )


    return df



# ==========================================================
# VOLATILITY FEATURES
# ==========================================================

def add_volatility_features(df):


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


    return df



# ==========================================================
# MAIN PROCESS
# ==========================================================

def process_country(country):


    print("\n" + "="*70)
    print(country.upper())
    print("="*70)


    file = (
        INPUT_DIR /
        f"{country}_clean.csv"
    )


    df = pd.read_csv(
        file,
        index_col=0,
        parse_dates=True
    )


    # Feature creation

    df = add_price_features(df)

    df = add_load_features(df)

    df = add_renewable_features(df)

    df = add_volatility_features(df)

    df = add_cyclical_features(df)



    # Remove rows created by lags

    df = df.dropna()


    output = (
        OUTPUT_DIR /
        f"{country}_features.csv"
    )


    df.to_csv(output)


    print(
        "Saved:",
        output
    )

    print(
        "Shape:",
        df.shape
    )



# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:

        try:

            process_country(country)

        except Exception as e:

            print(
                country,
                "FAILED"
            )

            print(e)