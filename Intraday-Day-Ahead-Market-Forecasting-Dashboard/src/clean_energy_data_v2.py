from pathlib import Path
import pandas as pd
import numpy as np


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MERGED_DIR = BASE_DIR / "data" / "merged"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]


# ==========================================================
# TIME FEATURES
# ==========================================================

def create_time_features(df):

    df["hour"] = df.index.hour

    df["day_of_week"] = df.index.dayofweek

    df["month"] = df.index.month

    df["quarter"] = df.index.quarter


    df["weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)


    # Season

    df["season"] = np.select(
        [
            df["month"].isin([12,1,2]),
            df["month"].isin([3,4,5]),
            df["month"].isin([6,7,8]),
            df["month"].isin([9,10,11])
        ],
        [
            "winter",
            "spring",
            "summer",
            "autumn"
        ],
        default="unknown"
    )


    return df



# ==========================================================
# PEAK / OFF PEAK
# ==========================================================

def create_peak_features(df):

    df["peak_period"] = (
        (df["hour"] >= 8)
        &
        (df["hour"] < 20)
    ).astype(int)


    df["off_peak_period"] = (
        df["peak_period"] == 0
    ).astype(int)


    return df



# ==========================================================
# GENERATION CLEANING
# ==========================================================

def process_generation(gen):


    # convert columns numeric

    gen = gen.apply(
        pd.to_numeric,
        errors="coerce"
    )


    # remove empty columns

    gen = gen.dropna(
        axis=1,
        how="all"
    )


    # WIND

    wind_columns = [
        c for c in gen.columns
        if "Wind" in c
    ]

    if wind_columns:

        gen["wind_generation"] = (
            gen[wind_columns]
            .sum(axis=1)
        )

    else:

        gen["wind_generation"] = 0



    # SOLAR

    solar_columns = [
        c for c in gen.columns
        if "Solar" in c
    ]


    if solar_columns:

        gen["solar_generation"] = (
            gen[solar_columns]
            .sum(axis=1)
        )

    else:

        gen["solar_generation"] = 0



    renewable_columns = [
        c for c in gen.columns
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


    gen["renewable_generation"] = (
        gen[renewable_columns]
        .sum(axis=1)
    )


    return gen[
        [
            "wind_generation",
            "solar_generation",
            "renewable_generation"
        ]
    ]



# ==========================================================
# COUNTRY PROCESSING
# ==========================================================

def process_country(country):


    print("\n" + "="*60)
    print(country.upper())
    print("="*60)


    folder = MERGED_DIR / country


    # ----------------------------
    # Load files
    # ----------------------------

    load = pd.read_csv(
        folder / "load.csv",
        index_col=0
    )


    price = pd.read_csv(
        folder / "day_ahead.csv",
        index_col=0
    )


    generation = pd.read_csv(
        folder / "generation.csv",
        index_col=0,
        low_memory=False
    )


    # ----------------------------
    # Timestamp handling
    # ----------------------------

    for df in [
        load,
        price,
        generation
    ]:

        df.index = pd.to_datetime(
            df.index,
            utc=True
        )


    # ----------------------------
    # Generation processing
    # ----------------------------

    generation = process_generation(
        generation
    )


    # ----------------------------
    # Rename columns dynamically
    # ----------------------------

    # LOAD

    load_column = load.columns[0]

    load = load.rename(
        columns={
            load_column: "load_mw"
        }
    )


    # DAY AHEAD PRICE

    price_column = price.columns[0]

    price = price.rename(
        columns={
            price_column: "day_ahead_price"
        }
    )


    # ----------------------------
    # Merge
    # ----------------------------

    df = pd.concat(
        [
            load,
            price,
            generation
        ],
        axis=1,
        sort=False
    )

    # ----------------------------
    # Hourly frequency
    # ----------------------------

    df = (
        df
        .sort_index()
        .resample("1h")
        .mean()
    )


    # ----------------------------
    # Missing values
    # ----------------------------

    df = df.interpolate(
        method="time"
    )



    # ----------------------------
    # Energy features
    # ----------------------------

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


    # ----------------------------
    # Calendar
    # ----------------------------

    df = create_time_features(df)

    df = create_peak_features(df)


    # ----------------------------
    # Save
    # ----------------------------

    output = (
        PROCESSED_DIR
        /
        f"{country}_clean.csv"
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
                f"{country} FAILED:"
            )

            print(e)