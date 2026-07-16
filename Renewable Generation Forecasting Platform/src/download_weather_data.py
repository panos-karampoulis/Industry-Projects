import pandas as pd
import requests
import argparse
from pathlib import Path


# -------------------------
# Paths
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------
# Country coordinates
# -------------------------

COUNTRIES = {

    "germany": {
        "latitude": 51.1657,
        "longitude": 10.4515,
        "timezone": "Europe/Berlin"
    },

    "denmark": {
        "latitude": 56.2639,
        "longitude": 9.5018,
        "timezone": "Europe/Copenhagen"
    },

    "italy": {
        "latitude": 41.8719,
        "longitude": 12.5674,
        "timezone": "Europe/Rome"
    }

}


# -------------------------
# Arguments
# -------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--country",
    default="germany"
)

args = parser.parse_args()

COUNTRY = args.country.lower()


if COUNTRY not in COUNTRIES:
    raise ValueError(
        f"Unknown country: {COUNTRY}"
    )


# -------------------------
# Load generation dataset
# -------------------------

generation_file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    COUNTRY
    /
    "dataset.csv"
)


print("Loading generation dataset...")

df = pd.read_csv(
    generation_file,
    parse_dates=["datetime"]
)


start_date = (
    df["datetime"]
    .min()
    .strftime("%Y-%m-%d")
)


end_date = (
    df["datetime"]
    .max()
    .strftime("%Y-%m-%d")
)


print(
    "Period:",
    start_date,
    "to",
    end_date
)


# -------------------------
# Weather API
# -------------------------

coords = COUNTRIES[COUNTRY]


url = "https://archive-api.open-meteo.com/v1/archive"


params = {

    "latitude":
    coords["latitude"],

    "longitude":
    coords["longitude"],

    "start_date":
    start_date,

    "end_date":
    end_date,

    "hourly":

    ",".join([

        "temperature_2m",

        "relative_humidity_2m",

        "pressure_msl",

        "cloud_cover",

        "wind_speed_10m",

        "wind_direction_10m",

        "shortwave_radiation"

    ]),

    "timezone":
    coords["timezone"]

}


print("Downloading weather data...")


response = requests.get(
    url,
    params=params
)


if response.status_code != 200:

    raise Exception(
        response.text
    )


data = response.json()


# -------------------------
# Convert to dataframe
# -------------------------

weather = pd.DataFrame(
    {
        "datetime":
        data["hourly"]["time"],

        "temperature":
        data["hourly"]["temperature_2m"],

        "humidity":
        data["hourly"]["relative_humidity_2m"],

        "pressure":
        data["hourly"]["pressure_msl"],

        "cloud_cover":
        data["hourly"]["cloud_cover"],

        "wind_speed":
        data["hourly"]["wind_speed_10m"],

        "wind_direction":
        data["hourly"]["wind_direction_10m"],

        "solar_radiation":
        data["hourly"]["shortwave_radiation"]

    }
)


weather["datetime"] = pd.to_datetime(
    weather["datetime"]
)

# Keep only generation period

weather = weather[
    (weather["datetime"] >= df["datetime"].min())
    &
    (weather["datetime"] <= df["datetime"].max())
].reset_index(drop=True)


# -------------------------
# Save
# -------------------------

output_dir = (

    BASE_DIR
    /
    "data"
    /
    "weather"
    /
    COUNTRY

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


print()
print(
    "Weather saved:"
)

print(
    output_file
)


print()
print(
    weather.head()
)


print()
print(
    "Shape:",
    weather.shape
)