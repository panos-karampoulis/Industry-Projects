from pathlib import Path
import pandas as pd
import numpy as np
import joblib


# ======================================================
# PATHS
# ======================================================


PROJECT_ROOT = Path(__file__).resolve().parents[2]


DATA_DIR = (
    PROJECT_ROOT
    /
    "data"
    /
    "processed"
    /
    "risk_dataset"
)


OUTPUT_DIR = (
    PROJECT_ROOT
    /
    "data"
    /
    "analytics"
    /
    "forecasting"
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



# ======================================================
# FORECAST RISK
# ======================================================


def classify_risk(row):


    uncertainty = (

        row["upper_bound"]

        -

        row["lower_bound"]

    )


    imbalance = abs(

        row["forecast_imbalance"]

    )



    if imbalance > 1000 or uncertainty > 800:

        return "HIGH"


    elif imbalance > 500 or uncertainty > 400:

        return "MEDIUM"


    else:

        return "LOW"




# ======================================================
# FORECAST GENERATOR
# ======================================================


def generate_forecast(country):


    print()
    print("="*60)
    print(
        f"FORECASTING {country.upper()}"
    )
    print("="*60)



    file = (

        DATA_DIR

        /

        f"{country}_risk_features.csv"

    )


    df = pd.read_csv(file)



    df["timestamp"] = pd.to_datetime(

        df["timestamp"]

    )



    df = df.sort_values(

        "timestamp"

    )



    # τελευταίες 24 ώρες

    forecast_window = (

        df.tail(96)

        .copy()

    )



    # baseline forecast

    forecast_window[

        "forecast_imbalance"

    ] = (

        forecast_window["imbalance_mw"]

        .rolling(24)

        .mean()

    )



    forecast_window[

        "forecast_imbalance"

    ] = (

        forecast_window[

            "forecast_imbalance"

        ]

        .fillna(

            forecast_window["imbalance_mw"].mean()

        )

    )



    # uncertainty based on historical volatility

    volatility = (

        df["imbalance_mw"]

        .std()

    )



    forecast_window[

        "lower_bound"

    ] = (

        forecast_window["forecast_imbalance"]

        -

        1.96 * volatility

    )



    forecast_window[

        "upper_bound"

    ] = (

        forecast_window["forecast_imbalance"]

        +

        1.96 * volatility

    )



    forecast_window[

        "risk_level"

    ] = forecast_window.apply(

        classify_risk,

        axis=1

    )



    output = (

        OUTPUT_DIR

        /

        f"{country}_forecast.csv"

    )


    forecast_window[

        [

            "timestamp",

            "forecast_imbalance",

            "lower_bound",

            "upper_bound",

            "risk_level"

        ]

    ].to_csv(

        output,

        index=False

    )



    print(

        "Saved:",

        output

    )





# ======================================================
# RUN ALL
# ======================================================


if __name__ == "__main__":


    for country in COUNTRIES:


        generate_forecast(

            country

        )


    print()

    print(
        "NEXT DAY FORECAST COMPLETED"
    )