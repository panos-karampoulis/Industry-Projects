import pandas as pd
import os


countries = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]


for c in countries:

    print("\n")
    print("="*50)
    print(c.upper())
    print("="*50)


    df = pd.read_csv(
        f"data/risk/{c}_imbalance_risk.csv"
    )


    print(
        "Rows:",
        len(df)
    )


    print(
        "\nRisk statistics:"
    )

    print(
        df["risk_score"]
        .describe()
    )


    print(
        "\nHigh risk events:"
    )

    print(
        df["high_risk_event"]
        .sum()
    )


    print(
        "\nAverage imbalance MW:"
    )

    print(
        df["imbalance_mw"]
        .mean()
    )


    print(
        "\nMax imbalance MW:"
    )

    print(
        df["imbalance_abs"]
        .max()
    )