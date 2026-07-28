import sys
from pathlib import Path
import argparse

import pandas as pd


# Add src to path
sys.path.append(
    str(Path(__file__).resolve().parents[1])
)


from data.weather_loader import WeatherLoader
from config.locations import COUNTRIES



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--country",
        required=True
    )

    parser.add_argument(
        "--year",
        type=int,
        required=True
    )

    parser.add_argument(
        "--month",
        type=int,
        required=True
    )


    args = parser.parse_args()


    country = args.country
    year = args.year
    month = args.month



    if country not in COUNTRIES:

        raise ValueError(
            f"Unknown country: {country}"
        )


    location = COUNTRIES[country]


    print("="*60)
    print("Downloading Weather Data")
    print("="*60)


    print(
        f"Country: {country}"
    )



    start = pd.Timestamp(
        year=year,
        month=month,
        day=1
    )


    end = (
        start
        +
        pd.offsets.MonthEnd(1)
    )



    # include next day for safety

    end = end + pd.Timedelta(days=1)



    loader = WeatherLoader()



    weather = loader.get_weather(

        latitude=location["lat"],

        longitude=location["lon"],

        start=start,

        end=end

    )



    output = Path(
        f"data/raw/weather/{country.lower()}/{year}/{month:02d}"
    )


    output.mkdir(
        parents=True,
        exist_ok=True
    )



    file = (
        output
        /
        "weather.csv"
    )


    weather.to_csv(
        file
    )


    print(
        "\nSaved:"
    )

    print(
        file
    )



if __name__ == "__main__":

    main()