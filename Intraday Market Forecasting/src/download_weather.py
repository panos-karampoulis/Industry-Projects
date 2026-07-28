import requests
import pandas as pd
from pathlib import Path
from datetime import datetime


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

START_DATE = "2020-01-01"
END_DATE = "2026-07-24"


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
# DOWNLOAD FUNCTION
# ============================================================


def download_weather(
    country,
    lat,
    lon
):


    print("="*60)
    print(country.upper())
    print("="*60)



    params = {

        "latitude": lat,

        "longitude": lon,

        "start_date": START_DATE,

        "end_date": END_DATE,


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



    # reorder columns

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



    output = (

        OUTPUT_DIR

        /

        f"{country}_weather.csv"

    )



    weather.to_csv(
        output,
        index=False
    )



    print(
        "Saved:",
        output
    )


    print(
        "Shape:",
        weather.shape
    )




# ============================================================
# MAIN
# ============================================================


for country, coords in COUNTRIES.items():


    download_weather(

        country,

        coords["lat"],

        coords["lon"]

    )



print("="*60)
print("WEATHER DOWNLOAD COMPLETED")
print("="*60)