import os
import time
import pandas as pd

from pathlib import Path
from entsoe import EntsoePandasClient

import sys


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
    COUNTRIES,
    START_YEAR,
    END_DATE
)



# ==========================================================
# ENTSO-E LOADER
# ==========================================================


class EntsoeLoader:


    def __init__(self):


        self.client = EntsoePandasClient(
            api_key=ENTSOE_API_KEY
        )


        self.raw_dir = (
            BASE_DIR /
            "data" /
            "raw"
        )



    # ======================================================
    # DATE RANGE
    # ======================================================


    def get_date_range(self):


        start = pd.Timestamp(
            f"{START_YEAR}-01-01",
            tz="Europe/Brussels"
        )


        if END_DATE:


            end = pd.Timestamp(
                END_DATE,
                tz="Europe/Brussels"
            )


        else:


            end = pd.Timestamp.now(
                tz="Europe/Brussels"
            )


        return start, end



    # ======================================================
    # RETRY WRAPPER
    # ======================================================


    def retry_request(
        self,
        func,
        retries=5,
        delay=15
    ):


        for attempt in range(
            retries
        ):


            try:

                return func()



            except Exception as e:


                print(
                    f"Attempt {attempt+1}/{retries} failed"
                )


                print(
                    e
                )


                if attempt < retries - 1:


                    print(
                        f"Retrying in {delay} seconds..."
                    )


                    time.sleep(
                        delay
                    )


                else:


                    raise e



    # ======================================================
    # LOAD
    # ======================================================


    def get_load(
        self,
        country
    ):


        domain = (
            COUNTRIES[country]["domain"]
        )


        start, end = self.get_date_range()


        print(
            "Downloading load..."
        )



        df = self.retry_request(

            lambda:

            self.client.query_load(
                domain,
                start=start,
                end=end
            )

        )



        if isinstance(
            df,
            pd.Series
        ):


            df = df.to_frame(
                "load_mw"
            )



        return df



    # ======================================================
    # DAY AHEAD PRICE
    # ======================================================


    def get_prices(
        self,
        country
    ):


        domain = (
            COUNTRIES[country]["domain"]
        )


        start, end = self.get_date_range()


        print(
            "Downloading prices..."
        )



        df = self.retry_request(

            lambda:

            self.client.query_day_ahead_prices(
                domain,
                start=start,
                end=end
            )

        )


        df = df.to_frame(
            "day_ahead_price"
        )


        return df



    # ======================================================
    # GENERATION
    # ======================================================


    def get_generation(
        self,
        country
    ):


        domain = (
            COUNTRIES[country]["domain"]
        )


        start, end = self.get_date_range()


        print(
            "Downloading generation..."
        )



        df = self.retry_request(

            lambda:

            self.client.query_generation(
                domain,
                start=start,
                end=end
            )

        )


        return df



    # ======================================================
    # RENEWABLE EXTRACTION
    # ======================================================


    def extract_renewables(
        self,
        generation
    ):


        result = pd.DataFrame(
            index=generation.index
        )


        result["wind_generation"] = 0

        result["solar_generation"] = 0



        for col in generation.columns:


            name = str(
                col
            ).lower()



            if "wind" in name:


                result["wind_generation"] += (
                    generation[col]
                )



            if "solar" in name:


                result["solar_generation"] += (
                    generation[col]
                )



        result["renewable_generation"] = (
            result["wind_generation"]
            +
            result["solar_generation"]
        )



        return result



    # ======================================================
    # SAVE
    # ======================================================


    def save(
        self,
        df,
        country,
        filename
    ):


        folder = (
            self.raw_dir /
            country
        )


        folder.mkdir(
            parents=True,
            exist_ok=True
        )



        path = (
            folder /
            filename
        )


        df.to_csv(
            path
        )


        print(
            f"Saved: {path}"
        )



    # ======================================================
    # UPDATE COUNTRY
    # ======================================================


    def update_country(
        self,
        country
    ):


        print("\n")
        print("="*60)
        print(
            f"UPDATING {country.upper()}"
        )
        print("="*60)



        # -------------------------------
        # LOAD
        # -------------------------------


        try:

            load = self.get_load(
                country
            )


            self.save(
                load,
                country,
                "load_latest.csv"
            )


        except Exception as e:


            print(
                "LOAD FAILED:",
                e
            )



        # -------------------------------
        # PRICE
        # -------------------------------


        try:


            prices = self.get_prices(
                country
            )


            self.save(
                prices,
                country,
                "prices_latest.csv"
            )


        except Exception as e:


            print(
                "PRICE FAILED:",
                e
            )



        # -------------------------------
        # GENERATION
        # -------------------------------


        try:


            generation = self.get_generation(
                country
            )


            renewables = self.extract_renewables(
                generation
            )


            self.save(
                renewables,
                country,
                "renewables_latest.csv"
            )


        except Exception as e:


            print(
                "GENERATION FAILED:",
                e
            )



        print(
            "Country update completed"
        )



# ==========================================================
# MAIN
# ==========================================================


if __name__ == "__main__":



    loader = EntsoeLoader()



    for country in COUNTRIES.keys():


        loader.update_country(
            country
        )



    print("\n")
    print("="*60)
    print(
        "ALL COUNTRIES UPDATED"
    )
    print("="*60)