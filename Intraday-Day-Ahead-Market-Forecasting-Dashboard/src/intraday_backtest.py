import os
import pandas as pd
import numpy as np
import joblib


# =====================================================
# PATHS
# =====================================================

BASE_PATH = r"D:\Portfolio\Intraday Market Forecasting - updated"


FEATURE_FILE = os.path.join(
    BASE_PATH,
    "data",
    "processed",
    "europe_intraday_weather_features.csv"
)


MODEL_PATH = os.path.join(
    BASE_PATH,
    "models"
)


OUTPUT_PATH = os.path.join(
    BASE_PATH,
    "data",
    "backtesting"
)


os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)



# =====================================================
# COUNTRIES
# =====================================================

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]



# =====================================================
# MODEL FEATURES
# (MATCH NEW FEATURE BUILDER)
# =====================================================

FEATURES = [

    "hour",

    "day_of_week",

    "month",

    "weekend",

    "dst_flag",

    "is_peak",

    "is_off_peak",

    "night_period",

    "morning_ramp",

    "evening_peak",

    "lag_1",

    "lag_4",

    "lag_96",

    "lag_672",

    "rolling_mean_96",

    "rolling_std_96",

    "rolling_mean_672",

    "temperature_2m",

    "wind_speed_10m",

    "shortwave_radiation",

    "cloud_cover",

    "precipitation"

]



# =====================================================
# LOAD DATA
# =====================================================

print("Loading feature dataset...")


df = pd.read_csv(
    FEATURE_FILE
)


df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    utc=True
)


# =====================================================
# CREATE DST FLAG FOR OLD TRAINED MODEL
# =====================================================

local_time = (
    df["timestamp"]
    .dt.tz_convert("Europe/Berlin")
)


df["dst_flag"] = (
    local_time
    .apply(
        lambda x: int(x.dst() != pd.Timedelta(0))
    )
)




df = df.sort_values(
    [
        "country",
        "timestamp"
    ]
)



print("\nDataset coverage:")

print(
    df.groupby("country")
    ["timestamp"]
    .agg(
        [
            "min",
            "max",
            "count"
        ]
    )
)



results = []



# =====================================================
# BACKTEST LOOP
# =====================================================


for country in COUNTRIES:


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    data = df[
        df["country"] == country
    ].copy()



    if data.empty:

        print(
            "No data"
        )

        continue



    model_file = os.path.join(
        MODEL_PATH,
        country,
        "XGBoost.joblib"
    )



    if not os.path.exists(model_file):

        print(
            "Model missing:",
            model_file
        )

        continue



    model = joblib.load(
        model_file
    )



    # =================================================
    # REMOVE MISSING VALUES
    # =================================================


    missing_features = [

        col for col in FEATURES

        if col not in data.columns

    ]


    if missing_features:

        print(
            "Missing columns:",
            missing_features
        )

        continue



    data = data.dropna(
        subset=
        FEATURES +
        [
            "price_eur_mwh"
        ]
    )



    print(
        "Rows:",
        len(data)
    )



    if len(data)==0:

        print(
            "No rows after dropna"
        )

        continue



    X = data[
        FEATURES
    ]


    y = data[
        "price_eur_mwh"
    ]



    # =================================================
    # PREDICTION
    # =================================================


    predictions = model.predict(
        X
    )



    temp = pd.DataFrame(

        {

            "timestamp":
                data["timestamp"].values,


            "country":
                country,


            "actual_price":
                y.values,


            "forecast_price":
                predictions

        }

    )



    # =================================================
    # ERRORS
    # =================================================


    temp["error"] = (

        temp["forecast_price"]

        -

        temp["actual_price"]

    )



    temp["absolute_error"] = (

        temp["error"]
        .abs()

    )



    temp["percentage_error"] = (

        temp["absolute_error"]

        /

        temp["actual_price"]
        .replace(
            0,
            np.nan
        )

        *

        100

    )



    results.append(
        temp
    )



    print(
        "Completed:",
        len(temp)
    )




# =====================================================
# SAVE RESULTS
# =====================================================


if len(results)==0:

    raise ValueError(
        "No backtesting results generated"
    )



final = pd.concat(
    results,
    ignore_index=True
)



output_file = os.path.join(
    OUTPUT_PATH,
    "intraday_backtest_results.csv"
)



final.to_csv(
    output_file,
    index=False
)



print("\n")
print("="*60)
print("INTRADAY BACKTESTING COMPLETED")
print("="*60)


print(
    "Saved:",
    output_file
)


print("\nPreview:")

print(
    final.head()
)