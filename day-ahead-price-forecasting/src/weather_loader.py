import requests
import pandas as pd


class WeatherLoader:


    def __init__(self):

        self.base_url = (
            "https://archive-api.open-meteo.com/v1/archive"
        )



    def get_weather(
        self,
        latitude,
        longitude,
        start,
        end
    ):


        params = {

            "latitude": latitude,

            "longitude": longitude,

            "start_date": start.strftime("%Y-%m-%d"),

            "end_date": end.strftime("%Y-%m-%d"),

            "hourly": [

                "temperature_2m",

                "wind_speed_10m",

                "shortwave_radiation",

                "cloud_cover",

                "precipitation"

            ],

            "timezone": "Europe/Berlin"

        }


        response = requests.get(
            self.base_url,
            params=params
        )


        response.raise_for_status()


        data = response.json()


        df = pd.DataFrame(
            data["hourly"]
        )


        df["datetime"] = pd.to_datetime(
            df["time"]
        )


        df.drop(
            columns=["time"],
            inplace=True
        )


        df.set_index(
            "datetime",
            inplace=True
        )


        return df