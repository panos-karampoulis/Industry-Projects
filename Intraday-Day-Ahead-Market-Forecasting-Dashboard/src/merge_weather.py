import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


INTRADAY_FILE = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "europe_intraday_features.csv"
)


WEATHER_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "weather"
)


OUTPUT_FILE = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "europe_intraday_weather_features.csv"
)



# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"

]



# ============================================================
# LOAD INTRADAY DATA
# ============================================================

print("="*60)
print("Loading intraday features")
print("="*60)


intraday = pd.read_csv(
    INTRADAY_FILE,
    parse_dates=[
        "timestamp",
        "local_timestamp"
    ]
)


print(
    intraday.head()
)


print(
    "Intraday shape:",
    intraday.shape
)



# ============================================================
# WEATHER PROCESSING FUNCTION
# ============================================================


def process_weather(country):


    print("="*60)
    print(
        f"Processing weather: {country}"
    )
    print("="*60)



    weather_file = (

        WEATHER_DIR
        /
        f"{country}_weather.csv"

    )


    weather = pd.read_csv(

        weather_file,

        parse_dates=[
            "timestamp"
        ]

    )


    print(
        "Original weather:",
        weather.shape
    )



    # timezone consistency

    if weather["timestamp"].dt.tz is None:

        weather["timestamp"] = (

            weather["timestamp"]
            .dt
            .tz_localize(
                "UTC"
            )

        )



    weather = (

        weather
        .set_index(
            "timestamp"
        )

    )



    # ========================================================
    # RESAMPLE WEATHER TO 15 MINUTES
    # ========================================================


    print(
        "Resampling weather..."
    )



    numeric_cols = (

        weather
        .select_dtypes(
            include=[
                "int64",
                "float64"
            ]
        )
        .columns

    )



    categorical_cols = (

        weather
        .select_dtypes(
            include=[
                "object"
            ]
        )
        .columns

    )



    # Numeric interpolation

    weather_numeric = (

        weather[numeric_cols]
        .resample(
            "15min"
        )
        .interpolate(
            method="time"
        )

    )



    # categorical forward fill

    if len(categorical_cols) > 0:


        weather_cat = (

            weather[categorical_cols]
            .resample(
                "15min"
            )
            .ffill()

        )


        weather = pd.concat(

            [

                weather_numeric,

                weather_cat

            ],

            axis=1

        )


    else:

        weather = weather_numeric



    weather = (

        weather
        .reset_index()

    )



    weather["country"] = country



    print(
        "Processed weather:",
        weather.shape
    )



    return weather




# ============================================================
# PROCESS ALL WEATHER DATA
# ============================================================


weather_list = []


for country in COUNTRIES:


    weather_country = process_weather(
        country
    )


    weather_list.append(
        weather_country
    )



weather_all = pd.concat(

    weather_list,

    ignore_index=True

)



print("="*60)
print("Weather dataset created")
print("="*60)


print(
    weather_all.shape
)



# ============================================================
# MERGE WEATHER + INTRADAY
# ============================================================


print("="*60)
print("Merging datasets")
print("="*60)



merged = pd.merge(

    intraday,

    weather_all,

    on=[
        "timestamp",
        "country"
    ],

    how="left"

)



print(
    "Merged shape:",
    merged.shape
)



# ============================================================
# CHECK MISSING VALUES
# ============================================================


print("="*60)
print("Missing values")
print("="*60)


missing = (

    merged
    .isna()
    .sum()
    .sort_values(
        ascending=False
    )

)


print(
    missing.head(20)
)



# ============================================================
# FINAL CLEAN
# ============================================================


merged = (

    merged
    .sort_values(

        [
            "country",
            "timestamp"

        ]

    )
    .reset_index(
        drop=True
    )

)



# ============================================================
# SAVE
# ============================================================


OUTPUT_FILE.parent.mkdir(

    exist_ok=True,

    parents=True

)


merged.to_csv(

    OUTPUT_FILE,

    index=False

)



print("="*60)
print("WEATHER MERGE COMPLETED")
print("="*60)


print(
    merged.head()
)


print(
    "Final shape:",
    merged.shape
)


print(
    "Saved:",
    OUTPUT_FILE
)