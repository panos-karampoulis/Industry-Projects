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


BALANCING_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "balancing"
)


GENERATION_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "generation"
)


PRICE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)


OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_market_dataset"
)


os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)


# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]

# ============================================================
# MERGE FUNCTION
# ============================================================


def merge_country(country):


    print("\n")
    print("=" * 70)
    print(f"MERGING {country.upper()}")
    print("=" * 70)


    # --------------------------------------------------------
    # LOAD IMBALANCE
    # --------------------------------------------------------

    imbalance_file = os.path.join(
        BALANCING_PATH,
        f"{country}_imbalance.csv"
    )


    imbalance = pd.read_csv(
        imbalance_file
    )


    imbalance["timestamp"] = pd.to_datetime(
        imbalance["timestamp"],
        utc=True
    )


    print(
        "Imbalance:",
        imbalance.shape
    )


    # --------------------------------------------------------
    # LOAD GENERATION
    # --------------------------------------------------------

    generation_file = os.path.join(
        GENERATION_PATH,
        f"{country}_generation_features.csv"
    )


    generation = pd.read_csv(
        generation_file
    )


    generation["timestamp"] = pd.to_datetime(
        generation["timestamp"],
        utc=True
    )


    print(
        "Generation:",
        generation.shape
    )


    # --------------------------------------------------------
    # LOAD PRICES
    # --------------------------------------------------------

    price_file = os.path.join(
        PRICE_PATH,
        country,
        "day_ahead_prices.csv"
    )


    prices = pd.read_csv(
        price_file
    )


    prices["timestamp"] = pd.to_datetime(
        prices["timestamp"],
        utc=True
    )


    prices = prices[
        [
            "timestamp",
            "price_eur_mwh"
        ]
    ]


    print(
        "Prices:",
        prices.shape
    )


    # --------------------------------------------------------
    # MERGE
    # --------------------------------------------------------


    df = imbalance.merge(
        generation,
        on="timestamp",
        how="left"
    )


    df = df.merge(
        prices,
        on="timestamp",
        how="left"
    )


    df["country"] = country


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    df = df.sort_values(
        "timestamp"
    )


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    output_file = os.path.join(
        OUTPUT_PATH,
        f"{country}_balancing_market_features.csv"
    )


    df.to_csv(
        output_file,
        index=False
    )


    print(
        "FINAL DATASET:",
        df.shape
    )


    print(
        "Saved:",
        output_file
    )


# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    for country in COUNTRIES:

        try:

            merge_country(
                country
            )


        except Exception as e:

            print(
                "\nFAILED:",
                country
            )

            print(
                repr(e)
            )


    print("\n")
    print("=" * 70)
    print("BALANCING MARKET MERGE COMPLETED")
    print("=" * 70)