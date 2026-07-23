import pandas as pd
import requests

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"


# ---------------------------------------
# Forecast date
# ---------------------------------------

forecast_date = "2026-07-24"


# Germany coordinates
latitude = 52.52
longitude = 13.405



# ---------------------------------------
# Load future features
# ---------------------------------------

future_file = (
    BASE_DIR
    /
    "data"
    /
    "future"
    /
    country
    /
    f"future_features_{forecast_date}.csv"
)


future = pd.read_csv(
    future_file,
    parse_dates=["datetime"]
)

future["datetime"] = (
    pd.to_datetime(
        future["datetime"]
    )
)

# ---------------------------------------
# Open-Meteo request
# ---------------------------------------

print("Downloading weather forecast...")


url = (

    "https://api.open-meteo.com/v1/forecast?"

    f"latitude={latitude}"

    f"&longitude={longitude}"

    "&hourly="

    "temperature_2m,"

    "relative_humidity_2m,"

    "wind_speed_10m,"

    "cloud_cover,"

    "surface_pressure,"

    "shortwave_radiation"

    "&timezone=UTC"

)


response = requests.get(
    url
)


data = response.json()



weather_datetime = (
    pd.to_datetime(
        data["hourly"]["time"],
        utc=True
    )
    .tz_localize(None)
)


weather = pd.DataFrame({

    "datetime":
    weather_datetime,

    "temperature_2m":
    data["hourly"]["temperature_2m"],

    "relative_humidity_2m":
    data["hourly"]["relative_humidity_2m"],

    "wind_speed_10m":
    data["hourly"]["wind_speed_10m"],

    "cloud_cover":
    data["hourly"]["cloud_cover"],

    "surface_pressure":
    data["hourly"]["surface_pressure"],

    "shortwave_radiation":
    data["hourly"]["shortwave_radiation"]

})

print("\nFuture datetime:")
print(future["datetime"].head())

print("\nWeather datetime:")
print(weather["datetime"].head())

print("\nFuture range:")
print(
    future["datetime"].min(),
    future["datetime"].max()
)

print("\nWeather range:")
print(
    weather["datetime"].min(),
    weather["datetime"].max()
)

# ---------------------------------------
# Merge
# ---------------------------------------

future = future.merge(
    weather,
    on="datetime",
    how="left"
)



# ---------------------------------------
# Save
# ---------------------------------------

output_file = (
    BASE_DIR
    /
    "data"
    /
    "future"
    /
    country
    /
    f"future_weather_features_{forecast_date}.csv"
)



future.to_csv(
    output_file,
    index=False
)



print()

print(
    future.head()
)


print()

print(
    "Dataset shape:",
    future.shape
)


print()

print(
    f"Saved:\n{output_file}"
)