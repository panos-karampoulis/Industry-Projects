import pandas as pd

from src.loader import (
    load_energy_data,
    load_weather_data
)


def merge_energy_weather(country="Germany"):
    """
    Merge energy and weather datasets.
    """

    energy = load_energy_data(country)

    weather = load_weather_data(country)

    df = energy.merge(
        weather,
        on="datetime",
        how="left"
    )

    return df