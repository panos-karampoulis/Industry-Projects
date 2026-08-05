import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(
    r"D:\Portfolio\Energy-Trading-Decision-Support-System"
)


# ============================================================
# PATHS
# ============================================================

RAW_INTRADAY_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "intraday_history"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "market_prices"
    /
    "intraday"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# PARAMETERS
# ============================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]


XML_NAMESPACE = {
    "ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"
}



# ============================================================
# XML PARSER
# ============================================================

def parse_xml_file(
        xml_file,
        country
):


    print(
        "Reading:",
        xml_file.name
    )


    tree = ET.parse(
        xml_file
    )

    root = tree.getroot()



    records = []



    # --------------------------------------------------------
    # Find all TimeSeries periods
    # --------------------------------------------------------

    periods = root.findall(
        ".//ns:Period",
        XML_NAMESPACE
    )


    for period in periods:


        time_interval = period.find(
            "ns:timeInterval",
            XML_NAMESPACE
        )


        if time_interval is None:
            continue



        start = time_interval.find(
            "ns:start",
            XML_NAMESPACE
        )


        if start is None:
            continue



        start_time = pd.to_datetime(
            start.text,
            utc=True
        )



        resolution = period.find(
            "ns:resolution",
            XML_NAMESPACE
        )


        if resolution is None:
            continue



        # Only 15 minute data

        if resolution.text != "PT15M":

            continue



        points = period.findall(
            "ns:Point",
            XML_NAMESPACE
        )



        for point in points:


            position = point.find(
                "ns:position",
                XML_NAMESPACE
            )


            price = point.find(
                "ns:price.amount",
                XML_NAMESPACE
            )


            if (
                position is None
                or
                price is None
            ):
                continue



            timestamp = (
                start_time
                +
                timedelta(
                    minutes=
                    (
                        int(position.text)-1
                    )
                    *
                    15
                )
            )



            records.append(

                {

                    "timestamp": timestamp,

                    "country": country,

                    "intraday_price_eur_mwh":
                        float(price.text)

                }

            )



    return records




# ============================================================
# COUNTRY PROCESSOR
# ============================================================

def process_country(
        country
):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    country_dir = (

        RAW_INTRADAY_DIR
        /
        country

    )


    if not country_dir.exists():

        print(
            "Missing folder:",
            country_dir
        )

        return



    xml_files = sorted(

        country_dir.glob(
            "*.xml"
        )

    )



    if len(xml_files) == 0:

        print(
            "No XML files found"
        )

        return



    all_records = []



    for xml_file in xml_files:


        records = parse_xml_file(

            xml_file,

            country

        )


        all_records.extend(
            records
        )



    df = pd.DataFrame(
        all_records
    )



    if df.empty:

        print(
            "No data extracted"
        )

        return



    df = df.sort_values(
        "timestamp"
    )



    df = df.drop_duplicates(
        subset=[
            "timestamp"
        ]
    )



    output_file = (

        OUTPUT_DIR
        /
        f"{country}_intraday_actual.csv"

    )



    df.to_csv(

        output_file,

        index=False

    )



    print(
        "Saved:",
        output_file
    )


    print(
        "Rows:",
        len(df)
    )


    print(
        df.head()
    )


    print(
        df.tail()
    )




# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    for country in COUNTRIES:


        process_country(
            country
        )



    print("\n")
    print("="*60)
    print(
        "INTRADAY XML PARSING COMPLETED"
    )
    print("="*60)