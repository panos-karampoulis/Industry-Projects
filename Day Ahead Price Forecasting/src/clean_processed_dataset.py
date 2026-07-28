# ============================================================
# GENERIC DATA CLEANING
# Day Ahead Price Forecasting
# Multi Country
# ============================================================

import pandas as pd
import numpy as np
import os
import argparse



# ============================================================
# PATHS
# ============================================================


def get_paths(country):

    raw_path = (
        f"data/raw/{country}"
    )

    processed_path = (
        f"data/processed/{country}"
    )

    os.makedirs(
        processed_path,
        exist_ok=True
    )

    return raw_path, processed_path




# ============================================================
# LOAD RAW DATA
# ============================================================


def load_raw_data(country):


    raw_path, _ = get_paths(country)


    print("="*70)
    print("LOADING RAW DATA")
    print("="*70)


    print(raw_path)


    prices = pd.read_csv(
        f"{raw_path}/prices.csv",
        index_col=0,
        parse_dates=True
    )


    load = pd.read_csv(
        f"{raw_path}/load.csv",
        index_col=0,
        parse_dates=True
    )


    generation = pd.read_csv(
        f"{raw_path}/generation.csv",
        index_col=0,
        parse_dates=True
    )


    return prices, load, generation





# ============================================================
# DATETIME
# ============================================================


def prepare_datetime(df):


    # convert mixed timezones to UTC

    df.index = pd.to_datetime(
        df.index,
        utc=True
    )


    df = df.sort_index()


    return df





# ============================================================
# NUMERIC CLEANING
# ============================================================


def numeric_clean(df):


    for col in df.columns:


        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    return df




# ============================================================
# FIND COLUMN
# ============================================================


def find_column(
        df,
        keywords
):


    for col in df.columns:


        name = col.lower()


        if all(
            k.lower() in name
            for k in keywords
        ):

            return col



    return None





# ============================================================
# GENERATION STANDARDIZATION
# ============================================================


def standardize_generation(
        generation
):


    generation = numeric_clean(
        generation
    )


    # remove empty columns

    generation = generation.dropna(
        axis=1,
        how="all"
    )


    output = pd.DataFrame(
        index=generation.index
    )



    mapping = {


        "solar_mw":[
            ["solar"]
        ],


        "wind_onshore_mw":[
            ["wind","onshore"]
        ],


        "wind_offshore_mw":[
            ["wind","offshore"]
        ],


        "gas_mw":[
            ["gas"]
        ],


        "lignite_mw":[
            [
                "lignite"
            ],
            [
                "brown",
                "coal"
            ]
        ],


        "oil_mw":[
            [
                "oil"
            ]
        ],


        "hydro_reservoir_mw":[
            [
                "reservoir"
            ],
            [
                "water",
                "reservoir"
            ]
        ],


        "hydro_pumped_mw":[
            [
                "pumped"
            ]
        ],


        "storage_mw":[
            [
                "storage"
            ]
        ]

    }




    for new_name, patterns in mapping.items():


        found = None


        for pattern in patterns:


            found = find_column(
                generation,
                pattern
            )


            if found:

                break



        if found:


            print(
                "Found:",
                new_name,
                "<-",
                found
            )


            output[new_name] = generation[found]



    return output






# ============================================================
# HOURLY RESAMPLE
# ============================================================


def hourly_resample(df):


    df = numeric_clean(
        df
    )


    df = df.resample(
        "1h"
    ).mean()


    return df





# ============================================================
# CREATE DATASET
# ============================================================


def clean_dataset(country):


    print("="*70)
    print("CLEANING DATASET")
    print("="*70)

    print(
        "Country:",
        country
    )



    prices, load, generation = load_raw_data(
        country
    )



    prices = prepare_datetime(
        prices
    )

    load = prepare_datetime(
        load
    )

    generation = prepare_datetime(
        generation
    )



    print("\nStandardizing generation...")


    generation = standardize_generation(
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




    # rename price

    if len(prices.columns)==1:

        prices.columns=[
            "price_eur_mwh"
        ]



    # rename load

    if len(load.columns)==1:

        load.columns=[
            "load_mw"
        ]



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



    # remove duplicates

    df = df[
        ~df.index.duplicated()
    ]



    # remove empty columns

    df = df.dropna(
        axis=1,
        how="all"
    )



    # fill remaining missing

    df = df.ffill()

    df = df.bfill()



    print("\nFINAL DATASET")


    print(
        df.head()
    )


    print()

    print(
        "Shape:",
        df.shape
    )


    print()

    print(
        "Date:",
        df.index.min(),
        "->",
        df.index.max()
    )


    print()

    print(
        "Missing:"
    )

    print(
        df.isna().sum()
    )



    _, processed_path = get_paths(
        country
    )


    output = os.path.join(
        processed_path,
        f"{country}_clean.csv"
    )


    df.to_csv(
        output
    )


    print()

    print(
        "Saved:"
    )

    print(
        output
    )


    print()

    print("DONE")






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



    clean_dataset(
        args.country.lower()
    )