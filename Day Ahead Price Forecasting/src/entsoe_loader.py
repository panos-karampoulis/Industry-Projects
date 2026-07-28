from pathlib import Path
from datetime import datetime
import pandas as pd

from dotenv import load_dotenv
import os

from entsoe import EntsoePandasClient


load_dotenv()


API_KEY = os.getenv("ENTSOE_API_KEY")


class EntsoeLoader:

    def __init__(self):

        if API_KEY is None:
            raise ValueError(
                "Missing ENTSO-E API key"
            )

        self.client = EntsoePandasClient(
            api_key=API_KEY
        )


    def get_day_ahead_prices(
            self,
            country_code,
            start,
            end
    ):

        start = pd.Timestamp(start)

        end = pd.Timestamp(end)

        prices = self.client.query_day_ahead_prices(
            country_code,
            start=start,
            end=end
        )

        return prices

    def get_load(
            self,
            country_code,
            start,
            end
    ):

        start = pd.Timestamp(start)
        end = pd.Timestamp(end)

        load = self.client.query_load(
            country_code,
            start=start,
            end=end
        )

        return load

    def get_generation(
            self,
            country_code,
            start,
            end
    ):

        start = pd.Timestamp(start)
        end = pd.Timestamp(end)

        generation = self.client.query_generation(
            country_code,
            start=start,
            end=end
        )

        return generation