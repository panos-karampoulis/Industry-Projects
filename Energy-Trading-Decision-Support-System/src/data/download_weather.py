import requests
import pandas as pd

from pathlib import Path
from datetime import datetime, timedelta


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "weather"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# CONFIG
# ============================================================


INITIAL_START_DATE = "2020-01-01"


COUNTRIES = {

    "germany": {
        "lat": 52.5200,
        "lon": 13.4050
    },

    "france": {
        "lat": 48.8566,
        "lon": 2.3522
    },

    "spain": {
        "lat": 40.4168,
        "lon": -3.7038
    },

    "italy": {
        "lat": 41.9028,
        "lon": 12.4964
    },

    "netherlands": {
        "lat": 52.3676,
        "lon": 4.9041
    }

}



API_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
)



# ============================================================
# GET LAST TIMESTAMP
# ============================================================


def get_last_timestamp(
    file
):


    if not file.exists():

        return None



    df = pd.read_csv(
        file,
        parse_dates=[
            "timestamp"
        ]
    )


    if df.empty:

        return None



    return (
        df["timestamp"]
        .max()
    )




# ============================================================
# DOWNLOAD WEATHER
# ============================================================


def download_weather(
    country,
    lat,
    lon
):


    print()
    print("="*60)
    print(country.upper())
    print("="*60)



    output_file = (
        OUTPUT_DIR
        /
        f"{country}_weather.csv"
    )



    # ----------------------------------------
    # DATE RANGE
    # ----------------------------------------


    last_timestamp = get_last_timestamp(
        output_file
    )



    if last_timestamp is not None:


        start_date = (
            last_timestamp
            +
            timedelta(days=1)
        ).strftime(
            "%Y-%m-%d"
        )


        print(
            "Existing weather until:",
            last_timestamp
        )


    else:


        start_date = INITIAL_START_DATE


        print(
            "No existing weather data"
        )



    end_date = (
        datetime.utcnow()
        -
        timedelta(days=1)
    ).strftime(
        "%Y-%m-%d"
    )



    if start_date > end_date:


        print(
            "Weather already updated"
        )

        return



    print(
        "Downloading:",
        start_date,
        "→",
        end_date
    )



    # ----------------------------------------
    # API REQUEST
    # ----------------------------------------


    params = {


        "latitude": lat,

        "longitude": lon,


        "start_date": start_date,

        "end_date": end_date,


        "hourly": ",".join(

            [

                "temperature_2m",

                "wind_speed_10m",

                "shortwave_radiation",

                "cloud_cover",

                "precipitation"

            ]

        ),


        "timezone": "UTC"

    }



    response = requests.get(
        API_URL,
        params=params
    )



    if response.status_code != 200:


        print(
            "FAILED",
            response.status_code
        )


        print(
            response.text[:500]
        )


        return




    data = response.json()



    weather = pd.DataFrame(
        data["hourly"]
    )



    weather["timestamp"] = pd.to_datetime(

        weather["time"],

        utc=True

    )



    weather = weather.drop(
        columns=[
            "time"
        ]
    )



    weather["country"] = country



    weather = weather[

        [

            "timestamp",

            "country",

            "temperature_2m",

            "wind_speed_10m",

            "shortwave_radiation",

            "cloud_cover",

            "precipitation"

        ]

    ]



    # ----------------------------------------
    # MERGE WITH EXISTING
    # ----------------------------------------


    if output_file.exists():


        old = pd.read_csv(

            output_file,

            parse_dates=[
                "timestamp"
            ]

        )


        weather = pd.concat(

            [

                old,

                weather

            ],

            ignore_index=True

        )



    before = len(weather)



    weather = (

        weather

        .drop_duplicates(

            subset=[
                "timestamp"
            ],

            keep="last"

        )

        .sort_values(
            "timestamp"
        )

        .reset_index(
            drop=True
        )

    )



    after = len(weather)



    weather.to_csv(

        output_file,

        index=False

    )



    print()
    print(
        "Saved:",
        output_file
    )

    print(
        "Rows:",
        after
    )


    print(
        "Duplicates removed:",
        before-after
    )


    print(
        "Latest:",
        weather.timestamp.max()
    )




# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":



    print()
    print("="*80)
    print(
        "OPEN-METEO INCREMENTAL WEATHER UPDATE"
    )
    print("="*80)



    for country,info in COUNTRIES.items():


        download_weather(

            country,

            info["lat"],

            info["lon"]

        )



    print()
    print("="*80)
    print(
        "WEATHER UPDATE COMPLETED"
    )
    print("="*80)