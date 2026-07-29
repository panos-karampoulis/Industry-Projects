import pandas as pd
import requests
import xml.etree.ElementTree as ET


from entsoe import EntsoePandasClient


from src.config.settings import ENTSOE_API_KEY

from src.config.countries import COUNTRIES




class EntsoeClient:
    """
    Generic ENTSO-E API Client

    Load:
        entsoe-py

    Day Ahead Prices:
        Raw ENTSO-E API
    """



    BASE_URL = "https://web-api.tp.entsoe.eu/api"



    def __init__(self):

        if ENTSOE_API_KEY is None:

            raise ValueError(
                "Missing ENTSO-E API key"
            )


        self.client = EntsoePandasClient(
            api_key=ENTSOE_API_KEY
        )



    # =====================================================
    # COUNTRY CONFIGURATION
    # =====================================================


    def get_country_config(
            self,
            country
    ):


        if country not in COUNTRIES:

            raise ValueError(
                f"Country {country} not configured"
            )


        return COUNTRIES[country]




    # =====================================================
    # DATE HANDLING
    # =====================================================


    def parse_dates(
            self,
            start,
            end,
            timezone
    ):


        start = pd.Timestamp(
            start,
            tz=timezone
        )


        end = pd.Timestamp(
            end,
            tz=timezone
        )


        return start, end





    # =====================================================
    # LOAD DATA
    # =====================================================


    def get_load_data(
            self,
            country,
            start,
            end
    ):


        config = self.get_country_config(
            country
        )


        start, end = self.parse_dates(
            start,
            end,
            config["timezone"]
        )



        data = self.client.query_load(

            country_code=config["country_code"],

            start=start,

            end=end

        )



        df = (

            data
            .reset_index()

        )



        df.columns = [

            "timestamp",

            "load_mw"

        ]



        df["country"] = country



        return df





    # =====================================================
    # DAY AHEAD PRICES
    # RAW ENTSO-E API
    # =====================================================


    def get_day_ahead_prices(
            self,
            country,
            start,
            end
    ):


        config = self.get_country_config(
            country
        )



        start, end = self.parse_dates(

            start,

            end,

            config["timezone"]

        )



        # ENTSO-E format

        period_start = (

            start
            .tz_convert("UTC")
            .strftime("%Y%m%d%H%M")

        )


        period_end = (

            end
            .tz_convert("UTC")
            .strftime("%Y%m%d%H%M")

        )



        domain = config["domain"]



        params = {


            "securityToken": ENTSOE_API_KEY,


            # Day Ahead Prices

            "documentType": "A44",


            "in_Domain": domain,


            "out_Domain": domain,


            "periodStart": period_start,


            "periodEnd": period_end

        }



        response = requests.get(

            self.BASE_URL,

            params=params,

            timeout=60

        )



        if response.status_code != 200:


            raise Exception(

                f"ENTSO-E API ERROR {response.status_code}: {response.text[:300]}"

            )



        xml_root = ET.fromstring(

            response.content

        )



        namespace = {

            "ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"

        }



        rows = []



        for period in xml_root.findall(

            ".//ns:TimeSeries",

            namespace

        ):



            for point in period.findall(

                ".//ns:Point",

                namespace

            ):



                position = point.find(

                    "ns:position",

                    namespace

                )


                price = point.find(

                    "ns:price.amount",

                    namespace

                )



                if price is not None:


                    rows.append(

                        {

                            "position": int(position.text),

                            "price_eur_mwh": float(price.text)

                        }

                    )



        if not rows:


            raise ValueError(

                f"No price data returned for {country}"

            )



        df = pd.DataFrame(rows)



        # Hourly index reconstruction

        timestamps = pd.date_range(

            start=start,

            periods=len(df),

            freq="1h",

            tz=config["timezone"]

        )



        df["timestamp"] = timestamps



        df = df[

            [

                "timestamp",

                "price_eur_mwh"

            ]

        ]



        df["country"] = country


        # =====================================================
        # SAFETY DATE FILTER
        # =====================================================

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )


        start_check = pd.Timestamp(
            start
        ).tz_convert(
            config["timezone"]
        )


        end_check = pd.Timestamp(
            end
        ).tz_convert(
            config["timezone"]
        )



        df = df[

            (df["timestamp"] >= start_check)

            &

            (df["timestamp"] <= end_check)

        ]



        df = (
            df
            .reset_index(
                drop=True
            )
        )



        return df