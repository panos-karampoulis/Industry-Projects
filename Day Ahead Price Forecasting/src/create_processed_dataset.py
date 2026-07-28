import pandas as pd
import os
import argparse


# ============================================================
# DATETIME PREPARATION
# ============================================================

def prepare_datetime(df):

    datetime_col = df.columns[0]

    df[datetime_col] = pd.to_datetime(
        df[datetime_col],
        errors="coerce",
        utc=True
    )

    df = df.dropna(
        subset=[datetime_col]
    )

    df = df.set_index(
        datetime_col
    )

    return df



# ============================================================
# CLEAN NUMERIC DATA
# ============================================================

def clean_numeric(df):

    for col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    # remove columns without data

    df = df.dropna(
        axis=1,
        how="all"
    )


    return df



# ============================================================
# RESAMPLING
# ============================================================

def hourly_resample(df):


    df = clean_numeric(
        df
    )


    df = df.resample(
        "1h"
    ).mean()


    return df



# ============================================================
# LOAD RAW FILES
# ============================================================

def load_raw_data(country):


    base_path = f"data/raw/{country}"


    print(
        f"Loading raw data from {base_path}"
    )


    prices = pd.read_csv(
        f"{base_path}/prices.csv"
    )


    load = pd.read_csv(
        f"{base_path}/load.csv"
    )


    generation = pd.read_csv(
        f"{base_path}/generation.csv"
    )


    return prices, load, generation



# ============================================================
# RENAME GENERATION COLUMNS
# ============================================================

def rename_generation_columns(df):


    rename = {}


    for col in df.columns:


        c = col.lower()


        if "solar" in c:

            rename[col] = "solar_mw"


        elif "wind offshore" in c:

            rename[col] = "wind_offshore_mw"


        elif "wind onshore" in c:

            rename[col] = "wind_onshore_mw"


        elif "biomass" in c:

            rename[col] = "biomass_mw"


        elif "gas" in c:

            rename[col] = "gas_mw"


        elif "brown coal" in c:

            rename[col] = "lignite_mw"


        elif "hard coal" in c:

            rename[col] = "hard_coal_mw"


        elif "hydro run" in c:

            rename[col] = "hydro_run_mw"


        elif "hydro water" in c:

            rename[col] = "hydro_reservoir_mw"


    df = df.rename(
        columns=rename
    )


    return df



# ============================================================
# PROCESS COUNTRY
# ============================================================

def process_country(country):


    print("="*70)
    print("CREATING PROCESSED DATASET")
    print("="*70)

    print(
        "Country:",
        country
    )


    prices, load, generation = load_raw_data(
        country
    )


    # datetime

    prices = prepare_datetime(
        prices
    )


    load = prepare_datetime(
        load
    )


    generation = prepare_datetime(
        generation
    )



    print("\nResampling hourly...")


    prices = hourly_resample(
        prices
    )


    load = hourly_resample(
        load
    )


    generation = hourly_resample(
        generation
    )


    # rename

    if "Actual Load" in load.columns:

        load = load.rename(
            columns={
                "Actual Load":"load_mw"
            }
        )


    prices.columns = [
        "price_eur_mwh"
    ]


    generation = rename_generation_columns(
        generation
    )


    # generation missing values

    generation = generation.fillna(
        0
    )



    print("\nDATA CHECK")

    print("\nPrices")
    print(
        prices.shape,
        prices.index.min(),
        prices.index.max()
    )


    print("\nLoad")
    print(
        load.shape,
        load.index.min(),
        load.index.max()
    )


    print("\nGeneration")
    print(
        generation.shape,
        generation.index.min(),
        generation.index.max()
    )



    print("\nMerging datasets...")


    df = prices.join(
        load,
        how="inner"
    )


    df = df.join(
        generation,
        how="inner"
    )


    df = df.sort_index()



    print("\nFINAL DATASET")

    print(
        df.head()
    )


    print("\nShape:")
    print(
        df.shape
    )


    print("\nDate range:")
    print(
        df.index.min(),
        df.index.max()
    )


    print("\nMissing values:")

    print(
        df.isna().sum()
    )



    # save


    output_path = (
        f"data/processed/{country}"
    )


    os.makedirs(
        output_path,
        exist_ok=True
    )


    output_file = (
        f"{output_path}/{country}_processed.csv"
    )


    df.to_csv(
        output_file
    )


    print("\nSaved:")
    print(
        output_file
    )


    print("\nDONE")



# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--country",
        required=True
    )


    args = parser.parse_args()


    process_country(
        args.country
    )