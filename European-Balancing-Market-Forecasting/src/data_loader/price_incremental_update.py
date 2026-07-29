import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    BASE_DIR / ".env"
)


from src.config.countries import COUNTRIES



# ============================================================
# ENTSO-E CLIENT
# ============================================================

client = EntsoePandasClient(
    api_key=os.getenv(
        "ENTSOE_API_KEY"
    )
)



# ============================================================
# PATHS
# ============================================================

RAW_DIR = (

    BASE_DIR

    /

    "data"

    /

    "raw"

)



# ============================================================
# HELPERS
# ============================================================

def get_price_file(country):


    return (

        RAW_DIR

        /

        country

        /

        "day_ahead_prices.csv"

    )





def get_last_timestamp(country):


    file = get_price_file(
        country
    )


    if not file.exists():

        return None



    df = pd.read_csv(

        file,

        usecols=[
            "timestamp"
        ]

    )



    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df["timestamp"].max()





# ============================================================
# UPDATE PRICE
# ============================================================

def update_price(country):


    print()

    print("=" * 70)

    print(
        f"UPDATING DAY AHEAD PRICE: {country.upper()}"
    )

    print("=" * 70)



    config = COUNTRIES[country]


    domain = config["domain"]

    timezone = config["timezone"]



    file = get_price_file(
        country
    )



    last_timestamp = get_last_timestamp(
        country
    )



    if last_timestamp is None:


        print(
            "No existing price dataset found"
        )

        return



    print(
        "Last timestamp UTC:",
        last_timestamp
    )



    start = pd.to_datetime(

        last_timestamp,

        utc=True

    )



    end = pd.Timestamp.now(
        tz="UTC"
    )



    if end <= start:


        print(
            "No new data available"
        )

        return



    try:


        print(
            "Requesting ENTSO-E..."
        )



        prices = client.query_day_ahead_prices(

            domain,

            start=start.tz_convert(
                timezone
            ),

            end=end.tz_convert(
                timezone
            )

        )



        prices = prices.reset_index()



        prices.columns = [

            "timestamp",

            "price_eur_mwh"

        ]



        prices["country"] = country



        print(

            "Downloaded:",

            len(prices)

        )



        old = pd.read_csv(
            file
        )



        updated = pd.concat(

            [

                old,

                prices

            ],

            ignore_index=True

        )



        updated["timestamp"] = pd.to_datetime(

            updated["timestamp"],

            utc=True

        )



        updated = updated.drop_duplicates(

            subset=[

                "timestamp"

            ],

            keep="last"

        )



        updated = updated.sort_values(

            "timestamp"

        )



        updated.to_csv(

            file,

            index=False

        )



        print()

        print(
            "Saved:"
        )

        print(
            file
        )


        print(

            "Shape:",

            updated.shape

        )



    except Exception as e:


        print()

        print(
            "PRICE UPDATE FAILED"
        )

        print(
            e
        )





# ============================================================
# RUN ALL COUNTRIES
# ============================================================

def run_price_update():


    for country, config in COUNTRIES.items():


        if config["enabled"]:


            update_price(
                country
            )





# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    print(
        """
============================================================
PRICE INCREMENTAL UPDATE
============================================================
"""
    )


    run_price_update()