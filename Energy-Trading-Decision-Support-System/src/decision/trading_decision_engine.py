import os
import pandas as pd
import numpy as np


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]


RESULTS_PATH = os.path.join(
    BASE_DIR,
    "results"
)


OUTPUT_FILE = os.path.join(
    RESULTS_PATH,
    "trading_decisions_all_countries.csv"
)


os.makedirs(
    RESULTS_PATH,
    exist_ok=True
)



def generate_signal(row):

    price = row["day_ahead_price"]

    risk = row["risk_score"]

    imbalance_cost = row["imbalance_cost_eur"]

    renewable_share = row["renewable_share"]


    score = 0


    # Price opportunity

    if price < 40:
        score += 2

    elif price > 80:
        score -= 2



    # Renewable availability

    if renewable_share > 0.5:
        score -= 1



    # Risk adjustment

    if risk < 3:
        score += 1

    elif risk > 7:
        score -= 2



    # Cost exposure

    if imbalance_cost > 500000:
        score -= 2



    if score >= 2:

        return "BUY"


    elif score <= -2:

        return "SELL"


    else:

        return "HOLD"




def confidence(row):

    risk = row["risk_score"]


    value = 100 - (
        risk * 8
    )


    return max(
        0,
        min(
            100,
            value
        )
    )




all_results = []



for country in COUNTRIES:


    print("\n" + "="*70)

    print(country.upper())

    print("="*70)



    feature_file = os.path.join(
        BASE_DIR,
        "data",
        "features",
        f"{country}_features.csv"
    )


    risk_file = os.path.join(
        RESULTS_PATH,
        f"{country}_imbalance_risk.csv"
    )


    if not os.path.exists(feature_file):

        print(
            "Missing features"
        )

        continue


    if not os.path.exists(risk_file):

        print(
            "Missing risk results"
        )

        continue



    features = pd.read_csv(
        feature_file
    )


    risk = pd.read_csv(
        risk_file
    )


    df = features.merge(
        risk[
            [
                "timestamp",
                "imbalance_mw",
                "imbalance_cost_eur",
                "risk_score",
                "risk_level"
            ]
        ],
        on="timestamp",
        how="inner"
    )


    df["country"] = country



    df["trading_signal"] = df.apply(
        generate_signal,
        axis=1
    )


    df["confidence"] = df.apply(
        confidence,
        axis=1
    )



    all_results.append(
        df
    )


    print(
        "Signals generated:",
        len(df)
    )



if len(all_results) > 0:


    final = pd.concat(
        all_results,
        ignore_index=True
    )


    final = final[
        [
            "timestamp",
            "country",
            "day_ahead_price",
            "load_mw",
            "renewable_share",
            "imbalance_mw",
            "imbalance_cost_eur",
            "risk_score",
            "risk_level",
            "trading_signal",
            "confidence"
        ]
    ]


    final.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\n")
    print("="*70)
    print("TRADING DECISION ENGINE COMPLETED")
    print("="*70)


    print(
        final["trading_signal"]
        .value_counts()
    )


    print(
        "\nSaved:"
    )

    print(
        OUTPUT_FILE
    )



else:

    print(
        "No results generated"
    )