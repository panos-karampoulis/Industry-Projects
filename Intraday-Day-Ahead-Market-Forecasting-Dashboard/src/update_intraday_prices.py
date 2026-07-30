import os
import sys
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone, timedelta


# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
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

PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


BACKUP_DIR = (
    PROCESSED_DIR
    /
    "backup"
)


BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ==========================================================
# ENTSO-E API
# ==========================================================

BASE_URL = (
    "https://web-api.tp.entsoe.eu/api"
)



# ==========================================================
# DOWNLOAD WINDOW
# ==========================================================

WINDOW_DAYS = 3



# ==========================================================
# FETCH FUNCTION
# ==========================================================

def fetch_intraday(
        country,
        domain,
        start,
        end
):


    params = {


        "securityToken":
            ENTSOE_API_KEY,


        "documentType":
            "A44",


        "businessType":
            "A62",


        "contract_MarketAgreement.type":
            "A01",


        "out_Domain":
            domain,


        "in_Domain":
            domain,


        "periodStart":
            start.strftime(
                "%Y%m%d%H%M"
            ),


        "periodEnd":
            end.strftime(
                "%Y%m%d%H%M"
            )

    }



    try:


        response = requests.get(

            BASE_URL,

            params=params,

            timeout=60

        )


        if response.status_code != 200:

            print(
                "HTTP ERROR:",
                response.status_code
            )

            return None



        return response.content



    except Exception as e:


        print(
            "Request failed:",
            repr(e)
        )


        return None




# ==========================================================
# XML PARSER
# ==========================================================

import xml.etree.ElementTree as ET


NS = {

"ns0":
"urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"

}



def parse_xml(
        content,
        country
):


    rows = []


    try:

        root = ET.fromstring(
            content
        )


    except Exception:


        return pd.DataFrame()



    for ts in root.findall(
        ".//ns0:TimeSeries",
        NS
    ):


        period = ts.find(
            ".//ns0:Period",
            NS
        )


        if period is None:
            continue



        start_node = period.find(
            ".//ns0:start",
            NS
        )


        resolution_node = period.find(
            ".//ns0:resolution",
            NS
        )



        if (
            start_node is None
            or
            resolution_node is None
        ):
            continue



        start_time = pd.to_datetime(
            start_node.text,
            utc=True
        )


        resolution = (
            resolution_node.text
        )


        if resolution == "PT15M":

            minutes = 15

        elif resolution == "PT30M":

            minutes = 30

        else:

            minutes = 60



        for point in period.findall(
            ".//ns0:Point",
            NS
        ):


            position = int(

                point.find(
                    "ns0:position",
                    NS
                ).text

            )


            price = float(

                point.find(
                    "ns0:price.amount",
                    NS
                ).text

            )


            timestamp = (

                start_time

                +

                pd.Timedelta(

                    minutes
                    *
                    (position-1),

                    unit="min"

                )

            )


            rows.append(

                {

                "timestamp":
                    timestamp,


                "country":
                    country,


                "price_eur_mwh":
                    price,


                "resolution":
                    resolution

                }

            )



    return pd.DataFrame(rows)





# ==========================================================
# UPDATE COUNTRY
# ==========================================================

def update_country(country):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    file_path = (

        PROCESSED_DIR
        /
        f"{country}_intraday_prices.csv"

    )



    if not file_path.exists():

        print(
            "Missing file"
        )

        return



    old = pd.read_csv(
        file_path
    )


    old["timestamp"] = pd.to_datetime(
        old["timestamp"],
        utc=True
    )


    last_timestamp = (
        old["timestamp"].max()
    )


    print(
        "Last timestamp:",
        last_timestamp
    )



    # backup

    old.to_csv(

        BACKUP_DIR
        /
        f"{country}_backup.csv",

        index=False

    )



    # rolling window

    start = (

        datetime.now(
            timezone.utc
        )

        -

        timedelta(
            days=WINDOW_DAYS
        )

    )


    end = datetime.now(
        timezone.utc
    )



    print(
        "Downloading:",
        start,
        "->",
        end
    )



    xml = fetch_intraday(

        country,

        COUNTRIES[country]["domain"],

        start,

        end

    )



    if xml is None:

        print(
            "No response"
        )

        return



    new = parse_xml(

        xml,

        country

    )



    if new.empty:

        print(
            "No new data"
        )

        return



    new = new[
        new["timestamp"] > last_timestamp
    ]



    if new.empty:

        print(
            "No timestamps after last"
        )

        return



    final = pd.concat(

        [

            old,

            new

        ],

        ignore_index=True

    )



    final = final.drop_duplicates(

        subset=[
            "timestamp"
        ],

        keep="last"

    )


    final = final.sort_values(
        "timestamp"
    )



    final.to_csv(

        file_path,

        index=False

    )



    print(
        "New rows:",
        len(new)
    )


    print(
        "Total rows:",
        len(final)
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


    print()
    print("="*60)
    print(
        "INTRADAY UPDATE COMPLETED"
    )
    print("="*60)