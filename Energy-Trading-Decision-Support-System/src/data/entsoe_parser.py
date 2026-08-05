# ==========================================================
# ENTSO-E XML PARSER
# Energy Trading Decision Support System
# ==========================================================

import pandas as pd
import xml.etree.ElementTree as ET



# ==========================================================
# NAMESPACES
# ==========================================================

NAMESPACES = {

    "ns":
    "urn:iec62325.351:tc57wg16:451-6:generationload_document:3:0"

}



# ==========================================================
# GENERIC XML READER
# ==========================================================


def parse_xml(
    xml_content
):


    """
    Converts ENTSO-E XML response into raw dataframe.
    """



    root = ET.fromstring(
        xml_content
    )


    rows = []


    for period in root.findall(
        ".//ns:TimeSeries/ns:Period",
        NAMESPACES
    ):


        start = period.find(
            ".//ns:timeInterval/ns:start",
            NAMESPACES
        )


        if start is None:

            continue



        timestamp = pd.to_datetime(
            start.text,
            utc=True
        )



        for point in period.findall(
            ".//ns:Point",
            NAMESPACES
        ):


            position = point.find(
                "ns:position",
                NAMESPACES
            )


            quantity = point.find(
                "ns:quantity",
                NAMESPACES
            )


            if (
                position is None
                or
                quantity is None
            ):

                continue



            rows.append(

                {

                    "timestamp":
                        timestamp,

                    "position":
                        int(position.text),

                    "value":
                        float(quantity.text)

                }

            )



    return pd.DataFrame(
        rows
    )




# ==========================================================
# LOAD PARSER
# ==========================================================


def parse_load_xml(
    xml_content
):


    df = parse_xml(
        xml_content
    )


    if len(df) == 0:

        return df



    df = df.rename(

        columns={

            "value":
            "load_mw"

        }

    )



    return df




# ==========================================================
# PRICE PARSER
# ==========================================================


def parse_price_xml(
    xml_content
):


    df = parse_xml(
        xml_content
    )


    if len(df) == 0:

        return df



    df = df.rename(

        columns={

            "value":
            "day_ahead_price"

        }

    )



    return df




# ==========================================================
# GENERATION PARSER
# ==========================================================


def parse_generation_xml(
    xml_content
):


    df = parse_xml(
        xml_content
    )


    if len(df) == 0:

        return df



    df = df.rename(

        columns={

            "value":
            "generation_mw"

        }

    )



    return df