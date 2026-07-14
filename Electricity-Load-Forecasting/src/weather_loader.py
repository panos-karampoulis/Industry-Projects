from pathlib import Path
import requests
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


COUNTRIES = {

    "France": {
        "lat": 48.8566,
        "lon": 2.3522
    },

    "Spain": {
        "lat": 40.4168,
        "lon": -3.7038
    },

    "Netherlands": {
        "lat": 52.3676,
        "lon": 4.9041
    }
}



def download_weather(country):

    coords = COUNTRIES[country]


    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={coords['lat']}"
        f"&longitude={coords['lon']}"
        "&start_date=2015-01-01"
        "&end_date=2020-09-30"
        "&hourly="
        "temperature_2m,"
        "wind_speed_10m,"
        "cloud_cover,"
        "shortwave_radiation"
        "&timezone=UTC"
    )


    response = requests.get(
        url
    )


    data = response.json()


    weather = pd.DataFrame(
        data["hourly"]
    )


    weather = weather.rename(
        columns={
            "time": "datetime",
            "temperature_2m": "temperature",
            "wind_speed_10m": "wind_speed",
            "shortwave_radiation": "solar_radiation"
        }
    )


    weather["datetime"] = pd.to_datetime(
        weather["datetime"]
    )


    output = (
        BASE_DIR
        / "data"
        / "raw"
        / f"weather_{country.lower()}.csv"
    )


    weather.to_csv(
        output,
        index=False
    )


    return weather