import os
import sys
import pandas as pd


from entsoe import EntsoePandasClient



# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


sys.path.append(
    BASE_DIR
)



# ==========================================================
# CONFIG
# ==========================================================

from config import (
    ENTSOE_API_KEY,
    COUNTRIES
)



# ==========================================================
# PATHS
# ==========================================================

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


BACKUP_DIR = os.path.join(
    PROCESSED_DIR,
    "backup"
)


os.makedirs(
    BACKUP_DIR,
    exist_ok=True
)



# ==========================================================
# CLIENT
# ==========================================================

client = EntsoePandasClient(
    api_key=ENTSOE_API_KEY
)



# ==========================================================
# UPDATE COUNTRY
# ==========================================================

def update_country(country):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    file_path = os.path.join(
        PROCESSED_DIR,
        f"{country}_day_ahead_prices.csv"
    )



    # ------------------------------------------------------
    # Existing data
    # ------------------------------------------------------

    if os.path.exists(file_path):


        df_old = pd.read_csv(
            file_path
        )


        df_old["timestamp"] = pd.to_datetime(
            df_old["timestamp"],
            utc=True
        )


        last_timestamp = (
            df_old["timestamp"].max()
        )


        print(
            "Last timestamp:",
            last_timestamp
        )


    else:


        df_old = pd.DataFrame()


        last_timestamp = None


        print(
            "No existing file"
        )



    # ------------------------------------------------------
    # Date range
    # ------------------------------------------------------

    if last_timestamp is None:


        start = pd.Timestamp(
            "2026-01-01",
            tz="UTC"
        )


    else:


        start = (
            last_timestamp
            +
            pd.Timedelta(
                hours=1
            )
        )



    end = (
        pd.Timestamp.now(
            tz="UTC"
        )
        -
        pd.Timedelta(
            hours=1
        )
    )



    if start >= end:


        print(
            "Already updated"
        )

        return



    print(
        "Downloading:"
    )


    print(
        start,
        "->",
        end
    )



    # ------------------------------------------------------
    # API
    # ------------------------------------------------------

    try:


        prices = client.query_day_ahead_prices(

            COUNTRIES[country]["domain"],

            start=start,

            end=end

        )



    except Exception as e:


        print(
            "API ERROR:"
        )

        print(
            repr(e)
        )

        return



    if prices.empty:


        print(
            "No data"
        )

        return



    # ------------------------------------------------------
    # Format
    # ------------------------------------------------------

    df_new = (

        prices

        .reset_index()

    )



    df_new.columns = [

        "timestamp",

        "price_eur_mwh"

    ]



    df_new["timestamp"] = pd.to_datetime(

        df_new["timestamp"],

        utc=True

    )



    df_new["country"] = country


    df_new["resolution"] = "PT15M"



    df_new = df_new[

        [

            "timestamp",

            "country",

            "price_eur_mwh",

            "resolution"

        ]

    ]



    # ------------------------------------------------------
    # Merge
    # ------------------------------------------------------

    if not df_old.empty:


        df = pd.concat(

            [

                df_old,

                df_new

            ],

            ignore_index=True

        )


    else:


        df = df_new



    df = (

        df

        .drop_duplicates(

            subset=[

                "timestamp"

            ],

            keep="last"

        )

        .sort_values(

            "timestamp"

        )

    )



    # ------------------------------------------------------
    # Backup
    # ------------------------------------------------------

    if not df_old.empty:


        df_old.to_csv(

            os.path.join(

                BACKUP_DIR,

                f"{country}_day_ahead_backup.csv"

            ),

            index=False

        )



    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    df.to_csv(

        file_path,

        index=False

    )


    print(
        "New rows:",
        len(df_new)
    )


    print(
        "Total rows:",
        len(df)
    )


    print(
        "Saved:",
        file_path
    )





# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:


        update_country(
            country
        )


    print("\n")
    print("="*60)

    print(
        "DAY AHEAD UPDATE COMPLETED"
    )

    print("="*60)