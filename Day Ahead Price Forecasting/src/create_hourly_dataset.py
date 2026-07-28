from pathlib import Path
import pandas as pd
import argparse



# ==========================================
# Arguments
# ==========================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Create hourly market dataset"
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
        default=1
    )


    return parser.parse_args()



# ==========================================
# Load CSV
# ==========================================

def load_csv(file):

    df = pd.read_csv(
        file
    )


    # first column is datetime

    df.rename(
        columns={
            df.columns[0]: "datetime"
        },
        inplace=True
    )


    df["datetime"] = pd.to_datetime(
        df["datetime"],
        utc=True
    )

    df["datetime"] = (
        df["datetime"]
        .dt.tz_convert(
            "Europe/Berlin"
        )
    )


    df = df.dropna(
        subset=["datetime"]
    )


    df = df.set_index(
        "datetime"
    )


    return df



# ==========================================
# Main
# ==========================================

def main():


    args = parse_arguments()


    country = args.country.lower()

    year = args.year

    month = args.month



    # ======================================
    # Paths
    # ======================================


    RAW_DIR = (

        Path("data/raw")

        /

        country

        /

        str(year)

        /

        f"{month:02d}"

    )


    OUTPUT_DIR = (

        Path("data/processed")

        /

        country

        /

        str(year)

        /

        f"{month:02d}"

    )



    print("="*60)

    print(
        "Creating hourly dataset"
    )

    print("="*60)


    print(
        f"Country: {country}"
    )

    print(
        f"Period: {year}-{month:02d}"
    )



    # -----------------------------
    # Prices
    # -----------------------------

    print("\nLoading prices...")


    prices = load_csv(

        RAW_DIR
        /
        "prices.csv"

    )


    prices.columns = [

        "price_eur_mwh"

    ]



    print(
        prices.head()
    )



    # -----------------------------
    # Load
    # -----------------------------

    print("\nLoading load...")


    load = load_csv(

        RAW_DIR
        /
        "load.csv"

    )


    load.columns = [

        "load_mw"

    ]



    load_hourly = (

        load

        .resample("1h")

        .mean()

    )



    # -----------------------------
    # Generation
    # -----------------------------

    print("\nLoading generation...")


    generation = load_csv(

        RAW_DIR
        /
        "generation.csv"

    )



    generation = generation.apply(

        pd.to_numeric,

        errors="coerce"

    )



    generation_hourly = (

        generation

        .resample("1h")

        .mean()

    )



    generation_hourly = (

        generation_hourly

        .fillna(0)

    )



    # -----------------------------
    # Merge
    # -----------------------------

    print("\nMerging datasets...")


    hourly = (

        prices

        .join(
            load_hourly,
            how="inner"
        )

        .join(
            generation_hourly,
            how="inner"
        )

    )



    hourly = hourly[

        ~hourly.index.duplicated()

    ]



    hourly = hourly.sort_index()



    print(
        "\nFinal dataset:"
    )


    print(
        hourly.head()
    )


    print(
        hourly.shape
    )



    # -----------------------------
    # Save
    # -----------------------------

    OUTPUT_DIR.mkdir(

        parents=True,

        exist_ok=True

    )



    output_file = (

        OUTPUT_DIR

        /

        "hourly_dataset.csv"

    )



    hourly.to_csv(

        output_file

    )



    print(
        "\nSaved:"
    )

    print(
        output_file
    )



if __name__ == "__main__":

    main()