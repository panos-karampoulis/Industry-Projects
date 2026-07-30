import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


RAW_DIR = (
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
    "processed"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# XML NAMESPACE
# ============================================================

NS = {
    "ns0":
    "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"
}



# ============================================================
# RESOLUTION HANDLER
# ============================================================

def resolution_minutes(resolution):

    if resolution == "PT15M":
        return 15

    elif resolution == "PT30M":
        return 30

    elif resolution == "PT60M":
        return 60

    else:
        raise ValueError(
            f"Unsupported resolution {resolution}"
        )



# ============================================================
# XML PARSER FUNCTION
# ============================================================

def parse_xml(
        xml_file,
        country
):


    print(
        f"Parsing {xml_file.name}"
    )


    tree = ET.parse(
        xml_file
    )

    root = tree.getroot()


    rows = []


    # υπάρχουν πολλές TimeSeries
    for timeseries in root.findall(
        ".//ns0:TimeSeries",
        NS
    ):


        period = timeseries.find(
            ".//ns0:Period",
            NS
        )


        if period is None:
            continue



        start_text = period.find(
            ".//ns0:start",
            NS
        ).text



        resolution_node = period.find(
            ".//ns0:resolution",
            NS
        )


        if resolution_node is None:
            continue


        resolution = resolution_node.text



        start_time = pd.to_datetime(
            start_text,
            utc=True
        )



        minutes = resolution_minutes(
            resolution
        )



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

                pd.to_timedelta(

                    (position - 1)
                    *
                    minutes,

                    unit="min"

                )

            )


            rows.append(

                {

                    "timestamp": timestamp,

                    "country": country,

                    "price_eur_mwh": price,

                    "resolution": resolution

                }

            )


    return pd.DataFrame(rows)




# ============================================================
# PROCESS ALL COUNTRIES
# ============================================================


countries = [

    "germany",

    "netherlands",

    "france",

    "spain",

    "italy"

]



all_countries = []



for country in countries:


    print("="*70)

    print(
        country.upper()
    )

    print("="*70)



    country_dir = (
        RAW_DIR
        /
        country
    )



    files = sorted(
        country_dir.glob(
            "*.xml"
        )
    )


    country_data = []



    for file in files:


        df = parse_xml(
            file,
            country
        )


        country_data.append(
            df
        )



    country_df = pd.concat(
        country_data,
        ignore_index=True
    )



    country_df = country_df.sort_values(
        "timestamp"
    )



    output_file = (

        OUTPUT_DIR

        /

        f"{country}_intraday_prices.csv"

    )



    country_df.to_csv(
        output_file,
        index=False
    )



    print(
        "Saved:",
        output_file
    )


    print(
        "Shape:",
        country_df.shape
    )


    print()


    all_countries.append(
        country_df
    )



# ============================================================
# CREATE EUROPE DATASET
# ============================================================


europe_df = pd.concat(
    all_countries,
    ignore_index=True
)


europe_df = europe_df.sort_values(
    [
        "country",
        "timestamp"
    ]
)



europe_file = (

    OUTPUT_DIR

    /

    "europe_intraday_prices.csv"

)



europe_df.to_csv(
    europe_file,
    index=False
)



print("="*70)

print(
    "EUROPE DATASET CREATED"
)

print("="*70)


print(
    europe_df.shape
)


print(
    europe_df.head()
)


print(
    "Saved:",
    europe_file
)