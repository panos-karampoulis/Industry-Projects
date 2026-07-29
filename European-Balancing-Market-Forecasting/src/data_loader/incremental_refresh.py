from pathlib import Path
import pandas as pd



ROOT = Path(
    r"D:\Portfolio\European-Balancing-Market-Forecasting"
)


DATA_DIR = (
    ROOT /
    "data" /
    "processed" /
    "final_market_dataset"
)



COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]



def check_latest_timestamp(country):


    file = (
        DATA_DIR /
        f"{country}_balancing_market_features.csv"
    )


    if not file.exists():

        print(
            f"{country}: dataset not found"
        )

        return None



    df = pd.read_csv(
        file,
        usecols=[
            "timestamp"
        ]
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )


    latest = df["timestamp"].max()


    print(
        f"{country.upper()} latest timestamp:"
    )

    print(
        latest
    )


    return latest





if __name__ == "__main__":


    print(
        """
============================================================
INCREMENTAL REFRESH CHECK
============================================================
"""
    )


    for country in COUNTRIES:

        check_latest_timestamp(
            country
        )