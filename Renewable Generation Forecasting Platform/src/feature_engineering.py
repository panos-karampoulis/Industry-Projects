import pandas as pd
import numpy as np

from pathlib import Path


def create_features(df, country=None, save=False):
    """
    Creates time-series features for renewable generation forecasting.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw generation dataframe.

    country : str, optional
        Country name used when saving processed datasets.

    save : bool, default=False
        If True, saves dataset.csv and features.csv automatically.

    Returns
    -------
    pandas.DataFrame
        Feature engineered dataframe.
    """

    # -------------------------
    # Sort
    # -------------------------

    df = (
        df
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    # Keep copy BEFORE lags/dropna
    original_df = df.copy()

    # -------------------------
    # Target
    # -------------------------

    df["renewable_total_mwh"] = (
        df["solar_mwh"]
        +
        df["wind_total_mwh"]
    )

    # -------------------------
    # Calendar Features
    # -------------------------

    df["hour"] = (
        df["datetime"]
        .dt.hour
    )

    df["day_of_week"] = (
        df["datetime"]
        .dt.dayofweek
    )

    df["month"] = (
        df["datetime"]
        .dt.month
    )

    df["day_of_year"] = (
        df["datetime"]
        .dt.dayofyear
    )

    df["year"] = (
        df["datetime"]
        .dt.year
    )

    df["day_of_month"] = (
        df["datetime"]
        .dt.day
    )

    # -------------------------
    # Cyclic Features
    # -------------------------

    df["hour_sin"] = np.sin(
        2 * np.pi * df["hour"] / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * df["hour"] / 24
    )

    df["month_sin"] = np.sin(
        2 * np.pi * df["month"] / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * df["month"] / 12
    )

    # -------------------------
    # Lag Features
    # -------------------------

    lags = [
        1,
        2,
        3,
        24,
        48,
        168
    ]

    for lag in lags:

        df[f"solar_lag_{lag}"] = (
            df["solar_mwh"]
            .shift(lag)
        )

        df[f"wind_lag_{lag}"] = (
            df["wind_total_mwh"]
            .shift(lag)
        )


    


    # -------------------------
    # Rolling Features
    # -------------------------

    windows = [
        3,
        6,
        24,
        168
    ]

    for window in windows:

        df[f"solar_roll_mean_{window}"] = (
            df["solar_mwh"]
            .shift(1)
            .rolling(window)
            .mean()
        )

        df[f"wind_roll_mean_{window}"] = (
            df["wind_total_mwh"]
            .shift(1)
            .rolling(window)
            .mean()
        )

        df[f"solar_roll_std_{window}"] = (
            df["solar_mwh"]
            .shift(1)
            .rolling(window)
            .std()
        )

        df[f"wind_roll_std_{window}"] = (
            df["wind_total_mwh"]
            .shift(1)
            .rolling(window)
            .std()
        )

    # -------------------------
    # Weather Rolling Features
    # -------------------------

   

    # -------------------------
    # Remove NaNs
    # -------------------------

    df = (
        df
        .dropna()
        .reset_index(drop=True)
    )

    # -------------------------
    # Save processed datasets
    # -------------------------

    if save and country is not None:

        base_dir = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        output_dir = (
            base_dir
            / "data"
            / "processed"
            / country
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        original_df.to_csv(
            output_dir / "dataset.csv",
            index=False
        )

        df.to_csv(
            output_dir / "features.csv",
            index=False
        )

        print()
        print("Processed datasets saved:")
        print(output_dir / "dataset.csv")
        print(output_dir / "features.csv")

    return df