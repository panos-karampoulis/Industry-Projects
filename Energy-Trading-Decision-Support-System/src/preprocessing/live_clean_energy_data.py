from pathlib import Path
import pandas as pd
import numpy as np


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


RAW_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "latest"
)


PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


PROCESSED_DIR.mkdir(
    exist_ok=True,
    parents=True
)



COUNTRIES = [

    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"

]



# ==========================================================
# LOAD CSV CLEAN FUNCTION
# ==========================================================

def load_entsoe_file(path):


    df = pd.read_csv(
        path
    )


    print("\nFILE:")
    print(path.name)

    print(df.dtypes)



    # find timestamp column

    timestamp_col = None


    for col in df.columns:


        if "time" in col.lower() or "date" in col.lower():

            timestamp_col = col
            break



    if timestamp_col is None:

        timestamp_col = df.columns[0]



    df["timestamp"] = pd.to_datetime(
        df[timestamp_col],
        utc=True,
        errors="coerce"
    )


    df = df.dropna(
        subset=[
            "timestamp"
        ]
    )



    df = df.set_index(
        "timestamp"
    )



    # keep numeric columns only

    numeric = (
        df
        .select_dtypes(
            include=np.number
        )
    )



    return numeric




# ==========================================================
# GENERATION PROCESS
# ==========================================================

def process_generation(df):


    wind = [
        c for c in df.columns
        if "wind" in c.lower()
    ]


    solar = [
        c for c in df.columns
        if "solar" in c.lower()
    ]



    if wind:

        df["wind_generation"] = (
            df[wind]
            .sum(axis=1)
        )

    else:

        df["wind_generation"] = 0



    if solar:

        df["solar_generation"] = (
            df[solar]
            .sum(axis=1)
        )

    else:

        df["solar_generation"] = 0




    df["renewable_generation"] = (

        df["wind_generation"]

        +

        df["solar_generation"]

    )



    return df[
        [
            "wind_generation",
            "solar_generation",
            "renewable_generation"
        ]
    ]





# ==========================================================
# COUNTRY PIPELINE
# ==========================================================

def process_country(country):


    print("\n")
    print("="*70)
    print(country.upper())
    print("="*70)



    folder = RAW_DIR



    # -------------------------
    # LOAD
    # -------------------------

    load = load_entsoe_file(

        folder /
        f"{country}_load.csv"

    )


    load_column = load.columns[0]


    load = load.rename(

        columns={
            load_column:
            "load_mw"
        }

    )



    # -------------------------
    # PRICE
    # -------------------------

    price = load_entsoe_file(

        folder /
        f"{country}_prices.csv"

    )


    price_column = price.columns[0]


    price = price.rename(

        columns={
            price_column:
            "day_ahead_price"
        }

    )



    # -------------------------
    # GENERATION
    # -------------------------

    generation_raw = load_entsoe_file(

        folder /
        f"{country}_generation.csv"

    )


    generation = process_generation(
        generation_raw
    )



    # -------------------------
    # MERGE
    # -------------------------

    df = pd.concat(

        [
            load,
            price,
            generation
        ],

        axis=1

    )



    df = (

        df
        .sort_index()
        .resample(
            "1h"
        )
        .mean()

    )



    # interpolate missing

    df = df.interpolate(
        method="time"
    )



    # -------------------------
    # ENERGY FEATURES
    # -------------------------


    df["residual_load"] = (

        df["load_mw"]

        -

        df["renewable_generation"]

    )



    df["renewable_share"] = (

        df["renewable_generation"]

        /

        df["load_mw"]

    )



    # -------------------------
    # TIME FEATURES
    # -------------------------

    df["hour"] = df.index.hour

    df["day_of_week"] = (
        df.index.dayofweek
    )

    df["month"] = (
        df.index.month
    )


    df["weekend"] = (

        df["day_of_week"] >= 5

    ).astype(int)



    # -------------------------
    # SAVE
    # -------------------------

    output = (

        PROCESSED_DIR

        /

        f"{country}_clean.csv"

    )


    df.to_csv(
        output
    )



    print(
        "Saved:",
        output
    )


    print(
        "Shape:",
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
                "FAILED:"
            )


            print(e)