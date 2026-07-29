import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


# ============================================================
# ENV
# ============================================================

load_dotenv(
    BASE_DIR / ".env"
)


from src.config.countries import COUNTRIES



# ============================================================
# CLIENT
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

def get_file(country):

    return (
        RAW_DIR
        /
        country
        /
        "load.csv"
    )



def get_last_timestamp(country):


    file = get_file(
        country
    )


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
# UPDATE
# ============================================================

def update_load(country):


    print()
    print("="*70)
    print(
        f"UPDATING LOAD: {country.upper()}"
    )
    print("="*70)



    config = COUNTRIES[country]


    domain = config["domain"]

    timezone = config["timezone"]



    file = get_file(
        country
    )


    last = get_last_timestamp(
        country
    )


    print(
        "Last timestamp UTC:",
        last
    )



    start = pd.to_datetime(
        last,
        utc=True
    )


    end = pd.Timestamp.now(
        tz="UTC"
    )


    if end <= start:

        print(
            "No new data"
        )

        return



    try:


        print(
            "Requesting ENTSO-E..."
        )


        new = client.query_load(

            domain,

            start=start.tz_convert(
                timezone
            ),

            end=end.tz_convert(
                timezone
            )

        )



        new = new.reset_index()



        new.columns = [
            "timestamp",
            "load_mw"
        ]



        new["country"] = country



        print(
            "Downloaded:",
            len(new)
        )



        old = pd.read_csv(
            file
        )



        updated = pd.concat(
            [
                old,
                new
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



        print(
            "Saved:",
            file
        )

        print(
            "Shape:",
            updated.shape
        )


    except Exception as e:

        print(
            "FAILED:"
        )

        print(e)




# ============================================================
# RUN ALL
# ============================================================

def run():

    for country, cfg in COUNTRIES.items():

        if cfg["enabled"]:

            update_load(
                country
            )



if __name__ == "__main__":

    print(
        """
============================================================
LOAD INCREMENTAL UPDATE
============================================================
"""
    )

    run()