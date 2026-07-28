# ============================================================
# DOWNLOAD ENTSOE DATA
# Day Ahead Price Forecasting
# ============================================================

import os
import time
import warnings

import pandas as pd

from dotenv import load_dotenv
from entsoe import EntsoePandasClient

warnings.filterwarnings("ignore")


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)

API_KEY = os.getenv("ENTSOE_API_KEY")

if API_KEY is None:
    raise ValueError(
        "ENTSOE_API_KEY not found inside .env"
    )

print("=" * 60)
print("API KEY LOADED")
print(API_KEY[:8] + "...")
print("=" * 60)


# ============================================================
# CLIENT
# ============================================================

client = EntsoePandasClient(
    api_key=API_KEY
)


# ============================================================
# COUNTRY
# ============================================================

COUNTRY = "DE_LU"


# ============================================================
# DATE RANGE
# ============================================================

START = pd.Timestamp(
    "2020-01-01",
    tz="Europe/Brussels"
)

END = pd.Timestamp(
    "2026-07-23",
    tz="Europe/Brussels"
)


# ============================================================
# OUTPUT FOLDER
# ============================================================

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "germany"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ============================================================
# SAVE FUNCTION
# ============================================================

def save_dataframe(df, filename):

    path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    df.to_csv(
        path,
        index=True
    )

    print("\nSaved ->", filename)

    print(df.head())

    print()

    print(df.tail())

    print()

    print("Shape:", df.shape)

    print()

    print("Columns:")

    print(df.columns.tolist())


# ============================================================
# CLEAN SERIES / DATAFRAME
# ============================================================

def ensure_dataframe(data, column_name=None):

    if isinstance(
        data,
        pd.Series
    ):

        if column_name is None:

            return data.to_frame()

        return data.to_frame(
            name=column_name
        )

    return data


# ============================================================
# PRINT SECTION
# ============================================================

def section(title):

    print()

    print("=" * 60)

    print(title)

    print("=" * 60)

# ============================================================
# DOWNLOAD DAY AHEAD PRICES
# ============================================================

section(
    "DOWNLOADING DAY AHEAD PRICES"
)


def download_prices():


    all_prices = []


    years = range(
        START.year,
        END.year + 1
    )


    for year in years:


        print()

        print(
            f"Downloading prices {year}"
        )


        start_year = pd.Timestamp(
            f"{year}-01-01",
            tz="Europe/Brussels"
        )


        end_year = pd.Timestamp(
            f"{year+1}-01-01",
            tz="Europe/Brussels"
        )


        try:


            data = client.query_day_ahead_prices(
                "DE_LU",
                start=start_year,
                end=end_year
            )


            data = ensure_dataframe(
                data,
                "price_eur_mwh"
            )


            all_prices.append(
                data
            )


            print(
                "OK:",
                data.shape
            )


        except Exception as e:


            print(
                "FAILED:",
                year
            )

            print(e)



    if len(all_prices) == 0:

        raise Exception(
            "No price data downloaded"
        )


    prices = pd.concat(
        all_prices
    )


    prices = prices[
        ~prices.index.duplicated()
    ]


    prices = prices.sort_index()


    save_dataframe(
        prices,
        "prices.csv"
    )


    return prices





# ============================================================
# DOWNLOAD ELECTRICITY LOAD
# ============================================================

section(
    "DOWNLOADING ELECTRICITY LOAD"
)


def download_load():

    try:

        load = client.query_load(
            COUNTRY,
            start=START,
            end=END
        )


        load = ensure_dataframe(
            load,
            "Actual Load"
        )


        # Ensure correct column name
        if len(load.columns) == 1:

            load.columns = [
                "Actual Load"
            ]


        save_dataframe(
            load,
            "load.csv"
        )


        return load


    except Exception as e:

        print()

        print("ERROR DOWNLOADING LOAD")

        print(e)

        raise e




# ============================================================
# DOWNLOAD GENERATION
# ============================================================

section(
    "DOWNLOADING GENERATION"
)


def download_generation():

    print("="*60)
    print("DOWNLOADING GENERATION")
    print("="*60)

    all_generation = []


    for year in range(2020, 2027):

        print(f"\nGeneration {year}")

        for month in range(1,13):
            # Stop future months (no ENTSO-E data available)
            if year == 2026 and month > 7:
                break

            start = pd.Timestamp(
                f"{year}-{month:02d}-01",
                tz="Europe/Brussels"
            )

            if month == 12:
                end = pd.Timestamp(
                    f"{year+1}-01-01",
                    tz="Europe/Brussels"
                )

            else:
                end = pd.Timestamp(
                    f"{year}-{month+1:02d}-01",
                    tz="Europe/Brussels"
                )


            try:

                print(
                    f"Downloading {year}-{month:02d}"
                )


                gen = client.query_generation(
                    COUNTRY,
                    start=start,
                    end=end,
                    psr_type=None
                )


                if isinstance(gen.columns, pd.MultiIndex):

                    gen.columns = [
                        "_".join(col).strip()
                        for col in gen.columns
                    ]


                all_generation.append(gen)


                print(
                    "OK:",
                    gen.shape
                )


                time.sleep(2)


            except Exception as e:

                print(
                    "FAILED:",
                    year,
                    month
                )

                print(e)

                continue



    generation = pd.concat(
        all_generation
    )


    generation = generation.sort_index()


    path = os.path.join(
        OUTPUT_FOLDER,
        "generation.csv"
    )


    generation.to_csv(path)


    print("\nSaved -> generation.csv")

    print(generation.head())

    print(generation.tail())

    print(
        "Shape:",
        generation.shape
    )


    return generation



# ============================================================
# VALIDATION
# ============================================================

def validate_dataset(df, name):

    print()
    print("-" * 60)
    print(name)
    print("-" * 60)

    print("Shape:")
    print(df.shape)

    print()

    print("Date range:")

    if isinstance(df.index, pd.DatetimeIndex):

        print(
            df.index.min()
        )

        print(
            df.index.max()
        )

    print()

    print("Missing values:")

    print(
        df.isna().sum().sum()
    )



# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    prices_path = os.path.join(
        OUTPUT_FOLDER,
        "prices.csv"
    )

    load_path = os.path.join(
        OUTPUT_FOLDER,
        "load.csv"
    )

    generation_path = os.path.join(
        OUTPUT_FOLDER,
        "generation.csv"
    )


    # ==========================
    # PRICES
    # ==========================

    if os.path.exists(prices_path):

        print("Loading existing prices.csv")

        prices = pd.read_csv(
            prices_path,
            index_col=0,
            parse_dates=True
        )

    else:

        prices = download_prices()



    # ==========================
    # LOAD
    # ==========================

    if os.path.exists(load_path):

        print("Loading existing load.csv")

        load = pd.read_csv(
            load_path,
            index_col=0,
            parse_dates=True
        )

    else:

        load = download_load()



    # ==========================
    # GENERATION
    # ==========================

    if os.path.exists(generation_path):

        print("Loading existing generation.csv")

        generation = pd.read_csv(
            generation_path,
            index_col=0,
            parse_dates=True
        )

    else:

        generation = download_generation()



    print()

    print("=" * 60)
    print("ENTSO-E DOWNLOAD COMPLETED")
    print("=" * 60)


    validate_dataset(
        prices,
        "DAY AHEAD PRICES"
    )


    validate_dataset(
        load,
        "ELECTRICITY LOAD"
    )


    validate_dataset(
        generation,
        "GENERATION"
    )


    print()

    print("=" * 60)
    print("FILES CREATED")
    print("=" * 60)


    print(OUTPUT_FOLDER)

    print(
        os.listdir(
            OUTPUT_FOLDER
        )
    )


    print()

    print("=" * 60)
    print("READY FOR DATA PROCESSING")
    print("=" * 60)