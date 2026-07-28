import os
import pandas as pd
from pathlib import Path
from entsoe import EntsoePandasClient


# ==========================================================
# CONFIG
# ==========================================================

API_KEY = "8969b923-bb59-481a-8a0f-37e88bdb5527"

client = EntsoePandasClient(api_key=API_KEY)


START_DATE = "2020-01-01"
END_DATE = "2026-07-24"


START = pd.Timestamp(START_DATE, tz="Europe/Brussels")
END = pd.Timestamp(END_DATE, tz="Europe/Brussels")


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"


# ==========================================================
# COUNTRIES
# ==========================================================
COUNTRIES = {

    "germany": {
        "load_generation": "DE_LU",
        "price": "DE_LU"
    },

    "netherlands": {
        "load_generation": "NL",
        "price": "NL"
    },

    "france": {
        "load_generation": "FR",
        "price": "FR"
    },

    "spain": {
        "load_generation": "ES",
        "price": "ES"
    },

    "italy": {
        "load_generation": "IT",
        "price": "10Y1001A1001A73I"
    }

}

# ==========================================================
# HELPERS
# ==========================================================

def save_dataframe(df, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(path)

    print(f"✅ Saved {path}")


def already_exists(path):

    return path.exists()


# ==========================================================
# LOAD
# ==========================================================

def download_load(country, code, folder):

    print("Downloading load...")

    output = folder / "load.csv"


    if already_exists(output):
        print("Already exists - skipping")
        return


    try:

        df = client.query_load(
            code,
            start=START,
            end=END
        )


        if isinstance(df, pd.Series):

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

def download_day_ahead(country, code, folder):

    print("Downloading day ahead...")


    output = folder / "day_ahead.csv"


    if already_exists(output):

        print("Already exists - skipping")
        return


    try:

        df = client.query_day_ahead_prices(
            code,
            start=START,
            end=END
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

def download_generation(country, code, folder):


    print("Downloading generation...")

    output = folder / "generation.csv"


    if already_exists(output):

        print("Already exists - skipping")
        return


    years = range(
        int(START_DATE[:4]),
        int(END_DATE[:4]) + 1
    )


    yearly_data = []


    try:


        for year in years:


            print(
                f"Generation {year}"
            )


            start = pd.Timestamp(
                f"{year}-01-01",
                tz="Europe/Brussels"
            )


            end = pd.Timestamp(
                f"{year}-12-31",
                tz="Europe/Brussels"
            )


            if end > END:
                end = END



            df = client.query_generation(
                code,
                start=start,
                end=end
            )


            yearly_data.append(df)



        generation = pd.concat(
            yearly_data
        )


        save_dataframe(
            generation,
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
        print("="*60)
        print(country.upper())
        print("="*60)


        folder = (
            RAW_DIR /
            country
        )


        load_generation_code = info["load_generation"]

        price_code = info["price"]



        download_load(
            country,
            load_generation_code,
            folder
        )


        download_day_ahead(
            country,
            price_code,
            folder
        )


        download_generation(
            country,
            load_generation_code,
            folder
        )



    print("\nDONE")