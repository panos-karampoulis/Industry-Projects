# ============================================================
# GENERIC FEATURE ENGINEERING
# Day Ahead Price Forecasting
# Multi Country
# ============================================================

import pandas as pd
import numpy as np
import os
import argparse



# ============================================================
# PATHS
# ============================================================

def get_paths(country):

    input_file = (
        f"data/processed/{country}/{country}_clean.csv"
    )

    output_file = (
        f"data/features/{country}_features.csv"
    )


    os.makedirs(
        "data/features",
        exist_ok=True
    )


    return input_file, output_file




# ============================================================
# LOAD DATA
# ============================================================

def load_dataset(country):


    input_file, _ = get_paths(country)


    print("="*70)
    print("CREATING FEATURES")
    print("="*70)


    print(
        "Loading:",
        input_file
    )


    df = pd.read_csv(
        input_file,
        index_col=0,
        parse_dates=True
    )


    df = df.sort_index()


    return df





# ============================================================
# TIME FEATURES
# ============================================================

def create_time_features(df):


    print(
        "Creating time features..."
    )


    df["hour"] = (
        df.index.hour
    )


    df["day_of_week"] = (
        df.index.dayofweek
    )


    df["month"] = (
        df.index.month
    )


    df["weekend"] = (
        df.index.dayofweek >= 5
    ).astype(int)


    return df





# ============================================================
# PRICE LAGS
# ============================================================

def create_price_lags(df):


    print(
        "Creating price lags..."
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


    return df





# ============================================================
# ROLLING FEATURES
# ============================================================

def create_rolling_features(df):


    print(
        "Creating rolling statistics..."
    )


    df["price_mean_24h"] = (
        df["price_eur_mwh"]
        .rolling(24)
        .mean()
    )


    df["price_std_24h"] = (
        df["price_eur_mwh"]
        .rolling(24)
        .std()
    )


    df["price_mean_168h"] = (
        df["price_eur_mwh"]
        .rolling(168)
        .mean()
    )


    return df





# ============================================================
# ENERGY FEATURES
# ============================================================

def create_energy_features(df):


    print(
        "Creating energy features..."
    )


    renewable_cols = []


    for col in df.columns:


        if any(
            x in col.lower()
            for x in [
                "solar",
                "wind",
                "hydro",
                "biomass",
                "renewable"
            ]
        ):

            renewable_cols.append(
                col
            )



    if len(renewable_cols) > 0:


        df["renewable_generation"] = (
            df[renewable_cols]
            .sum(axis=1)
        )


        df["renewable_share"] = (

            df["renewable_generation"]

            /

            df["load_mw"]

        ).replace(
            [np.inf, -np.inf],
            0
        )


    else:


        df["renewable_generation"] = 0

        df["renewable_share"] = 0



    # residual load

    if "load_mw" in df.columns:


        df["residual_load"] = (

            df["load_mw"]

            -

            df["renewable_generation"]

        )


    return df





# ============================================================
# CLEAN FINAL DATASET
# ============================================================

def clean_features(df):


    print(
        "Cleaning missing values..."
    )


    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )


    df = df.dropna()


    return df





# ============================================================
# PIPELINE
# ============================================================

def create_features(country):


    df = load_dataset(
        country
    )


    print()

    print(
        "Original dataset:"
    )

    print(
        df.shape
    )



    df = create_time_features(
        df
    )


    df = create_price_lags(
        df
    )


    df = create_rolling_features(
        df
    )


    df = create_energy_features(
        df
    )



    df = clean_features(
        df
    )



    print()

    print(
        "FINAL FEATURES DATASET"
    )


    print(
        df.head()
    )


    print()

    print(
        "Shape:"
    )

    print(
        df.shape
    )


    print()

    print(
        "Date range:"
    )

    print(
        df.index.min(),
        df.index.max()
    )


    print()

    print(
        "Missing values:"
    )

    print(
        df.isna().sum().sum()
    )



    _, output_file = get_paths(
        country
    )


    df.to_csv(
        output_file
    )


    print()

    print(
        "Saved:"
    )

    print(
        output_file
    )


    print()

    print(
        "DONE"
    )





# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--country",
        required=True
    )


    args = parser.parse_args()



    create_features(
        args.country.lower()
    )