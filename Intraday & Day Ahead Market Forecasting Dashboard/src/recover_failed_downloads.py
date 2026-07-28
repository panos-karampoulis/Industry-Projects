from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd
from entsoe import EntsoePandasClient

from config import ENTSOE_API_KEY, COUNTRIES

client = EntsoePandasClient(api_key=ENTSOE_API_KEY)

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"


FAILED = {

    "germany": {
        "generation": [2020]
    },

    "netherlands": {
        "generation": [2020]
    },

    "italy": {

        "load": [
            2023,
            2024,
            2025,
            2026
        ],

        "day_ahead": [
            2022,
            2023,
            2024,
            2025,
            2026
        ],

        "generation": [
            2022,
            2023,
            2024,
            2025,
            2026
        ]
    }

}


def save(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    print(f"Saved -> {path.name}")


for country, datasets in FAILED.items():

    print("\n" + "=" * 60)
    print(country.upper())
    print("=" * 60)

    folder = RAW_DIR / country

    for dataset, years in datasets.items():

        for year in years:

            print(f"\n{dataset.upper()}  {year}")

            start = pd.Timestamp(
                f"{year}-01-01",
                tz="Europe/Brussels"
            )

            end = pd.Timestamp(
                f"{year}-12-31",
                tz="Europe/Brussels"
            )

            try:

                if dataset == "load":

                    code = COUNTRIES[country]["load"]

                    df = client.query_load(
                        code,
                        start=start,
                        end=end
                    )

                    if isinstance(df, pd.Series):
                        df = df.to_frame("load_mw")

                    save(
                        df,
                        folder / f"load_{year}.csv"
                    )

                elif dataset == "day_ahead":

                    code = COUNTRIES[country]["price"]

                    df = client.query_day_ahead_prices(
                        code,
                        start=start,
                        end=end
                    )

                    df = df.to_frame("price_eur_mwh")

                    save(
                        df,
                        folder / f"day_ahead_{year}.csv"
                    )

                elif dataset == "generation":

                    code = COUNTRIES[country]["generation"]

                    df = client.query_generation(
                        code,
                        start=start,
                        end=end
                    )

                    save(
                        df,
                        folder / f"generation_{year}.csv"
                    )

            except Exception as e:

                print(f"FAILED -> {e}")

print("\nRecovery finished.")