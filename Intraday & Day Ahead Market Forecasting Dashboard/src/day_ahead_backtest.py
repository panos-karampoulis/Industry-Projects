import os
import joblib
import pandas as pd
import numpy as np


# =====================================================
# PATHS
# =====================================================

BASE_PATH = r"D:\Portfolio\Intraday Market Forecasting - updated"


FEATURE_PATH = os.path.join(
    BASE_PATH,
    "data",
    "features"
)


MODEL_PATH = os.path.join(
    BASE_PATH,
    "models",
    "day_ahead"
)


OUTPUT_PATH = os.path.join(
    BASE_PATH,
    "data",
    "backtesting",
    "day_ahead_backtest_results.csv"
)


os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)



COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]



# =====================================================
# MODEL FEATURES
# =====================================================

FEATURES = [
    "hour",
    "day_of_week",
    "month",
    "day_of_year",
    "lag_1",
    "lag_24",
    "lag_48",
    "lag_168",
    "rolling_mean_24",
    "rolling_std_24"
]



# =====================================================
# BACKTEST
# =====================================================


all_results = []



for country in COUNTRIES:


    print("="*60)
    print(country.upper())
    print("="*60)



    try:


        # -----------------------------
        # Load features
        # -----------------------------

        feature_file = os.path.join(
            FEATURE_PATH,
            f"{country}_day_ahead_features.csv"
        )


        df = pd.read_csv(
            feature_file
        )



        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            utc=True,
            errors="coerce"
        )


        df = df.sort_values(
            "timestamp"
        )


        print(
            "Rows:",
            len(df)
        )



        # -----------------------------
        # Load model
        # -----------------------------


        model_file = os.path.join(
            MODEL_PATH,
            f"{country}_xgb_day_ahead.pkl"
        )


        model = joblib.load(
            model_file
        )



        # -----------------------------
        # Prepare X
        # -----------------------------


        X = df[
            FEATURES
        ].copy()


        y_actual = df[
            "price_eur_mwh"
        ]



        # -----------------------------
        # Prediction
        # -----------------------------


        predictions = model.predict(
            X
        )



        result = pd.DataFrame({

            "timestamp":
                df["timestamp"],

            "country":
                country,

            "actual_price":
                y_actual,

            "forecast_price":
                predictions

        })



        # -----------------------------
        # Errors
        # -----------------------------


        result["error"] = (
            result["actual_price"]
            -
            result["forecast_price"]
        )


        result["absolute_error"] = (
            result["error"]
            .abs()
        )


        result["percentage_error"] = (
            result["absolute_error"]
            /
            result["actual_price"]
            .replace(0,np.nan)
            *
            100
        )



        print(
            "Completed:",
            len(result)
        )


        all_results.append(
            result
        )



    except Exception as e:

        print(
            "ERROR:",
            country,
            e
        )



# =====================================================
# SAVE
# =====================================================


if all_results:


    final_df = pd.concat(
        all_results,
        ignore_index=True
    )


    final_df.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print("="*60)
    print(
        "DAY AHEAD BACKTESTING COMPLETED"
    )
    print("="*60)


    print(
        "Saved:",
        OUTPUT_PATH
    )


    print(
        final_df.head()
    )


else:

    print(
        "No results generated"
    )