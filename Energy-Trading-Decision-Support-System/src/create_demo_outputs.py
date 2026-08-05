# ==========================================================
# CREATE DEMO OUTPUT FILES
# ENERGY TRADING DECISION SUPPORT SYSTEM
# ==========================================================


from pathlib import Path
import pandas as pd
import numpy as np



# ==========================================================
# PATHS
# ==========================================================


BASE_DIR = Path(__file__).resolve().parents[1]


DEMO_DIR = (
    BASE_DIR
    /
    "data"
    /
    "demo"
)


RESULT_DIR = (
    BASE_DIR
    /
    "results"
)



RESULT_DIR.mkdir(
    exist_ok=True
)



print("Creating demo outputs...")



# ==========================================================
# LOAD DEMO FEATURES
# ==========================================================


feature_file = (
    DEMO_DIR
    /
    "germany_features_sample.csv"
)


df = pd.read_csv(
    feature_file
)


df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    utc=True
)



print(
    "Features loaded:",
    df.shape
)



# ==========================================================
# 1. LOAD FORECAST OUTPUT
# ==========================================================


forecast = df[

    [
        "timestamp",
        "load_mw"

    ]

].copy()



forecast["forecast_load_mw"] = (

    forecast["load_mw"]

    *

    np.random.normal(
        1,
        0.015,
        len(forecast)
    )

)



forecast["forecast_error"] = (

    forecast["forecast_load_mw"]

    -

    forecast["load_mw"]

)



forecast.to_csv(

    RESULT_DIR
    /
    "load_forecast_demo.csv",

    index=False

)



print(
    "Created load forecast"
)





# ==========================================================
# 2. MODEL PERFORMANCE
# ==========================================================


metrics = pd.DataFrame(

    {

        "model":[

            "Linear Regression",

            "Random Forest",

            "XGBoost",

            "Prophet"

        ],


        "MAE":[

            1109.3,

            537.2,

            490.6,

            2820.2

        ],


        "RMSE":[

            1422.2,

            739.0,

            650.9,

            3719.0

        ],


        "MAPE":[

            0.0214,

            0.0104,

            0.0095,

            0.0563

        ]

    }

)



metrics.to_csv(

    RESULT_DIR
    /
    "model_metrics_demo.csv",

    index=False

)



print(
    "Created model metrics"
)





# ==========================================================
# 3. FEATURE IMPORTANCE
# ==========================================================


importance = pd.DataFrame(

    {


        "feature":[

            "load_lag_1",

            "load_lag_24",

            "day_ahead_price_lag_24",

            "renewable_generation",

            "wind_generation",

            "solar_generation"

        ],


        "importance":[

            0.916,

            0.035,

            0.021,

            0.012,

            0.009,

            0.007

        ]

    }

)



importance.to_csv(

    RESULT_DIR
    /
    "feature_importance_demo.csv",

    index=False

)



print(
    "Created feature importance"
)





# ==========================================================
# 4. BACKTESTING RESULTS
# ==========================================================


backtest = pd.DataFrame(

    {


        "timestamp":

        df["timestamp"],


        "actual_price":

        df["day_ahead_price"],


        "predicted_price":

        (

            df["day_ahead_price"]

            *

            np.random.normal(

                1,

                0.05,

                len(df)

            )

        )

    }

)



backtest["return"] = (

    backtest["predicted_price"]

    -

    backtest["actual_price"]

)



backtest.to_csv(

    RESULT_DIR
    /
    "backtesting_results.csv",

    index=False

)



print(
    "Created backtesting"
)





# ==========================================================
# 5. TRADE ANALYTICS
# ==========================================================


signals = pd.read_csv(

    DEMO_DIR
    /
    "trading_decisions_sample.csv"

)



signals["timestamp"] = pd.to_datetime(

    signals["timestamp"],

    utc=True

)



if "profit_loss" not in signals.columns:


    signals["profit_loss"] = np.random.normal(

        500,

        2000,

        len(signals)

    )




signals.to_csv(

    RESULT_DIR
    /
    "trade_analytics.csv",

    index=False

)



print(
    "Created trade analytics"
)



print(
    "\nALL DEMO OUTPUTS CREATED SUCCESSFULLY"
)