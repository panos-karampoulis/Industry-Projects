import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_market_dataset"
)


# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [
    "italy"
]


# ============================================================
# QUALITY CHECK
# ============================================================


def quality_check(country):

    print("\n")
    print("=" * 70)
    print(f"FINAL DATASET QUALITY: {country.upper()}")
    print("=" * 70)


    file = os.path.join(
        DATA_PATH,
        f"{country}_balancing_market_features.csv"
    )


    df = pd.read_csv(
        file
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    print("\nGENERAL")
    print("-" * 50)

    print(
        "Rows:",
        len(df)
    )

    print(
        "Columns:",
        len(df.columns)
    )

    print(
        "Start:",
        df["timestamp"].min()
    )

    print(
        "End:",
        df["timestamp"].max()
    )


    # Frequency

    freq = (
        df["timestamp"]
        .sort_values()
        .diff()
        .median()
    )


    print(
        "Frequency:",
        freq
    )


    # Duplicate timestamps

    duplicates = (
        df["timestamp"]
        .duplicated()
        .sum()
    )


    print(
        "Duplicate timestamps:",
        duplicates
    )


    # Missing values

    print("\nMISSING VALUES")
    print("-" * 50)


    missing = (
        df.isna()
        .sum()
        .sort_values(
            ascending=False
        )
    )


    print(
        missing[
            missing > 0
        ].head(15)
    )


    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    print("\nLOAD")
    print("-" * 50)


    if "actual_load_mw" in df.columns:

        print(
            df["actual_load_mw"]
            .describe()
        )


    # --------------------------------------------------------
    # IMBALANCE
    # --------------------------------------------------------

    print("\nIMBALANCE")
    print("-" * 50)


    if "imbalance_mw" in df.columns:

        print(
            df["imbalance_mw"]
            .describe()
        )


    # --------------------------------------------------------
    # GENERATION
    # --------------------------------------------------------

    print("\nGENERATION")
    print("-" * 50)


    generation_cols = [
        c for c in df.columns
        if (
            "Solar" in c
            or "Wind" in c
            or "Hydro" in c
            or "Biomass" in c
        )
    ]


    print(
        "Generation columns:",
        len(generation_cols)
    )


    print(
        generation_cols
    )


    # --------------------------------------------------------
    # PRICE
    # --------------------------------------------------------

    print("\nPRICE")
    print("-" * 50)


    if "price_eur_mwh" in df.columns:

        print(
            df["price_eur_mwh"]
            .describe()
        )


        print(
            "Negative prices:",
            (
                df["price_eur_mwh"] < 0
            ).sum()
        )


    print("\nQUALITY CHECK COMPLETED")


# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    for country in COUNTRIES:

        try:

            quality_check(
                country
            )


        except Exception as e:

            print(
                "FAILED:",
                country
            )

            print(
                repr(e)
            )