import argparse
from pathlib import Path

import pandas as pd
import yaml

from entsoe_client import get_client
from time_utils import convert_to_utc


BASE_DIR = Path(__file__).resolve().parent.parent


CONFIG_FILE = (
    BASE_DIR
    /
    "configs"
    /
    "countries.yaml"
)


with open(CONFIG_FILE, "r") as f:
    COUNTRIES = yaml.safe_load(f)



def download_load(country):

    country = country.lower()


    if country not in COUNTRIES:
        raise ValueError(
            f"Country '{country}' not found"
        )


    country_code = (
        COUNTRIES[country]["entsoe_code"]
    )


    timezone = (
        COUNTRIES[country]["timezone"]
    )


    print(
        f"Downloading load for {country}..."
    )


    client = get_client()


    start = pd.Timestamp(
        "2020-01-01",
        tz="Europe/Brussels"
    )


    end = pd.Timestamp(
        "2026-01-02",
        tz="Europe/Brussels"
    )


    load = client.query_load(
        country_code=country_code,
        start=start,
        end=end
    )


    load = load.reset_index()


    load.columns = [
        "datetime",
        "load_mwh"
    ]


    load = (
        load
        .set_index("datetime")
        .resample("1h")
        .mean()
        .dropna()
        .reset_index()
    )


    load = convert_to_utc(
        load,
        timezone=timezone
    )


    output_dir = (
        BASE_DIR
        /
        "data"
        /
        "raw"
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
        f"{country}_load.csv"
    )


    load.to_csv(
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


    download_load(
        args.country
    )