import os
import sys

from pathlib import Path


# ============================================================
# PROJECT PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


import pandas as pd
import numpy as np



# ============================================================
# PATHS
# ============================================================

INPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "balancing"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "analytics"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# RISK CLASSIFICATION
# ============================================================

def classify_imbalance(
    value
):

    value = abs(value)


    if value < 100:

        return "Normal"


    elif value < 500:

        return "Moderate"


    elif value < 1000:

        return "High"


    else:

        return "Extreme"





# ============================================================
# ANALYZE COUNTRY
# ============================================================

def analyze_country(
    country
):


    print()
    print("=" * 70)
    print(f"ANALYZING {country.upper()}")
    print("=" * 70)



    file = (
        INPUT_DIR
        /
        f"{country}_imbalance.csv"
    )



    if not file.exists():

        raise FileNotFoundError(
            f"Missing file: {file}"
        )



    df = pd.read_csv(
        file
    )



    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )



    # --------------------------------------------------------
    # Risk Features
    # --------------------------------------------------------


    df["imbalance_direction"] = np.where(

        df["imbalance_mw"] > 0,

        "Shortage",

        "Surplus"

    )



    df["risk_level"] = (

        df["imbalance_mw"]

        .apply(
            classify_imbalance
        )

    )



    df["absolute_imbalance_mw"] = (

        df["imbalance_mw"]

        .abs()

    )



    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------


    total_hours = len(df)



    shortage_hours = (

        df["imbalance_mw"] > 0

    ).sum()



    surplus_hours = (

        df["imbalance_mw"] < 0

    ).sum()



    extreme_events = (

        df["risk_level"]

        ==
        "Extreme"

    ).sum()



    report = {


        "country": country,


        "mean_imbalance_mw":

            df["imbalance_mw"].mean(),



        "imbalance_volatility_mw":

            df["imbalance_mw"].std(),



        "mean_absolute_error_mw":

            df["absolute_imbalance_mw"].mean(),



        "p95_imbalance_mw":

            df["absolute_imbalance_mw"]

            .quantile(
                0.95
            ),



        "maximum_shortage_mw":

            df["imbalance_mw"].max(),



        "maximum_surplus_mw":

            df["imbalance_mw"].min(),



        "shortage_percentage":

            shortage_hours
            /
            total_hours
            *
            100,



        "surplus_percentage":

            surplus_hours
            /
            total_hours
            *
            100,



        "extreme_events":

            extreme_events


    }



    events = df[

        df["risk_level"]

        ==
        "Extreme"

    ].copy()



    events["country"] = country



    return report, events





# ============================================================
# MAIN
# ============================================================

def run_analysis():


    countries = [

        "germany",

        "france",

        "italy",

        "netherlands",

        "spain"

    ]



    reports = []

    all_events = []



    for country in countries:


        try:


            report, events = analyze_country(
                country
            )


            reports.append(
                report
            )


            all_events.append(
                events
            )


        except Exception as e:


            print(
                "FAILED:",
                country
            )


            print(
                e
            )



    report_df = pd.DataFrame(
        reports
    )


    events_df = pd.concat(
        all_events,
        ignore_index=True
    )



    report_path = (

        OUTPUT_DIR

        /

        "imbalance_risk_report.csv"

    )


    events_path = (

        OUTPUT_DIR

        /

        "imbalance_events.csv"

    )



    report_df.to_csv(
        report_path,
        index=False
    )


    events_df.to_csv(
        events_path,
        index=False
    )



    print()
    print("=" * 70)
    print("IMBALANCE RISK REPORT")
    print("=" * 70)


    print(
        report_df
    )


    print()

    print(
        "Saved:",
        report_path
    )


    print(
        "Saved:",
        events_path
    )



if __name__ == "__main__":

    run_analysis()