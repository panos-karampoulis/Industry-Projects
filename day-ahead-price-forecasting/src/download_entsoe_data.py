from pathlib import Path
import sys
import argparse
import pandas as pd
import time


# ==================================================
# Add project root
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)

sys.path.append(
    str(BASE_DIR / "src")
)


# ==================================================
# Imports
# ==================================================

from data.entsoe_loader import EntsoeLoader

from config.countries import COUNTRIES

from config.settings import RAW_DATA_DIR



# ==================================================
# Arguments
# ==================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Download ENTSO-E market data"
    )


    parser.add_argument(
        "--country",
        type=str,
        default="Germany"
    )


    parser.add_argument(
        "--year",
        type=int,
        default=2020
    )


    parser.add_argument(
        "--month",
        type=int,
        default=None
    )


    return parser.parse_args()



# ==================================================
# Retry wrapper
# ==================================================

def download_with_retry(
        func,
        retries=3,
        wait_seconds=30
):

    for attempt in range(retries):

        try:

            return func()


        except Exception as e:

            print(
                f"\nAttempt {attempt + 1}/{retries} failed"
            )

            print(e)


            if attempt < retries - 1:

                print(
                    f"Waiting {wait_seconds} seconds before retry..."
                )

                time.sleep(
                    wait_seconds
                )


    raise Exception(
        "Download failed after retries"
    )



# ==================================================
# Save dataframe
# ==================================================

def save_dataframe(
        df,
        filepath
):

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    df.to_csv(
        filepath
    )


    print(
        f"Saved: {filepath}"
    )



# ==================================================
# Main
# ==================================================

def main():


    args = parse_arguments()


    country = args.country

    year = args.year

    month = args.month



    # ----------------------------------------------
    # Country validation
    # ----------------------------------------------

    if country not in COUNTRIES:

        raise ValueError(
            f"Country {country} not found"
        )



    country_config = COUNTRIES[country]


    code = country_config["code"]

    domain = country_config["domain"]

    timezone = country_config["timezone"]



    # ----------------------------------------------
    # Dates
    # ----------------------------------------------

    if month:


        start = pd.Timestamp(
            f"{year}-{month:02d}-01",
            tz=timezone
        )


        end = (
            start
            + pd.offsets.MonthEnd(1)
            + pd.Timedelta(days=1)
        )


    else:


        start = pd.Timestamp(
            f"{year}-01-01",
            tz=timezone
        )


        end = pd.Timestamp(
            f"{year+1}-01-01",
            tz=timezone
        )


    # 2026 partial year

    if year == 2026 and month is None:


        end = pd.Timestamp(
            "2026-07-24",
            tz=timezone
        )



    print("\n" + "="*60)

    print(
        f"Downloading ENTSO-E data: {country}"
    )

    print(
        f"Period: {start} -> {end}"
    )

    print("="*60)



    # ----------------------------------------------
    # Output directory
    # ----------------------------------------------

    if month:


        output_dir = (

            RAW_DATA_DIR

            /

            country.lower()

            /

            str(year)

            /

            f"{month:02d}"

        )


    else:


        output_dir = (

            RAW_DATA_DIR

            /

            country.lower()

            /

            str(year)

        )



    loader = EntsoeLoader()



    # ----------------------------------------------
    # Prices
    # ----------------------------------------------

    price_file = (
        output_dir
        /
        "prices.csv"
    )


    if price_file.exists():

        print(
            "\nPrices already exist - skipping"
        )

    else:


        print(
            "\nDownloading prices..."
        )


        prices = download_with_retry(

            lambda:

                loader.get_day_ahead_prices(

                    code,

                    start,

                    end

                )

        )


        save_dataframe(
            prices,
            price_file
        )



    # ----------------------------------------------
    # Load
    # ----------------------------------------------

    load_file = (
        output_dir
        /
        "load.csv"
    )


    if load_file.exists():

        print(
            "\nLoad already exists - skipping"
        )

    else:


        print(
            "\nDownloading load..."
        )


        load = download_with_retry(

            lambda:

                loader.get_load(

                    code,

                    start,

                    end

                )

        )


        save_dataframe(
            load,
            load_file
        )



    # ----------------------------------------------
    # Generation
    # ----------------------------------------------

    generation_file = (
        output_dir
        /
        "generation.csv"
    )


    if generation_file.exists():

        print(
            "\nGeneration already exists - skipping"
        )

    else:


        print(
            "\nDownloading generation..."
        )


        generation = download_with_retry(

            lambda:

                loader.get_generation(

                    code,

                    start,

                    end

                )

        )


        save_dataframe(
            generation,
            generation_file
        )



    print(
        "\n" + "="*60
    )

    print(
        "Download completed successfully"
    )

    print("="*60)



# ==================================================
# Run
# ==================================================

if __name__ == "__main__":

    main()