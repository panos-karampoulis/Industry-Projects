import pandas as pd
import os


BASE_PATH = "data/features"
RISK_PATH = "D:/Portfolio/European-Balancing-Market-Forecasting/data/processed/risk_dataset"


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


def merge_country(country):

    print("\nProcessing:", country)


    # -----------------------------
    # Trading features
    # -----------------------------

    trading_file = (
        f"{BASE_PATH}/{country}_features.csv"
    )

    trading = pd.read_csv(trading_file)


    # timestamp fix
    trading.rename(
        columns={
            "Unnamed: 0": "timestamp"
        },
        inplace=True
    )


    trading["timestamp"] = pd.to_datetime(
        trading["timestamp"],
        utc=True
    )


    # -----------------------------
    # Risk features
    # -----------------------------

    risk_file = (
        f"{RISK_PATH}/{country}_risk_features.csv"
    )


    risk = pd.read_csv(
        risk_file
    )


    risk["timestamp"] = pd.to_datetime(
        risk["timestamp"],
        utc=True
    )


    risk = risk[
        [
            "timestamp",
            "imbalance_abs",
            "renewable_risk",
            "generation_risk",
            "price_volatility_24",
            "high_risk_event"
        ]
    ]


    # -----------------------------
    # Merge
    # -----------------------------

    merged = pd.merge_asof(
        trading.sort_values("timestamp"),
        risk.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("30min")
    )


    output = (
        f"{BASE_PATH}/"
        f"{country}_features_with_risk.csv"
    )


    merged.to_csv(
        output,
        index=False
    )


    print(
        "Saved:",
        output,
        merged.shape
    )



if __name__ == "__main__":


    for c in COUNTRIES:
        merge_country(c)