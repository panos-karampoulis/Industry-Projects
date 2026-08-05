# ==========================================================
# ENTSO-E API CLIENT
# Energy Trading Decision Support System
# ==========================================================

import requests
import pandas as pd

from pathlib import Path


from src.data.entsoe_queries import (
    build_load_query,
    build_price_query,
    build_generation_query
)


from src.data.entsoe_parser import (
    parse_load_xml,
    parse_price_xml,
    parse_generation_xml
)



# ==========================================================
# CONFIG
# ==========================================================

API_URL = (
    "https://web-api.tp.entsoe.eu/api"
)



# ==========================================================
# CLIENT
# ==========================================================


class EntsoeClient:


    def __init__(
        self,
        api_key
    ):


        self.api_key = api_key



    # ======================================================
    # REQUEST
    # ======================================================


    def _request(
        self,
        params
    ):


        response = requests.get(

            API_URL,

            params=params,

            timeout=60

        )



        if response.status_code != 200:

            print("\n===== ENTSO-E DEBUG =====")

            print(response.text)

            print("=========================\n")


            raise Exception(

                f"ENTSO-E API error "
                f"{response.status_code}"

            )



        return response.text




    # ======================================================
    # LOAD
    # ======================================================


    def query_load(
        self,
        domain,
        start,
        end
    ):


        params = build_load_query(

            token=self.api_key,

            domain=domain,

            start=start,

            end=end

        )



        xml = self._request(

            params

        )



        df = parse_load_xml(

            xml

        )


        return df




    # ======================================================
    # DAY AHEAD PRICE
    # ======================================================


    def query_prices(
        self,
        domain,
        start,
        end
    ):


        params = build_price_query(

            token=self.api_key,

            domain=domain,

            start=start,

            end=end

        )



        xml = self._request(

            params

        )



        df = parse_price_xml(

            xml

        )


        return df




    # ======================================================
    # GENERATION
    # ======================================================


    def query_generation(
        self,
        domain,
        start,
        end
    ):


        params = build_generation_query(

            token=self.api_key,

            domain=domain,

            start=start,

            end=end

        )



        xml = self._request(

            params

        )



        df = parse_generation_xml(

            xml

        )


        return df