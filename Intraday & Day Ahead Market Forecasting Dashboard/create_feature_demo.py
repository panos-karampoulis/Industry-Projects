from pathlib import Path
import pandas as pd
import numpy as np


OUTPUT_DIR = Path(
    "demo_data/feature_importance"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



features = [

    "load_lag_1",
    "load_lag_24",
    "temperature",
    "wind_generation",
    "solar_generation",
    "hour",
    "day_of_week",
    "month",
    "holiday_flag",
    "price_lag_1",
    "price_lag_24",
    "rolling_mean_24",
    "rolling_std_24",
    "renewable_share",
    "demand_forecast"

]



# -----------------------------
# Intraday
# -----------------------------

np.random.seed(42)


intraday = pd.DataFrame(

    {

        "Feature": features,

        "Importance": np.random.random(

            len(features)

        )

    }

)



intraday["Importance"] = (

    intraday["Importance"]

    /

    intraday["Importance"].sum()

)



intraday = intraday.sort_values(

    "Importance",

    ascending=False

)



intraday.to_csv(

    OUTPUT_DIR /

    "intraday_feature_importance.csv",

    index=False

)



# -----------------------------
# Day Ahead
# -----------------------------


day_ahead = pd.DataFrame(

    {

        "Feature": features,

        "Importance": np.random.random(

            len(features)

        )

    }

)



day_ahead["Importance"] = (

    day_ahead["Importance"]

    /

    day_ahead["Importance"].sum()

)



day_ahead = day_ahead.sort_values(

    "Importance",

    ascending=False

)



day_ahead.to_csv(

    OUTPUT_DIR /

    "day_ahead_feature_importance.csv",

    index=False

)



print("Feature importance demo files created")

print(

    list(

        OUTPUT_DIR.glob("*.csv")

    )

)