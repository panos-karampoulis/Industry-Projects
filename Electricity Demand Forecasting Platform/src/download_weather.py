import argparse
from pathlib import Path

import requests
import pandas as pd
import yaml

from time_utils import convert_to_utc



BASE_DIR = Path(__file__).resolve().parent.parent



CONFIG_FILE = (
    BASE_DIR
    /
    "configs"
    /
    "countries.yaml"
)


with open(CONFIG_FILE,"r") as f:
    COUNTRIES = yaml.safe_load(f)




def download_weather(country):


    country = country.lower()


    if country not in COUNTRIES:
        raise ValueError(
            f"Country '{country}' not found"
        )


    config = COUNTRIES[country]


    latitude = config["latitude"]

    longitude = config["longitude"]

    timezone = config["timezone"]



    print(
        f"Downloading weather for {country}..."
    )


    url = (
        "https://archive-api.open-meteo.com/v1/archive"
    )


    params = {


        "latitude": latitude,

        "longitude": longitude,


        "start_date":
        "2020-01-01",


        "end_date":
        "2026-01-02",


        "hourly":[


            "temperature_2m",

            "relative_humidity_2m",

            "wind_speed_10m",

            "cloud_cover",

            "surface_pressure",

            "shortwave_radiation"

        ],


        "timezone": timezone

    }



    response = requests.get(
        url,
        params=params
    )


    response.raise_for_status()


    data = response.json()



    weather = pd.DataFrame(
        data["hourly"]
    )


    weather["datetime"] = pd.to_datetime(
        weather["time"]
    )


    weather.drop(
        columns=["time"],
        inplace=True
    )


    weather = convert_to_utc(
        weather,
        timezone=timezone
    )



    output_dir = (
        BASE_DIR
        /
        "data"
        /
        "weather"
        /
        country
    )


    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )



    output_file = (
        output_dir
        /
        "weather.csv"
    )



    weather.to_csv(
        output_file,
        index=False
    )


    print(
        f"Saved:\n{output_file}"
    )


    return output_file





if __name__ == "__main__":


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--country",
        required=True
    )


    args = parser.parse_args()


    download_weather(
        args.country
    )