import os
import joblib
import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = r"D:\Portfolio\Energy-Trading-Decision-Support-System"


FEATURE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "features"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "day_ahead"
)


OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "forecasts",
    "day_ahead_long_term"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


# Forecast horizon
FORECAST_DAYS = 30

FORECAST_HOURS = FORECAST_DAYS * 24



# ============================================================
# LONG TERM FORECAST FUNCTION
# ============================================================


def generate_forecast(country):


    print("\n" + "=" * 60)
    print(country.upper())
    print("=" * 60)



    # --------------------------------------------------------
    # Load Model
    # --------------------------------------------------------

    model_path = os.path.join(
        MODEL_DIR,
        f"{country}_xgb_day_ahead.pkl"
    )


    if not os.path.exists(model_path):

        print(
            "Missing model:",
            model_path
        )

        return



    model = joblib.load(
        model_path
    )



    # --------------------------------------------------------
    # Load Features
    # --------------------------------------------------------

    feature_path = os.path.join(
        FEATURE_DIR,
        f"{country}_day_ahead_features.csv"
    )


    if not os.path.exists(feature_path):

        print(
            "Missing features:",
            feature_path
        )

        return



    df = pd.read_csv(
        feature_path
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.sort_values(
        "timestamp"
    )



    # --------------------------------------------------------
    # Model Feature Schema
    # --------------------------------------------------------

    model_features = (
        model
        .get_booster()
        .feature_names
    )


    print(
        "Model features:"
    )

    print(
        model_features
    )



    # --------------------------------------------------------
    # Last available observation
    # --------------------------------------------------------

    last_row = (
        df
        .iloc[-1:]
        .copy()
    )


    last_time = (
        last_row["timestamp"]
        .iloc[0]
    )


    print(
        "Last timestamp:",
        last_time
    )



    # --------------------------------------------------------
    # Recursive Forecast
    # --------------------------------------------------------

    results = []


    previous_prediction = None



    for step in range(
        1,
        FORECAST_HOURS + 1
    ):



        future_time = (
            last_time
            +
            pd.Timedelta(
                hours=step
            )
        )



        row = last_row.copy()



        row["timestamp"] = future_time



        # Calendar features

        if "hour" in row.columns:

            row["hour"] = (
                future_time.hour
            )


        if "day_of_week" in row.columns:

            row["day_of_week"] = (
                future_time.dayofweek
            )


        if "month" in row.columns:

            row["month"] = (
                future_time.month
            )


        if "day_of_year" in row.columns:

            row["day_of_year"] = (
                future_time.dayofyear
            )



        # ----------------------------------------------------
        # Recursive price update
        # ----------------------------------------------------

        if previous_prediction is not None:


            if "price_eur_mwh" in row.columns:

                row["price_eur_mwh"] = (
                    previous_prediction
                )


            if "target" in row.columns:

                row["target"] = (
                    previous_prediction
                )


            if "lag_1" in row.columns:

                row["lag_1"] = (
                    previous_prediction
                )



        # ----------------------------------------------------
        # Missing features protection
        # ----------------------------------------------------

        for col in model_features:


            if col not in row.columns:

                row[col] = 0



        X_future = (
            row[model_features]
            .copy()
        )



        # ensure numeric

        X_future = X_future.astype(
            float
        )



        prediction = model.predict(
            X_future
        )[0]



        previous_prediction = prediction



        results.append(
            {
                "timestamp": future_time,
                "country": country,
                "forecast_price_eur_mwh": prediction,
                "forecast_hour": step,
                "model": "XGBoost"
            }
        )



    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    forecast_df = pd.DataFrame(
        results
    )


    output_file = os.path.join(
        OUTPUT_DIR,
        f"{country}_day_ahead_{FORECAST_DAYS}d_forecast.csv"
    )


    forecast_df.to_csv(
        output_file,
        index=False
    )


    print(
        "Forecast rows:",
        len(forecast_df)
    )


    print(
        "Saved:",
        output_file
    )


    # ========================================================
    # SAVE FORECAST ARCHIVE
    # ========================================================

    from datetime import datetime


    archive_date = datetime.now().strftime(
        "%Y-%m-%d"
    )


    archive_dir = os.path.join(

        BASE_DIR,

        "data",

        "forecasts",

        "archive",

        archive_date

    )


    os.makedirs(
        archive_dir,
        exist_ok=True
    )


    archive_file = os.path.join(

        archive_dir,

        f"{country}_day_ahead_forecast.csv"

    )


    forecast_df.to_csv(
        output_file,
        index=False
    )


    print(
        "Forecast rows:",
        len(forecast_df)
    )


    print(
        "Saved:",
        output_file
    )


    # ========================================================
    # SAVE FORECAST ARCHIVE
    # ========================================================

    from datetime import datetime


    archive_date = datetime.now().strftime(
        "%Y-%m-%d"
    )


    archive_dir = os.path.join(

        BASE_DIR,

        "data",

        "forecasts",

        "archive",

        archive_date

    )


    os.makedirs(
        archive_dir,
        exist_ok=True
    )


    archive_file = os.path.join(

        archive_dir,

        f"{country}_day_ahead_forecast.csv"

    )


    forecast_df.to_csv(

        archive_file,

        index=False

    )


    print(
        "Archived:",
        archive_file
    )




# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    for country in COUNTRIES:


        try:

            generate_forecast(
                country
            )


        except Exception as e:

            print(
                "ERROR:",
                country,
                e
            )



    print(
        "\nDAY AHEAD LONG TERM FORECAST COMPLETED"
    )