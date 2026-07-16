import requests
import pandas as pd
from pathlib import Path 


# Germany reference location
latitude = 52.52
longitude = 13.41


# Historical period
start_date = "2020-01-01"
end_date = "2025-12-31"


url = "https://archive-api.open-meteo.com/v1/archive"


params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "pressure_msl",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
        "cloud_cover",
        "shortwave_radiation",
        "direct_radiation",
        "sunshine_duration"
    ],
    "timezone": "Europe/Berlin"
}


response = requests.get(
    url,
    params=params
)


if response.status_code != 200:
    raise Exception(
        f"API Error: {response.status_code}"
    )


data = response.json()


# Convert to dataframe

df = pd.DataFrame(
    data["hourly"]
)


# Convert datetime

df["time"] = pd.to_datetime(
    df["time"]
)


# Add country column

df["country"] = "Germany"


# Save raw dataset

from pathlib import Path


# Project root directory
project_root = Path(__file__).resolve().parent.parent


output_path = (
    project_root
    / "data"
    / "raw"
    / "germany_weather.csv"
)


df.to_csv(
    output_path,
    index=False
)


print("Weather dataset downloaded successfully")
print(df.head())
print(df.shape)