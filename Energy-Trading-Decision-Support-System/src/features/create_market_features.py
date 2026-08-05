# ==========================================================
# MARKET FEATURE ENGINEERING
# Energy Trading Decision Support System
# ==========================================================


import pandas as pd
from pathlib import Path
import numpy as np
import sys



# ==========================================================
# PROJECT PATH
# ==========================================================


BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)



# ==========================================================
# DIRECTORIES
# ==========================================================


PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)



FEATURE_DIR = (
    BASE_DIR
    /
    "data"
    /
    "features"
)



FEATURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ==========================================================
# HELPERS
# ==========================================================


def load_csv(path):


    df = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True
    )


    df.index = pd.to_datetime(
        df.index,
        utc=True
    )


    df = df.sort_index()


    return df




# ==========================================================
# GENERATION AGGREGATION
# ==========================================================


def create_generation_features(df):


    result = pd.DataFrame(
        index=df.index
    )



    # ------------------------------
    # Renewable
    # ------------------------------


    renewable_cols = []


    for col in df.columns:


        name = col.lower()


        if any(
            x in name
            for x in [
                "solar",
                "wind",
                "hydro",
                "biomass",
                "renewable"
            ]
        ):

            renewable_cols.append(col)



    if renewable_cols:


        result["renewable_generation"] = (
            df[renewable_cols]
            .sum(axis=1)
        )


    else:

        result["renewable_generation"] = 0




    # ------------------------------
    # Solar
    # ------------------------------


    solar_cols = [
        c for c in df.columns
        if "solar" in c.lower()
    ]


    if solar_cols:

        result["solar_generation"] = (
            df[solar_cols]
            .sum(axis=1)
        )

    else:

        result["solar_generation"] = 0




    # ------------------------------
    # Wind
    # ------------------------------


    wind_cols = [
        c for c in df.columns
        if "wind" in c.lower()
    ]


    if wind_cols:

        result["wind_generation"] = (
            df[wind_cols]
            .sum(axis=1)
        )

    else:

        result["wind_generation"] = 0




    return result





# ==========================================================
# PRICE FEATURES
# ==========================================================


def create_price_features(df):


    price = df[
        "price_eur_mwh"
    ]



    result = pd.DataFrame(
        index=df.index
    )



    result["price_eur_mwh"] = price



    # lag features

    result["price_lag_1"] = (
        price.shift(1)
    )


    result["price_lag_4"] = (
        price.shift(4)
    )


    result["price_lag_96"] = (
        price.shift(96)
    )



    # price movement


    result["price_change"] = (
        price
        -
        price.shift(1)
    )



    # volatility


    result["rolling_mean_24h"] = (
        price
        .rolling(96)
        .mean()
    )


    result["rolling_std_24h"] = (
        price
        .rolling(96)
        .std()
    )


    result["volatility"] = (
        result["rolling_std_24h"]
        /
        result["rolling_mean_24h"]
    )




    # negative prices


    result["negative_price_flag"] = (
        price < 0
    ).astype(int)



    # spikes


    threshold = (
        price.mean()
        +
        2 * price.std()
    )


    result["price_spike_flag"] = (
        price > threshold
    ).astype(int)



    return result




# ==========================================================
# LOAD FEATURES
# ==========================================================


def create_load_features(df):


    load = df[
        "Actual Load"
    ]



    result = pd.DataFrame(
        index=df.index
    )



    result["load"] = load



    result["load_lag_1"] = (
        load.shift(1)
    )


    result["load_lag_96"] = (
        load.shift(96)
    )



    result["load_change"] = (
        load
        -
        load.shift(1)
    )



    peak = (
        load.mean()
        +
        load.std()
    )



    result["peak_load_flag"] = (
        load > peak
    ).astype(int)



    return result




# ==========================================================
# COUNTRY PIPELINE
# ==========================================================


def create_country_features(
        country
):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    price_file = (
        PROCESSED_DIR
        /
        f"{country}_prices_clean.csv"
    )


    load_file = (
        PROCESSED_DIR
        /
        f"{country}_load_clean.csv"
    )


    generation_file = (
        PROCESSED_DIR
        /
        f"{country}_generation_clean.csv"
    )



    features = []



    # prices

    if price_file.exists():

        price_df = load_csv(
            price_file
        )

        features.append(
            create_price_features(
                price_df
            )
        )



    # load

    if load_file.exists():

        load_df = load_csv(
            load_file
        )


        features.append(
            create_load_features(
                load_df
            )
        )



    # generation

    if generation_file.exists():

        gen_df = load_csv(
            generation_file
        )


        features.append(
            create_generation_features(
                gen_df
            )
        )




    final = pd.concat(
        features,
        axis=1
    )



    final = final.ffill().bfill()



    output = (
        FEATURE_DIR
        /
        f"{country}_market_features.csv"
    )



    final.to_csv(
        output
    )



    print(
        "Saved:",
        output
    )


    print(
        "Shape:",
        final.shape
    )



# ==========================================================
# MAIN
# ==========================================================


def main():


    countries = [

        "germany",
        "netherlands",
        "france",
        "spain",
        "italy"

    ]



    print("="*70)

    print(
        "ENERGY MARKET FEATURE ENGINEERING"
    )

    print("="*70)



    for country in countries:

        create_country_features(
            country
        )



    print("\n")

    print("="*70)

    print(
        "FEATURE ENGINEERING COMPLETED"
    )

    print("="*70)




if __name__ == "__main__":

    main()