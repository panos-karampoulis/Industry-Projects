import pandas as pd
import numpy as np

from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


ANALYTICS_DIR = (
    BASE_DIR
    /
    "data"
    /
    "analytics"
)


ANALYTICS_DIR.mkdir(
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



# ============================================================
# PRICE ANALYSIS
# ============================================================


def analyze_prices(country):


    file = (
        PROCESSED_DIR
        /
        f"{country}_price_features.csv"
    )


    df = pd.read_csv(
        file
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    summary = {


        "country": country,


        "average_price":
            df["price_eur_mwh"].mean(),


        "price_std":
            df["price_eur_mwh"].std(),


        "minimum_price":
            df["price_eur_mwh"].min(),


        "maximum_price":
            df["price_eur_mwh"].max(),


        "negative_price_hours":
            (
                df["negative_price"]
                .sum()
            ),


        "negative_price_percentage":
            (
                df["negative_price"]
                .mean()
                *
                100
            )

    }


    return summary




# ============================================================
# LOAD ANALYSIS
# ============================================================


def analyze_load(country):


    file = (
        PROCESSED_DIR
        /
        f"{country}_load_features.csv"
    )


    df = pd.read_csv(
        file
    )


    summary = {


        "country": country,


        "average_load_mw":
            df["load_mw"].mean(),


        "max_load_mw":
            df["load_mw"].max(),


        "min_load_mw":
            df["load_mw"].min(),


        "load_volatility":
            df["load_mw"].std()

    }


    return summary




# ============================================================
# COUNTRY SUMMARY
# ============================================================


def create_market_summary():


    price_results = []


    load_results = []



    for country in COUNTRIES:


        print(
            "Analyzing:",
            country.upper()
        )


        price_results.append(

            analyze_prices(
                country
            )

        )


        load_results.append(

            analyze_load(
                country
            )

        )



    price_df = pd.DataFrame(
        price_results
    )


    load_df = pd.DataFrame(
        load_results
    )



    price_df.to_csv(

        ANALYTICS_DIR
        /
        "price_summary.csv",

        index=False

    )


    load_df.to_csv(

        ANALYTICS_DIR
        /
        "load_summary.csv",

        index=False

    )



    print()
    print("="*70)
    print("PRICE SUMMARY")
    print("="*70)

    print(
        price_df
    )


    print()
    print("="*70)
    print("LOAD SUMMARY")
    print("="*70)

    print(
        load_df
    )



# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    create_market_summary()


    print()

    print(
        "MARKET ANALYSIS COMPLETED"
    )