import xml.etree.ElementTree as ET
import pandas as pd
from datetime import timedelta



class XMLPriceParser:


    """
    Parser for ENTSO-E Day Ahead Price XML files
    """



    def __init__(
            self,
            xml_content
    ):


        self.root = ET.fromstring(
            xml_content
        )



    # =====================================================
    # RESOLUTION PARSER
    # =====================================================

    def parse_resolution(
            self,
            resolution
    ):


        if resolution == "PT60M":

            return timedelta(
                hours=1
            )


        elif resolution == "PT30M":

            return timedelta(
                minutes=30
            )


        elif resolution == "PT15M":

            return timedelta(
                minutes=15
            )


        else:

            raise ValueError(
                f"Unsupported resolution {resolution}"
            )



    # =====================================================
    # MAIN PARSER
    # =====================================================

    def parse(self):


        rows = []


        namespaces = {

            "ns":
            "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"

        }



        for series in self.root.findall(
            ".//ns:TimeSeries",
            namespaces
        ):


            period = series.find(
                ".//ns:Period",
                namespaces
            )


            if period is None:

                continue



            start_node = period.find(
                ".//ns:start",
                namespaces
            )


            resolution_node = period.find(
                ".//ns:resolution",
                namespaces
            )


            if (
                start_node is None
                or resolution_node is None
            ):

                continue



            start_time = pd.Timestamp(
                start_node.text
            )


            frequency = self.parse_resolution(
                resolution_node.text
            )



            for point in period.findall(
                ".//ns:Point",
                namespaces
            ):


                position = int(

                    point.find(
                        "ns:position",
                        namespaces
                    ).text

                )


                price = float(

                    point.find(
                        "ns:price.amount",
                        namespaces
                    ).text

                )


                timestamp = (

                    start_time

                    +

                    (position - 1)
                    *
                    frequency

                )


                rows.append(

                    {

                        "timestamp":
                        timestamp,

                        "price_eur_mwh":
                        price

                    }

                )



        df = pd.DataFrame(
            rows
        )


        if not df.empty:


            df = (
                df
                .sort_values(
                    "timestamp"
                )
                .reset_index(
                    drop=True
                )
            )



        return df