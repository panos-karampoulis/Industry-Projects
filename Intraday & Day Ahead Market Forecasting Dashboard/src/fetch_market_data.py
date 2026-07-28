import pandas as pd
from pathlib import Path
from entsoe import EntsoePandasClient

import sys

# Add project root to path
BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


from config import (
    ENTSOE_API_KEY,
    COUNTRIES,
    START_YEAR,
    END_YEAR,
    END_DATE
)


# ==========================================================
# CLIENT
# ==========================================================

client = EntsoePandasClient(
    api_key=ENTSOE_API_KEY
)


RAW_DIR = (
    BASE_DIR /
    "data" /
    "raw"
)


# ==========================================================
# HELPERS
# ==========================================================

def get_year_range(year):

    start = pd.Timestamp(
        f"{year}-01-01",
        tz="Europe/Brussels"
    )


    if year == END_YEAR:

        end = pd.Timestamp(
            END_DATE,
            tz="Europe/Brussels"
        )

    else:

        end = pd.Timestamp(
            f"{year}-12-31",
            tz="Europe/Brussels"
        )


    return start, end



def save_dataframe(df, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    df.to_csv(
        path
    )


    print(
        f"Saved: {path}"
    )



def exists(path):

    return path.exists()



# ==========================================================
# LOAD
# ==========================================================

def download_load(code, year, folder):


    print(
        "Downloading load..."
    )


    output = (
        folder /
        f"load_{year}.csv"
    )


    if exists(output):

        print(
            "Already exists - skipping"
        )

        return



    start, end = get_year_range(
        year
    )


    try:


        df = client.query_load(
            code,
            start=start,
            end=end
        )


        if isinstance(
            df,
            pd.Series
        ):

            df = df.to_frame(
                name="load_mw"
            )


        save_dataframe(
            df,
            output
        )


    except Exception as e:

        print(
            f"Load failed: {e}"
        )



# ==========================================================
# DAY AHEAD
# ==========================================================

def download_day_ahead(code, year, folder):


    print(
        "Downloading day ahead..."
    )


    output = (
        folder /
        f"day_ahead_{year}.csv"
    )


    if exists(output):

        print(
            "Already exists - skipping"
        )

        return



    start, end = get_year_range(
        year
    )


    try:


        df = client.query_day_ahead_prices(
            code,
            start=start,
            end=end
        )


        df = df.to_frame(
            name="price_eur_mwh"
        )


        save_dataframe(
            df,
            output
        )


    except Exception as e:

        print(
            f"Day ahead failed: {e}"
        )



# ==========================================================
# GENERATION
# ==========================================================

def download_generation(code, year, folder):


    print(
        "Downloading generation..."
    )


    output = (
        folder /
        f"generation_{year}.csv"
    )


    if exists(output):

        print(
            "Already exists - skipping"
        )

        return



    start, end = get_year_range(
        year
    )


    try:


        df = client.query_generation(
            code,
            start=start,
            end=end
        )


        save_dataframe(
            df,
            output
        )


    except Exception as e:

        print(
            f"Generation failed: {e}"
        )



# ==========================================================
# MAIN
# ==========================================================


if __name__ == "__main__":


    for country, info in COUNTRIES.items():


        print("\n")
        print("="*70)
        print(country.upper())
        print("="*70)



        folder = (
            RAW_DIR /
            country
        )


        code_load = info["load"]

        code_price = info["price"]

        code_generation = info["generation"]



        for year in range(
            START_YEAR,
            END_YEAR + 1
        ):


            print("\n")
            print(
                f"YEAR {year}"
            )

            print(
                "-"*40
            )



            download_load(
                code_load,
                year,
                folder
            )



            download_day_ahead(
                code_price,
                year,
                folder
            )



            download_generation(
                code_generation,
                year,
                folder
            )



    print("\n")
    print("="*70)
    print("DOWNLOAD COMPLETED")
    print("="*70)