# ============================================================
# DOWNLOAD ENTSO-E DATA
# Multi Country Day Ahead Price Forecasting
# ============================================================

import os
import time
import warnings
import argparse

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


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env"
    )
)


API_KEY = os.getenv(
    "ENTSOE_API_KEY"
)


if API_KEY is None:

    raise ValueError(
        "ENTSOE_API_KEY not found"
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
# COUNTRY CONFIGURATION
# ============================================================

COUNTRIES = {


    "germany": {

        "code": "DE_LU"

    },


    "greece": {

        "code": "GR"

    },


    "spain": {

        "code": "ES"

    }


}



# ============================================================
# DATE RANGE
# ============================================================

START = pd.Timestamp(
    "2020-01-01",
    tz="Europe/Brussels"
)


END = pd.Timestamp.now(
    tz="Europe/Brussels"
)



# ============================================================
# HELPERS
# ============================================================


def section(title):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)



def ensure_dataframe(
        data,
        column_name=None
):

    if isinstance(
        data,
        pd.Series
    ):

        if column_name:

            return data.to_frame(
                name=column_name
            )


        return data.to_frame()


    return data



def save_dataframe(
        df,
        path,
        filename
):

    os.makedirs(
        path,
        exist_ok=True
    )


    file_path = os.path.join(
        path,
        filename
    )


    df.to_csv(
        file_path
    )


    print(
        "Saved ->",
        filename
    )


    print(
        "Shape:",
        df.shape
    )


    return file_path




# ============================================================
# DOWNLOAD PRICES
# ============================================================


def download_prices(
        country_code,
        output_folder
):


    section(
        "DOWNLOADING DAY AHEAD PRICES"
    )


    prices_all = []


    for year in range(
        START.year,
        END.year + 1
    ):


        print(
            f"Downloading prices {year}"
        )


        start = pd.Timestamp(
            f"{year}-01-01",
            tz="Europe/Brussels"
        )


        end = pd.Timestamp(
            f"{year+1}-01-01",
            tz="Europe/Brussels"
        )


        try:


            data = client.query_day_ahead_prices(

                country_code,

                start=start,

                end=end

            )


            data = ensure_dataframe(
                data,
                "price_eur_mwh"
            )


            prices_all.append(
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



    prices = pd.concat(
        prices_all
    )


    prices = prices[
        ~prices.index.duplicated()
    ]


    prices = prices.sort_index()



    save_dataframe(
        prices,
        output_folder,
        "prices.csv"
    )


    return prices

# ============================================================
# DOWNLOAD LOAD
# ============================================================


def download_load(
        country_code,
        output_folder
):


    section(
        "DOWNLOADING ELECTRICITY LOAD"
    )


    try:


        load = client.query_load(

            country_code,

            start=START,

            end=END

        )


        load = ensure_dataframe(
            load,
            "Actual Load"
        )


        if len(load.columns) == 1:

            load.columns = [
                "Actual Load"
            ]


        save_dataframe(
            load,
            output_folder,
            "load.csv"
        )


        return load



    except Exception as e:


        print(
            "LOAD DOWNLOAD FAILED"
        )

        print(e)

        return None





# ============================================================
# DOWNLOAD GENERATION
# ============================================================


def download_generation(
        country_code,
        output_folder
):


    section(
        "DOWNLOADING GENERATION"
    )


    all_generation = []



    for year in range(
        START.year,
        END.year + 1
    ):


        print()
        print(
            "Generation",
            year
        )


        for month in range(
            1,
            13
        ):


            # stop future months

            start = pd.Timestamp(

                f"{year}-{month:02d}-01",

                tz="Europe/Brussels"

            )


            if start >= END:

                break



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



            success = False



            for attempt in range(
                1,
                4
            ):


                try:


                    print(
                        f"Downloading {year}-{month:02d} attempt {attempt}"
                    )



                    gen = client.query_generation(

                        country_code,

                        start=start,

                        end=end,

                        psr_type=None

                    )



                    if isinstance(
                        gen.columns,
                        pd.MultiIndex
                    ):


                        gen.columns = [

                            "_".join(col).strip()

                            for col in gen.columns

                        ]



                    all_generation.append(
                        gen
                    )


                    print(
                        "OK:",
                        gen.shape
                    )


                    success = True


                    break



                except Exception as e:


                    print(
                        "FAILED"
                    )


                    print(e)


                    time.sleep(
                        5
                    )



            if not success:


                print(
                    f"Skipping {year}-{month:02d}"
                )




    if len(all_generation) == 0:


        print(
            "NO GENERATION DATA"
        )

        return None




    generation = pd.concat(
        all_generation
    )


    generation = generation.sort_index()



    save_dataframe(

        generation,

        output_folder,

        "generation.csv"

    )



    return generation






# ============================================================
# VALIDATION
# ============================================================


def validate_dataset(
        df,
        name
):


    print()
    print("-"*60)
    print(name)
    print("-"*60)



    if df is None:


        print(
            "NO DATA"
        )

        return



    print(
        "Shape:",
        df.shape
    )


    print(
        "Date:",
        df.index.min(),
        "->",
        df.index.max()
    )


    print(
        "Missing:",
        df.isna().sum().sum()
    )






# ============================================================
# PROCESS COUNTRY
# ============================================================


def process_country(
        country
):


    config = COUNTRIES[country]


    code = config["code"]



    output_folder = os.path.join(

        BASE_DIR,

        "data",

        "raw",

        country

    )


    os.makedirs(
        output_folder,
        exist_ok=True
    )



    print()
    print("#"*60)
    print(
        "COUNTRY:",
        country.upper()
    )
    print("#"*60)




    prices_path = os.path.join(
        output_folder,
        "prices.csv"
    )


    load_path = os.path.join(
        output_folder,
        "load.csv"
    )


    generation_path = os.path.join(
        output_folder,
        "generation.csv"
    )





    # -------------------------
    # PRICES
    # -------------------------


    if os.path.exists(
        prices_path
    ):


        print(
            "Existing prices.csv"
        )


        prices = pd.read_csv(

            prices_path,

            index_col=0,

            parse_dates=True

        )


    else:


        prices = download_prices(

            code,

            output_folder

        )





    # -------------------------
    # LOAD
    # -------------------------


    if os.path.exists(
        load_path
    ):


        print(
            "Existing load.csv"
        )


        load = pd.read_csv(

            load_path,

            index_col=0,

            parse_dates=True

        )


    else:


        load = download_load(

            code,

            output_folder

        )





    # -------------------------
    # GENERATION
    # -------------------------


    if os.path.exists(
        generation_path
    ):


        print(
            "Existing generation.csv"
        )


        generation = pd.read_csv(

            generation_path,

            index_col=0,

            parse_dates=True

        )


    else:


        generation = download_generation(

            code,

            output_folder

        )





    print()
    print(
        "DOWNLOAD COMPLETED:",
        country
    )



    validate_dataset(
        prices,
        "PRICES"
    )


    validate_dataset(
        load,
        "LOAD"
    )


    validate_dataset(
        generation,
        "GENERATION"
    )






# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":



    parser = argparse.ArgumentParser()


    parser.add_argument(

        "--country",

        required=False

    )


    args = parser.parse_args()





    if args.country:


        process_country(
            args.country.lower()
        )


    else:


        for country in COUNTRIES:


            process_country(
                country
            )



    print()
    print("="*60)
    print("ALL DOWNLOADS FINISHED")
    print("="*60)