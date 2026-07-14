import pandas as pd
import numpy as np


def create_features(df):
    """
    Create time-series features for load forecasting.
    """

    df = df.copy()

    # Time features
    df["hour"] = df["datetime"].dt.hour
    df["month"] = df["datetime"].dt.month
    df["weekday"] = df["datetime"].dt.weekday

    df["weekend"] = (
        df["weekday"]
        >= 5
    ).astype(int)


    # Lag features
    df["load_lag_1"] = (
        df["load"]
        .shift(1)
    )

    df["load_lag_24"] = (
        df["load"]
        .shift(24)
    )

    df["load_lag_168"] = (
        df["load"]
        .shift(168)
    )


    # Rolling features

    df["rolling_mean_24"] = (
        df["load"]
        .shift(1)
        .rolling(24)
        .mean()
    )

    df["rolling_std_24"] = (
        df["load"]
        .shift(1)
        .rolling(24)
        .std()
    )


    # Cyclical encoding

    df["hour_sin"] = np.sin(
        2 * np.pi * df["hour"] / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * df["hour"] / 24
    )


    # Remove rows with missing lags

    df = df.dropna()


    return df