import requests
import pandas as pd


def get_future_weather(
        latitude,
        longitude,
        forecast_date
):

    """
    Download future weather forecast
    from Open-Meteo API
    """

    url = (
        "https://api.open-meteo.com/v1/forecast"
    )


    params = {

        "latitude": latitude,

        "longitude": longitude,

        "hourly": [

            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "cloud_cover",
            "surface_pressure",
            "shortwave_radiation"

        ],

        "start_date": forecast_date,

        "end_date": forecast_date,

        "timezone": "Europe/Berlin"

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


    weather = weather.drop(
        columns=["time"]
    )


    return weather