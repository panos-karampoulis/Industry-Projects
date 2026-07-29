import pandas as pd
from pathlib import Path
import sys


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


RAW_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "generation"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# GENERATION FEATURES
# ============================================================

def process_generation(country):


    print()
    print("=" * 70)
    print(
        f"PROCESSING GENERATION: {country.upper()}"
    )
    print("=" * 70)



    file = (
        RAW_DIR
        /
        country
        /
        "generation.csv"
    )



    df = pd.read_csv(
        file
    )



    # timestamp

    df.rename(
        columns={
            "index": "timestamp"
        },
        inplace=True
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )



    df = df.sort_values(
        "timestamp"
    )



    # ========================================================
    # RENEWABLE GENERATION
    # ========================================================


    renewable_cols = [

        "Solar",

        "Wind Onshore",

        "Hydro Run-of-river and poundage",

        "Hydro Water Reservoir",

        "Biomass",

        "Geothermal"

    ]



    for col in renewable_cols:


        if col not in df.columns:

            df[col] = 0



        df[col] = (
            pd.to_numeric(
                df[col],
                errors="coerce"
            )
            .fillna(0)
        )



    df["renewable_generation_mw"] = (

        df[renewable_cols]

        .sum(axis=1)

    )



    # ========================================================
    # TOTAL GENERATION
    # ========================================================


    generation_cols = [

        c for c in df.columns

        if c not in [

            "timestamp",

            "country"

        ]

    ]



    df["total_generation_mw"] = (

        df[generation_cols]

        .select_dtypes(
            include="number"
        )

        .sum(axis=1)

    )



    df["renewable_share"] = (

        df["renewable_generation_mw"]

        /

        df["total_generation_mw"]

    )



    # ========================================================
    # VOLATILITY FEATURES
    # ========================================================


    df["generation_ramp_mw"] = (

        df["renewable_generation_mw"]

        .diff()

    )


    df["renewable_volatility"] = (

        df["generation_ramp_mw"]

        .rolling(24)

        .std()

    )



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



    output = (

        OUTPUT_DIR

        /

        f"{country}_generation_features.csv"

    )



    df.to_csv(
        output,
        index=False
    )


    print(
        "Saved:",
        output
    )



# ============================================================
# RUN
# ============================================================


if __name__ == "__main__":


    process_generation(
        "italy"
    )