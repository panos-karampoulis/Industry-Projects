from pathlib import Path
import pandas as pd
import numpy as np

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_market_dataset"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "risk_dataset"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


# ==========================================================
# CREATE RISK FEATURES
# ==========================================================

def create_risk_features(df):

    # ------------------------
    # Price cleaning
    # ------------------------

    if "price_eur_mwh" in df.columns:

        df["price_eur_mwh"] = (
            df["price_eur_mwh"]
            .ffill()
            .bfill()
        )

    # ------------------------
    # Absolute imbalance
    # ------------------------

    df["imbalance_abs_mw"] = (
        df["imbalance_mw"]
        .abs()
    )

    # ------------------------
    # Direction
    # ------------------------

    df["imbalance_direction"] = np.where(
        df["imbalance_mw"] >= 0,
        "surplus",
        "shortage"
    )

    # ------------------------
    # Renewable generation
    # ------------------------

    renewable_columns = []

    possible_columns = [

        "Solar",
        "Wind Onshore",
        "Hydro Run-of-river and poundage",
        "Hydro Water Reservoir",
        "Biomass",

        "Solar_Actual Aggregated",
        "Wind Onshore_Actual Aggregated",
        "Hydro Run-of-river and poundage_Actual Aggregated",
        "Hydro Water Reservoir_Actual Aggregated",
        "Biomass_Actual Aggregated"

    ]

    for col in possible_columns:

        if col in df.columns:

            renewable_columns.append(col)

    df["renewable_generation_mw"] = (
        df[renewable_columns]
        .fillna(0)
        .sum(axis=1)
    )

    # ------------------------
    # Renewable share
    # ------------------------

    df["renewable_share"] = (
        df["renewable_generation_mw"]
        /
        df["actual_load_mw"]
    )

    df["renewable_share"] = (
        df["renewable_share"]
        .replace(
            [np.inf, -np.inf],
            np.nan
        )
        .fillna(0)
    )

    # ------------------------
    # Cost proxy
    # ------------------------

    df["imbalance_cost_proxy"] = (

        df["imbalance_abs_mw"]

        *

        df["price_eur_mwh"]

    )

    # ------------------------
    # Market Stress Index
    # ------------------------

    stress = (

        df["imbalance_abs_mw"]

        *

        df["price_eur_mwh"]

    )

    df["market_stress_index"] = (

        (stress - stress.min())

        /

        (stress.max() - stress.min())

    )

    # ------------------------
    # Percentiles
    # ------------------------

    price90 = df["price_eur_mwh"].quantile(
        0.90
    )

    imb95 = df["imbalance_abs_mw"].quantile(
        0.95
    )

    ren80 = df["renewable_share"].quantile(
        0.80
    )

    # ------------------------
    # Flags
    # ------------------------

    df["high_price_flag"] = (

        df["price_eur_mwh"]

        >

        price90

    )

    df["high_imbalance_flag"] = (

        df["imbalance_abs_mw"]

        >

        imb95

    )

    df["high_renewable_flag"] = (

        df["renewable_share"]

        >

        ren80

    )

    return df


# ==========================================================
# PROCESS COUNTRY
# ==========================================================

def process_country(country):

    print()
    print("=" * 70)
    print(f"PROCESSING {country.upper()}")
    print("=" * 70)

    file = (

        INPUT_DIR

        /

        f"{country}_balancing_market_features.csv"

    )

    df = pd.read_csv(file)

    df = create_risk_features(df)

    output = (

        OUTPUT_DIR

        /

        f"{country}_risk_features.csv"

    )

    df.to_csv(
        output,
        index=False
    )

    print("Saved:", output)

    print(df.shape)


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    for country in COUNTRIES:

        process_country(country)

    print()
    print("=" * 70)
    print("MARKET RISK FEATURES COMPLETED")
    print("=" * 70)