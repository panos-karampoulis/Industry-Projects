import argparse
from pathlib import Path

import pandas as pd



BASE_DIR = Path(__file__).resolve().parent.parent




def prepare_dataset(country):


    country = country.lower()


    print(
        "Loading datasets..."
    )



    load_file = (
        BASE_DIR
        /
        "data"
        /
        "raw"
        /
        country
        /
        f"{country}_load.csv"
    )


    weather_file = (
        BASE_DIR
        /
        "data"
        /
        "weather"
        /
        country
        /
        "weather.csv"
    )



    load = pd.read_csv(
        load_file,
        parse_dates=["datetime"]
    )


    weather = pd.read_csv(
        weather_file,
        parse_dates=["datetime"]
    )



    print(
        "Merging datasets..."
    )


    df = pd.merge(
        load,
        weather,
        on="datetime",
        how="inner"
    )



    output_dir = (
        BASE_DIR
        /
        "data"
        /
        "processed"
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
        "load_weather_dataset.csv"
    )



    df.to_csv(
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


    prepare_dataset(
        args.country
    )