import os
import pandas as pd
import numpy as np
import joblib


# ==========================================================
# CONFIG
# ==========================================================

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


FEATURES = [

    "load_mw",
    "load_lag_1",
    "load_lag_24",
    "load_lag_168",

    "wind_generation",
    "solar_generation",
    "renewable_generation",
    "renewable_share",

    "residual_load",

    "day_ahead_price",
    "day_ahead_price_lag_1",
    "day_ahead_price_lag_24",

    "hour",
    "day_of_week",
    "month",
    "weekend",

    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
    "month_sin",
    "month_cos"

]


PENALTY_FACTOR = 1.15


# ==========================================================
# IMBALANCE RISK FUNCTION
# ==========================================================


def calculate_risk(
        actual,
        forecast
):

    error = actual - forecast


    abs_error = np.abs(error)


    percentile = (
        abs_error.rank(pct=True)
    )


    risk_score = (
        percentile * 10
    )


    risk_level = np.where(

        risk_score < 4,
        "LOW",

        np.where(

            risk_score < 7,
            "MEDIUM",

            "HIGH"
        )
    )


    return (
        error,
        risk_score,
        risk_level
    )



# ==========================================================
# MAIN PIPELINE
# ==========================================================


all_results = []



for country in COUNTRIES:


    print("\n")
    print("="*70)
    print(country.upper())
    print("="*70)



    try:


        # --------------------------------------------------
        # LOAD FEATURES
        # --------------------------------------------------

        feature_path = os.path.join(

            BASE_DIR,
            "data",
            "features",
            f"{country}_features.csv"

        )


        df = pd.read_csv(
            feature_path
        )


        print(
            "Dataset:",
            df.shape
        )



        # --------------------------------------------------
        # LOAD MODEL
        # --------------------------------------------------

        model_path = os.path.join(
            BASE_DIR,
            "models",
            country,
            f"{country}_load_xgb.pkl"
        )


        model = joblib.load(
            model_path
        )


        print(
            "Model loaded:",
            model_path
        )



        # --------------------------------------------------
        # PREPARE INPUT
        # --------------------------------------------------

        X = df[FEATURES].copy()
        
        
        X = X.replace(
            [np.inf, -np.inf],
            np.nan
        )


        X = X.ffill()


        X = X.fillna(
            0
        )



        # --------------------------------------------------
        # FORECAST
        # --------------------------------------------------

        print(
            "Generating forecasts..."
        )


        forecast_load = model.predict(
            X
        )



        actual_load = df["load_mw"]



        # --------------------------------------------------
        # IMBALANCE
        # --------------------------------------------------

        print(
            "Calculating imbalance..."
        )


        imbalance_mw, risk_score, risk_level = calculate_risk(

            actual_load,
            forecast_load

        )



        imbalance_cost = (

            np.abs(imbalance_mw)

            *

            df["day_ahead_price"]

            *

            PENALTY_FACTOR

        )



        result = pd.DataFrame({

            "timestamp":
                df["timestamp"],


            "country":
                country,


            "actual_load_mw":
                actual_load,


            "forecast_load_mw":
                forecast_load,


            "imbalance_mw":
                imbalance_mw,


            "imbalance_cost_eur":
                imbalance_cost,


            "risk_score":
                risk_score,


            "risk_level":
                risk_level

        })



        # --------------------------------------------------
        # SAVE
        # --------------------------------------------------

        output_path = os.path.join(

            BASE_DIR,
            "results",
            f"{country}_imbalance_risk.csv"

        )


        result.to_csv(

            output_path,

            index=False

        )


        print()

        print(
            "Completed:",
            country
        )


        print(
            result["risk_level"]
            .value_counts()
        )


        print(
            "Saved:",
            output_path
        )



        all_results.append(
            result
        )



    except Exception as e:


        print(
            country.upper(),
            "FAILED"
        )

        print(e)



# ==========================================================
# SUMMARY
# ==========================================================


if len(all_results) > 0:


    final = pd.concat(
        all_results,
        ignore_index=True
    )


    final_path = os.path.join(

        BASE_DIR,
        "results",
        "all_countries_imbalance_risk.csv"

    )


    final.to_csv(

        final_path,

        index=False

    )


    print("\n")
    print("="*70)
    print("ALL COUNTRIES COMPLETED")
    print("="*70)


    print(final.groupby(
        "country"
    )["risk_score"].mean())


    print()

    print(
        "Saved:",
        final_path
    )

else:

    print(
        "No results generated"
    )