from pathlib import Path
import pandas as pd


import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.utils.data_loader import read_entsoe_csv

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "merged"
MERGED_DIR = BASE_DIR / "data" / "merged"

COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]

DATASETS = [
    "load",
    "day_ahead",
    "generation"
]


def merge_dataset(country, dataset):

    folder = DATA_DIR / country

    files = sorted(folder.glob(f"{dataset}_20*.csv"))

    if len(files) == 0:
        print(f"No files found for {country} - {dataset}")
        return

    dfs = []

    for file in files:

        print(f"Reading {file.name}")

        df = read_entsoe_csv(file)
        dfs.append(df)

    merged = pd.concat(dfs)

    merged = merged.sort_index()

    merged = merged[~merged.index.duplicated(keep="first")]

    output_folder = MERGED_DIR / country

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output = output_folder / f"{dataset}.csv"

    merged.to_csv(output)

    print("--------------------------------------")
    print(country.upper(), dataset.upper())
    print("Rows :", len(merged))
    print("Columns :", len(merged.columns))
    print("Saved ->", output)
    print("--------------------------------------\n")


if __name__ == "__main__":

    for country in COUNTRIES:

        print("\n")
        print("=" * 60)
        print(country.upper())
        print("=" * 60)

        for dataset in DATASETS:

            merge_dataset(
                country,
                dataset
            )

    print("\nMERGE COMPLETED")