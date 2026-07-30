from pathlib import Path
import pandas as pd
import numpy as np


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "processed"


COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]


# ==========================================================
# QUALITY CHECK
# ==========================================================

def check_country(country):

    print("\n" + "=" * 70)
    print(country.upper())
    print("=" * 70)


    file = DATA_DIR / f"{country}_clean.csv"


    df = pd.read_csv(
        file,
        index_col=0,
        parse_dates=True
    )


    # ------------------------------------------------------
    # Basic information
    # ------------------------------------------------------

    print("\nShape:")
    print(df.shape)


    print("\nColumns:")
    print(list(df.columns))


    # ------------------------------------------------------
    # Date range
    # ------------------------------------------------------

    print("\nStart date:")
    print(df.index.min())


    print("\nEnd date:")
    print(df.index.max())


    # ------------------------------------------------------
    # Missing values
    # ------------------------------------------------------

    print("\nMissing values:")
    print(
        df.isna()
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    # ------------------------------------------------------
    # Duplicates
    # ------------------------------------------------------

    print("\nDuplicates:")
    print(
        df.index.duplicated()
        .sum()
    )


    # ------------------------------------------------------
    # Frequency
    # ------------------------------------------------------

    intervals = (
        df.index
        .to_series()
        .diff()
        .value_counts()
        .head()
    )


    print("\nMost common intervals:")
    print(intervals)


    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    print("\nStatistics:")
    print(
        df[
            [
                "load_mw",
                "day_ahead_price",
                "wind_generation",
                "solar_generation",
                "renewable_generation",
                "residual_load"
            ]
        ]
        .describe()
    )


    # ------------------------------------------------------
    # Correlations
    # ------------------------------------------------------

    print("\nCorrelation matrix:")

    print(
        df[
            [
                "day_ahead_price",
                "load_mw",
                "renewable_generation",
                "residual_load",
                "renewable_share"
            ]
        ]
        .corr()
        .round(3)
    )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:

        try:

            check_country(country)


        except Exception as e:

            print(
                f"{country} FAILED"
            )

            print(e)