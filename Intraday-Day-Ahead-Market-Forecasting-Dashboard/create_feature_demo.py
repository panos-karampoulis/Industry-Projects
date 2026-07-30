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

from pathlib import Path
import pandas as pd
import numpy as np


OUTPUT = Path(
    "demo_data/features"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True
)


timestamps = pd.date_range(
    start="2025-01-01",
    periods=5000,
    freq="15min"
)


df = pd.DataFrame({

    "timestamp": timestamps,

    "load_lag_1": np.random.normal(
        50000,5000,len(timestamps)
    ),

    "load_lag_24": np.random.normal(
        50000,5000,len(timestamps)
    ),

    "temperature": np.random.normal(
        15,8,len(timestamps)
    ),

    "wind_generation": np.random.uniform(
        0,20000,len(timestamps)
    ),

    "solar_generation": np.random.uniform(
        0,15000,len(timestamps)
    ),

    "hour": timestamps.hour,

    "day_of_week": timestamps.dayofweek,

    "month": timestamps.month,

    "holiday_flag": np.random.randint(
        0,2,len(timestamps)
    ),

    "price_lag_1": np.random.normal(
        80,20,len(timestamps)
    ),

    "price_lag_24": np.random.normal(
        80,20,len(timestamps)
    ),

    "rolling_mean_24": np.random.normal(
        80,10,len(timestamps)
    ),

    "rolling_std_24": np.random.uniform(
        5,20,len(timestamps)
    ),

    "renewable_share": np.random.uniform(
        0,1,len(timestamps)
    ),

    "demand_forecast": np.random.normal(
        50000,5000,len(timestamps)
    )

})


df.to_csv(
    OUTPUT /
    "europe_intraday_weather_features.csv",
    index=False
)


print("Feature dataset created")