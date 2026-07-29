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
# API CLIENT
# ============================================================

API_KEY = os.getenv(
    "ENTSOE_API_KEY"
)


client = EntsoePandasClient(
    api_key=API_KEY
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

def get_generation_file(country):

    return (
        RAW_DIR
        /
        country
        /
        "generation.csv"
    )



def get_last_timestamp(country):


    file = get_generation_file(
        country
    )


    if not file.exists():

        return None



    df = pd.read_csv(

        file,

        usecols=[
            "index"
        ]

    )


    df["index"] = pd.to_datetime(

        df["index"],

        utc=True

    )


    return df["index"].max()





def flatten_columns(df):


    if isinstance(
        df.columns,
        pd.MultiIndex
    ):


        df.columns = [

            "_".join(col)

            for col in df.columns

        ]


    return df





# ============================================================
# UPDATE GENERATION
# ============================================================

def update_generation(country):


    print()

    print("=" * 70)

    print(
        f"UPDATING GENERATION: {country.upper()}"
    )

    print("=" * 70)



    config = COUNTRIES[country]


    domain = config["domain"]

    timezone = config["timezone"]



    file = get_generation_file(
        country
    )



    last_timestamp = get_last_timestamp(
        country
    )



    if last_timestamp is None:


        print(
            "No existing generation dataset found"
        )

        print(
            "Run historical downloader first"
        )

        return



    print(
        "Last timestamp (UTC):",
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
            "Requesting ENTSO-E data..."
        )



        new_data = client.query_generation(

            domain,

            start=start.tz_convert(timezone),

            end=end.tz_convert(timezone)

        )



        new_data = flatten_columns(
            new_data
        )



        new_data = new_data.reset_index()



        new_data["country"] = country



        print(

            "Downloaded new rows:",

            len(new_data)

        )



        if len(new_data) == 0:


            print(
                "Nothing to append"
            )

            return



        old_data = pd.read_csv(
            file
        )



        updated = pd.concat(

            [
                old_data,
                new_data
            ],

            ignore_index=True

        )



        updated["index"] = pd.to_datetime(

            updated["index"],

            utc=True

        )



        updated = updated.drop_duplicates(

            subset=[
                "index"
            ],

            keep="last"

        )



        updated = updated.sort_values(

            "index"

        )



        updated.to_csv(

            file,

            index=False

        )



        print()

        print(
            "Updated dataset saved:"
        )

        print(
            file
        )


        print(

            "New dataset size:",

            updated.shape

        )



    except Exception as e:


        print()

        print(
            "UPDATE FAILED"
        )

        print(
            e
        )





# ============================================================
# RUN ALL COUNTRIES
# ============================================================

def run_incremental_generation_update():


    for country, config in COUNTRIES.items():


        if config["enabled"]:


            update_generation(
                country
            )





# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    print(
        """
============================================================
GENERATION INCREMENTAL UPDATE
============================================================
"""
    )


    run_incremental_generation_update()