import os
import sys
import pandas as pd
import numpy as np



# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


sys.path.append(
    BASE_DIR
)



# ==========================================================
# PATHS
# ==========================================================

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


FEATURE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "features"
)


os.makedirs(
    FEATURE_DIR,
    exist_ok=True
)



# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]



# ==========================================================
# FEATURE CREATION
# ==========================================================

def create_features(country):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    input_file = os.path.join(

        PROCESSED_DIR,

        f"{country}_day_ahead_prices.csv"

    )


    output_file = os.path.join(

        FEATURE_DIR,

        f"{country}_day_ahead_features.csv"

    )



    # ------------------------------------------------------
    # LOAD DATA
    # ------------------------------------------------------

    df = pd.read_csv(

        input_file

    )



    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )



    df = df.sort_values(

        "timestamp"

    )



    df = df.set_index(

        "timestamp"

    )



    # ------------------------------------------------------
    # HOURLY AGGREGATION
    # ------------------------------------------------------

    df = (

        df["price_eur_mwh"]

        .resample("1h")

        .mean()

        .to_frame()

    )



    df.columns = [

        "price_eur_mwh"

    ]



    # ------------------------------------------------------
    # CALENDAR FEATURES
    # ------------------------------------------------------

    df["hour"] = (

        df.index.hour

    )


    df["day_of_week"] = (

        df.index.dayofweek

    )


    df["month"] = (

        df.index.month

    )


    df["day_of_year"] = (

        df.index.dayofyear

    )



    # ------------------------------------------------------
    # LAG FEATURES
    # ------------------------------------------------------

    df["lag_1"] = (

        df["price_eur_mwh"]

        .shift(1)

    )


    df["lag_24"] = (

        df["price_eur_mwh"]

        .shift(24)

    )


    df["lag_48"] = (

        df["price_eur_mwh"]

        .shift(48)

    )


    df["lag_168"] = (

        df["price_eur_mwh"]

        .shift(168)

    )



    # ------------------------------------------------------
    # ROLLING FEATURES
    # ------------------------------------------------------

    df["rolling_mean_24"] = (

        df["price_eur_mwh"]

        .rolling(24)

        .mean()

    )


    df["rolling_std_24"] = (

        df["price_eur_mwh"]

        .rolling(24)

        .std()

    )



    # ------------------------------------------------------
    # TARGET
    # ------------------------------------------------------

    df["target"] = (

        df["price_eur_mwh"]

        .shift(-24)

    )



    # ------------------------------------------------------
    # CLEAN
    # ------------------------------------------------------

    df = df.dropna()



    df = df.reset_index()



    df["country"] = country



    df.to_csv(

        output_file,

        index=False

    )


    print(

        "Saved:",

        output_file

    )


    print(

        "Rows:",

        len(df)

    )





# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:


        create_features(

            country

        )


    print("\n")
    print("="*60)
    print("DAY AHEAD FEATURE ENGINEERING COMPLETED")
    print("="*60)