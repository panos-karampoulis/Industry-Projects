import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"

PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "generation"
)

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# COUNTRY LIST
# ============================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]


# ============================================================
# FEATURE ENGINEERING
# ============================================================


def create_generation_features(df):


    df = df.copy()


    # timestamp
    df["timestamp"] = pd.to_datetime(
        df["index"],
        utc=True
    )


    df = df.drop(
        columns=["index"],
        errors="ignore"
    )


    df = df.sort_values(
        "timestamp"
    )


    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------

    numeric_cols = df.columns.drop(
        [
            "timestamp",
            "country"
        ],
        errors="ignore"
    )


    df[numeric_cols] = df[numeric_cols].apply(
        pd.to_numeric,
        errors="coerce"
    )


    # --------------------------------------------------------
    # Fill missing generation values
    # --------------------------------------------------------

    df[numeric_cols] = (
        df[numeric_cols]
        .fillna(0)
    )


    # --------------------------------------------------------
    # Generation aggregation
    # --------------------------------------------------------

    renewable_cols = [

        "Solar",
        "Wind Onshore",
        "Hydro Run-of-river and poundage",
        "Hydro Water Reservoir",
        "Biomass",
        "Geothermal"

    ]


    renewable_cols = [

        c for c in renewable_cols
        if c in df.columns

    ]


    df["renewable_generation_mw"] = (
        df[renewable_cols]
        .sum(axis=1)
    )


    total_cols = [

        c for c in df.columns
        if c not in
        [
            "timestamp",
            "country"
        ]

    ]


    df["total_generation_mw"] = (
        df[total_cols]
        .sum(axis=1)
    )


    df["renewable_share"] = (

        df["renewable_generation_mw"]

        /

        df["total_generation_mw"]

    )


    df["renewable_share"] = (
        df["renewable_share"]
        .replace(
            [np.inf, -np.inf],
            np.nan
        )
        .fillna(0)
    )


    # --------------------------------------------------------
    # Time features
    # --------------------------------------------------------

    df["hour"] = (
        df["timestamp"]
        .dt.hour
    )


    df["weekday"] = (
        df["timestamp"]
        .dt.weekday
    )


    df["month"] = (
        df["timestamp"]
        .dt.month
    )


    # --------------------------------------------------------
    # Lag features
    # --------------------------------------------------------

    for lag in [

        1,
        4,
        24,
        96

    ]:

        df[f"renewable_lag_{lag}"] = (

            df["renewable_generation_mw"]
            .shift(lag)

        )


    # --------------------------------------------------------
    # Rolling statistics
    # --------------------------------------------------------

    df["renewable_roll_mean_24"] = (

        df["renewable_generation_mw"]
        .rolling(24)
        .mean()

    )


    df["renewable_roll_std_24"] = (

        df["renewable_generation_mw"]
        .rolling(24)
        .std()

    )


    df["generation_volatility_96"] = (

        df["total_generation_mw"]
        .rolling(96)
        .std()

    )


    # remove initial NaNs
    df = df.dropna()


    return df



# ============================================================
# PROCESS COUNTRY
# ============================================================


def process_country(country):


    print()

    print("=" * 70)

    print(
        f"PROCESSING GENERATION: {country.upper()}"
    )

    print("=" * 70)


    input_file = (

        RAW_DIR
        /
        country
        /
        "generation.csv"

    )


    if not input_file.exists():

        print(
            "Missing:",
            input_file
        )

        return



    df = pd.read_csv(
        input_file
    )


    features = create_generation_features(
        df
    )


    output = (

        PROCESSED_DIR
        /
        f"{country}_generation_features.csv"

    )


    features.to_csv(
        output,
        index=False
    )


    print(
        "Saved:",
        output
    )

    print(
        features.shape
    )



# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    for country in COUNTRIES:

        process_country(
            country
        )


    print()

    print(
        "GENERATION FEATURE ENGINEERING COMPLETED"
    )