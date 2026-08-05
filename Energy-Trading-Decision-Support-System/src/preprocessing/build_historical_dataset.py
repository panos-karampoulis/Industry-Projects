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



COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]



# ==========================================================
# GENERATION PROCESSING
# ==========================================================

def process_generation(df):


    # convert all possible numeric columns

    for col in df.columns:

        if col != "timestamp":

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )



    df = df.dropna(
        axis=1,
        how="all"
    )



    # WIND

    wind_cols = [
        c for c in df.columns
        if "Wind" in c
    ]


    if wind_cols:

        df["wind_generation"] = (
            df[wind_cols]
            .sum(axis=1)
        )

    else:

        df["wind_generation"] = 0



    # SOLAR

    solar_cols = [
        c for c in df.columns
        if "Solar" in c
    ]


    if solar_cols:

        df["solar_generation"] = (
            df[solar_cols]
            .sum(axis=1)
        )

    else:

        df["solar_generation"] = 0



    # TOTAL RENEWABLES

    renewable_cols = [
        c for c in df.columns
        if any(
            x in c
            for x in [
                "Wind",
                "Solar",
                "Hydro",
                "Biomass",
                "Geothermal"
            ]
        )
    ]


    df["renewable_generation"] = (
        df[renewable_cols]
        .sum(axis=1)
    )



    return df[
        [
            "timestamp",
            "wind_generation",
            "solar_generation",
            "renewable_generation"
        ]
    ]



# ==========================================================
# TIME FEATURES
# ==========================================================

def add_time_features(df):


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


    df["weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)



    return df



# ==========================================================
# COUNTRY BUILDER
# ==========================================================

def build_country(country):


    print("\n")
    print("="*70)
    print(country.upper())
    print("="*70)



    folder = (
        RAW_DIR
        /
        country
    )



    # ------------------------------------------------------
    # LOAD YEARLY FILES
    # ------------------------------------------------------

    print("Loading load files...")


    load_files = sorted(
        folder.glob(
            "load_*.csv"
        )
    )


    load_list = []


    for file in load_files:


        df = pd.read_csv(
            file
        )


        df.columns = [
            c.lower()
            for c in df.columns
        ]


        timestamp_col = (
            "unnamed: 0"
        )


        df["timestamp"] = pd.to_datetime(
            df[timestamp_col],
            utc=True
        )


        value_col = [
            c for c in df.columns
            if c not in [
                timestamp_col,
                "timestamp"
            ]
        ][0]


        df = df.rename(
            columns={
                value_col:"load_mw"
            }
        )


        load_list.append(
            df[
                [
                    "timestamp",
                    "load_mw"
                ]
            ]
        )



    load = pd.concat(
        load_list,
        ignore_index=True
    )



    # ------------------------------------------------------
    # PRICE
    # ------------------------------------------------------

    print("Loading prices...")


    price_files = sorted(
        folder.glob(
            "day_ahead_*.csv"
        )
    )


    price_list=[]


    for file in price_files:


        df=pd.read_csv(
            file
        )


        df.columns=[
            c.lower()
            for c in df.columns
        ]


        timestamp_col="unnamed: 0"


        df["timestamp"]=pd.to_datetime(
            df[timestamp_col],
            utc=True
        )


        value_col=[
            c for c in df.columns
            if c not in [
                timestamp_col,
                "timestamp"
            ]
        ][0]


        df=df.rename(
            columns={
                value_col:
                "day_ahead_price"
            }
        )


        price_list.append(
            df[
                [
                    "timestamp",
                    "day_ahead_price"
                ]
            ]
        )



    price=pd.concat(
        price_list,
        ignore_index=True
    )



    # ------------------------------------------------------
    # GENERATION
    # ------------------------------------------------------

    print("Loading generation...")


    generation_files=sorted(
        folder.glob(
            "generation_*.csv"
        )
    )


    generation_list=[]


    for file in generation_files:


        df=pd.read_csv(
            file,
            low_memory=False
        )


        df.columns=[
            c
            for c in df.columns
        ]


        df["timestamp"]=pd.to_datetime(
            df["Unnamed: 0"],
            utc=True
        )


        df=df.drop(
            columns=[
                "Unnamed: 0"
            ]
        )



        generation_list.append(
            df
        )



    generation=pd.concat(
        generation_list,
        ignore_index=True
    )


    generation=process_generation(
        generation
    )



    # ------------------------------------------------------
    # MERGE
    # ------------------------------------------------------


    print("Merging...")


    df=(
        load
        .merge(
            price,
            on="timestamp",
            how="outer"
        )
        .merge(
            generation,
            on="timestamp",
            how="outer"
        )
    )



    df=df.sort_values(
        "timestamp"
    )



    # hourly

    df=(
        df
        .set_index(
            "timestamp"
        )
        .resample(
            "1h"
        )
        .mean()
    )



    df=df.interpolate(
        method="time"
    )


    df=df.reset_index()



    # extra features

    df["residual_load"]=(
        df["load_mw"]
        -
        df["renewable_generation"]
    )


    # Renewable share

    df["renewable_share"] = np.where(

        df["load_mw"] > 0,

        df["renewable_generation"]
        /
        df["load_mw"],

        np.nan

    )


    df=add_time_features(
        df
    )



    output=(
        PROCESSED_DIR
        /
        f"{country}_clean.csv"
    )




    # ==========================================================
    # FINAL DATA QUALITY CHECK
    # ==========================================================

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )


    df = df.dropna()

    df.to_csv(
        output,
        index=False
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

if __name__=="__main__":


    for country in COUNTRIES:

        try:

            build_country(
                country
            )


        except Exception as e:

            print(
                country,
                "FAILED:"
            )

            print(e)