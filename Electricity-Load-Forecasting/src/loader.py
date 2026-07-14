from pathlib import Path
import pandas as pd

from src.energy_loader import load_country_energy


BASE_DIR = Path(__file__).resolve().parent.parent


WEATHER_FILES = {

    "Germany":
        "weather_germany.csv",

    "France":
        "weather_france.csv",

    "Spain":
        "weather_spain.csv",

    "Netherlands":
        "weather_netherlands.csv"
}



def load_weather_data(country):

    file_path = (
        BASE_DIR
        / "data"
        / "raw"
        / WEATHER_FILES[country]
    )


    weather = pd.read_csv(
    file_path,
    parse_dates=["datetime"]
)


    weather["datetime"] = (
    weather["datetime"]
    .dt.tz_localize(None)
)
    
    
    


    return weather



def load_processed_data(country="Germany"):

    energy = load_country_energy(
        country
    )


    weather = load_weather_data(
        country
    )


    df = energy.merge(
        weather,
        on="datetime",
        how="left"
    )


    return df