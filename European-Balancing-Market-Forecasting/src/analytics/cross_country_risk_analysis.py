from pathlib import Path
import pandas as pd


# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


INPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "risk_dataset"
)


OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "analytics"
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
# LOAD
# ==========================================================

def load_country(country):

    file = (
        INPUT_DIR
        /
        f"{country}_risk_features.csv"
    )

    df = pd.read_csv(file)

    df["country"] = country

    return df



# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize(series):

    return (
        (series - series.min())
        /
        (series.max() - series.min())
    )



# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    print("=" * 70)
    print("ADVANCED COUNTRY RISK ANALYSIS")
    print("=" * 70)


    datasets = []


    for country in COUNTRIES:

        print(
            "Loading:",
            country
        )

        datasets.append(
            load_country(country)
        )


    full = pd.concat(
        datasets,
        ignore_index=True
    )


    # ======================================================
    # COUNTRY KPI TABLE
    # ======================================================

    summary = (

        full
        .groupby("country")
        .agg(

            imbalance_volatility=(
                "imbalance_mw",
                "std"
            ),


            extreme_events=(
                "high_imbalance_flag",
                "sum"
            ),


            avg_price=(
                "price_eur_mwh",
                "mean"
            ),


            price_volatility=(
                "price_eur_mwh",
                "std"
            ),


            high_price_events=(
                "high_price_flag",
                "sum"
            ),


            avg_renewable_share=(
                "renewable_share",
                "mean"
            ),


            renewable_volatility=(
                "renewable_share",
                "std"
            )

        )

        .reset_index()

    )


    # ======================================================
    # BALANCING RISK
    # ======================================================


    balancing = summary.copy()


    balancing["volatility_score"] = normalize(
        balancing["imbalance_volatility"]
    )


    balancing["event_score"] = normalize(
        balancing["extreme_events"]
    )


    balancing["balancing_risk_score"] = (

        balancing["volatility_score"] * 0.5

        +

        balancing["event_score"] * 0.3

    )


    balancing = balancing.sort_values(
        "balancing_risk_score",
        ascending=False
    )


    balancing["rank"] = range(
        1,
        len(balancing)+1
    )


    balancing.to_csv(

        OUTPUT_DIR
        /
        "balancing_risk_ranking.csv",

        index=False

    )


    # ======================================================
    # PRICE RISK
    # ======================================================


    price = summary.copy()


    price["price_volatility_score"] = normalize(
        price["price_volatility"]
    )


    price["high_price_score"] = normalize(
        price["high_price_events"]
    )


    price["price_risk_score"] = (

        price["price_volatility_score"] * 0.5

        +

        price["high_price_score"] * 0.5

    )


    price = price.sort_values(
        "price_risk_score",
        ascending=False
    )


    price["rank"] = range(
        1,
        len(price)+1
    )


    price.to_csv(

        OUTPUT_DIR
        /
        "price_risk_ranking.csv",

        index=False

    )


    # ======================================================
    # RENEWABLE RISK
    # ======================================================


    renewable = summary.copy()


    renewable["renewable_share_score"] = normalize(
        renewable["avg_renewable_share"]
    )


    renewable["renewable_volatility_score"] = normalize(
        renewable["renewable_volatility"]
    )


    renewable["renewable_risk_score"] = (

        renewable["renewable_share_score"] * 0.5

        +

        renewable["renewable_volatility_score"] * 0.5

    )


    renewable = renewable.sort_values(
        "renewable_risk_score",
        ascending=False
    )


    renewable["rank"] = range(
        1,
        len(renewable)+1
    )


    renewable.to_csv(

        OUTPUT_DIR
        /
        "renewable_risk_ranking.csv",

        index=False

    )


    print()
    print("=" * 70)
    print("RISK RANKINGS COMPLETED")
    print("=" * 70)


    print("\nBALANCING RISK")
    print(
        balancing[
            [
                "country",
                "balancing_risk_score",
                "rank"
            ]
        ]
    )


    print("\nPRICE RISK")
    print(
        price[
            [
                "country",
                "price_risk_score",
                "rank"
            ]
        ]
    )


    print("\nRENEWABLE RISK")
    print(
        renewable[
            [
                "country",
                "renewable_risk_score",
                "rank"
            ]
        ]
    )