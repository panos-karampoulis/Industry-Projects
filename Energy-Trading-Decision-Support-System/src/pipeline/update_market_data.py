import pandas as pd
from pathlib import Path
import sys


# ==========================================================
# PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


# ==========================================================
# IMPORTS
# ==========================================================

from entsoe import EntsoePandasClient

from config import (
    ENTSOE_API_KEY,
    COUNTRIES
)


# ==========================================================
# CLIENT
# ==========================================================

client = EntsoePandasClient(
    api_key=ENTSOE_API_KEY
)


RAW_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "latest"
)


RAW_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# HELPERS
# ==========================================================

def save_csv(
    df,
    filename
):

    path = RAW_DIR / filename


    df = df.copy()


    # ---------------------------------------
    # Convert index to timestamp column
    # ---------------------------------------

    if "timestamp" not in df.columns:

        df = df.reset_index()


    # rename possible index column

    if df.columns[0] != "timestamp":

        df = df.rename(
            columns={
                df.columns[0]: "timestamp"
            }
        )


    # datetime conversion

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.sort_values(
        "timestamp"
    )


    df.to_csv(
        path,
        index=False
    )


    print(
        "Saved",
        path
    )


def get_dates():

    end = pd.Timestamp.now(
        tz="UTC"
    )


    start = (
        end
        -
        pd.Timedelta(
            days=7
        )
    )


    return start, end



# ==========================================================
# LOAD
# ==========================================================

def update_load(country):


    print(
        country.upper(),
        "LOAD"
    )


    try:


        domain = COUNTRIES[country]["domain"]


        start,end = get_dates()


        df = client.query_load(

            domain,

            start=start,

            end=end

        )


        if isinstance(df, pd.Series):

            df = df.to_frame(
                "load_mw"
            )


        else:

            df = df.copy()



        df = df.reset_index()



        df = df.rename(
            columns={
                df.columns[0]: "timestamp"
            }
        )


        df = df.rename(
            columns={
                df.columns[1]: "load_mw"
            }
        )



        save_csv(

            df,

            f"{country}_load.csv"

        )



    except Exception as e:


        print(
            "Load update failed:",
            e
        )





# ==========================================================
# PRICES
# ==========================================================

def update_prices(country):


    print(
        country.upper(),
        "PRICES"
    )


    try:


        domain = COUNTRIES[country]["domain"]


        start,end = get_dates()



        df = client.query_day_ahead_prices(

            domain,

            start=start,

            end=end

        )



        if isinstance(df,pd.Series):

            df = df.to_frame(
                "price_eur_mwh"
            )



        save_csv(

            df,

            f"{country}_prices.csv"

        )



    except Exception as e:


        print(
            "Price update failed:",
            e
        )






# ==========================================================
# GENERATION
# ==========================================================

def update_generation(country):


    print(
        country.upper(),
        "GENERATION"
    )


    try:


        domain = COUNTRIES[country]["domain"]


        start,end = get_dates()



        df = client.query_generation(

            domain,

            start=start,

            end=end

        )


        save_csv(

            df,

            f"{country}_generation.csv"

        )


    except Exception as e:


        print(
            "Generation update failed:",
            e
        )





# ==========================================================
# MAIN
# ==========================================================

def main():


    print("="*70)

    print(
        "ENTSO-E MARKET DATA REFRESH"
    )

    print("="*70)



    for country in COUNTRIES:


        print("\n")
        print("="*70)
        print(country.upper())
        print("="*70)


        update_load(country)


        update_prices(country)


        update_generation(country)



    print("\n")
    print("="*70)

    print(
        "ENTSO-E UPDATE COMPLETED"
    )

    print("="*70)





if __name__=="__main__":

    main()