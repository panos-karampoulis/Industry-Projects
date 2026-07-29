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
# COUNTRY RISK ANALYSIS
# ==========================================================

def analyze_country(country):

    print()
    print("=" * 70)
    print(f"ANALYZING {country.upper()}")
    print("=" * 70)


    file = (
        INPUT_DIR
        /
        f"{country}_risk_features.csv"
    )


    df = pd.read_csv(file)


    # ------------------------------------------------------
    # General Risk Metrics
    # ------------------------------------------------------

    summary = {

        "country": country,

        "rows":
        len(df),


        "mean_imbalance_mw":
        df["imbalance_mw"].mean(),


        "imbalance_volatility_mw":
        df["imbalance_mw"].std(),


        "max_abs_imbalance_mw":
        df["imbalance_abs_mw"].max(),


        "imbalance_p95_mw":
        df["imbalance_abs_mw"].quantile(
            0.95
        ),


        "mean_market_stress":
        df["market_stress_index"].mean(),


        "max_market_stress":
        df["market_stress_index"].max(),


        "average_price":
        df["price_eur_mwh"].mean(),


        "price_volatility":
        df["price_eur_mwh"].std(),


        "renewable_share":
        df["renewable_share"].mean(),


        "shortage_percentage":
        (
            (df["imbalance_mw"] < 0)
            .mean()
            *
            100
        ),


        "surplus_percentage":
        (
            (df["imbalance_mw"] >= 0)
            .mean()
            *
            100
        )

    }


    # ------------------------------------------------------
    # Extreme Events
    # ------------------------------------------------------

    imbalance_threshold = (
        df["imbalance_abs_mw"]
        .quantile(0.99)
    )


    stress_threshold = (
        df["market_stress_index"]
        .quantile(0.99)
    )


    extreme = df[

        (df["imbalance_abs_mw"]
         >= imbalance_threshold)

        |

        (df["market_stress_index"]
         >= stress_threshold)

    ].copy()


    extreme["country"] = country


    # ------------------------------------------------------
    # Renewable Impact
    # ------------------------------------------------------

    renewable = pd.DataFrame({

        "country":
        [country],


        "average_renewable_share":
        [
            df["renewable_share"].mean()
        ],


        "renewable_volatility":
        [
            df["renewable_share"].std()
        ],


        "high_renewable_hours":
        [
            df["high_renewable_flag"]
            .sum()
        ],


        "average_imbalance_high_renewables":
        [

            df.loc[
                df["high_renewable_flag"],
                "imbalance_abs_mw"
            ]
            .mean()

        ]

    })


    # ------------------------------------------------------
    # Price / Imbalance relationship
    # ------------------------------------------------------

    correlation = (

        df[

            [

            "price_eur_mwh",

            "imbalance_abs_mw",

            "market_stress_index"

            ]

        ]

        .corr()

    )


    price_analysis = pd.DataFrame({

        "country":
        [country],


        "price_imbalance_correlation":
        [
            correlation
            .loc[
                "price_eur_mwh",
                "imbalance_abs_mw"
            ]
        ],


        "price_stress_correlation":
        [
            correlation
            .loc[
                "price_eur_mwh",
                "market_stress_index"
            ]
        ]

    })


    return (
        summary,
        extreme,
        renewable,
        price_analysis
    )



# ==========================================================
# MAIN PIPELINE
# ==========================================================

if __name__ == "__main__":


    summaries = []

    extremes = []

    renewables = []

    prices = []


    for country in COUNTRIES:


        result = analyze_country(
            country
        )


        summaries.append(
            result[0]
        )


        extremes.append(
            result[1]
        )


        renewables.append(
            result[2]
        )


        prices.append(
            result[3]
        )


    # ------------------------------------------------------
    # Save outputs
    # ------------------------------------------------------

    summary_df = pd.DataFrame(
        summaries
    )


    summary_df.to_csv(
        OUTPUT_DIR
        /
        "country_risk_summary.csv",
        index=False
    )


    extreme_df = pd.concat(
        extremes,
        ignore_index=True
    )


    extreme_df.to_csv(
        OUTPUT_DIR
        /
        "extreme_events.csv",
        index=False
    )


    renewable_df = pd.concat(
        renewables,
        ignore_index=True
    )


    renewable_df.to_csv(
        OUTPUT_DIR
        /
        "renewable_impact.csv",
        index=False
    )


    price_df = pd.concat(
        prices,
        ignore_index=True
    )


    price_df.to_csv(
        OUTPUT_DIR
        /
        "price_imbalance_analysis.csv",
        index=False
    )


    # Ranking

    ranking = summary_df.copy()


    ranking["risk_score"] = (

        ranking["mean_market_stress"]

        +

        ranking["imbalance_volatility_mw"]
        /
        ranking["imbalance_volatility_mw"].max()

        +

        ranking["price_volatility"]
        /
        ranking["price_volatility"].max()

    )


    ranking = ranking.sort_values(
        "risk_score",
        ascending=False
    )


    ranking.to_csv(
        OUTPUT_DIR
        /
        "country_rankings.csv",
        index=False
    )


    print()
    print("=" * 70)
    print("MARKET RISK ANALYSIS COMPLETED")
    print("=" * 70)