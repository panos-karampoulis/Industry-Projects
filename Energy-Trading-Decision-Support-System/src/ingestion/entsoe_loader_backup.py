import os
import time
import shutil
import pandas as pd

from pathlib import Path
from datetime import datetime
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
    # DATE HANDLING
    # ======================================================

    def get_full_start_date(self):

        return pd.Timestamp(
            f"{START_YEAR}-01-01",
            tz="UTC"
        )



    def get_end_date(self):

        if END_DATE:

            return pd.Timestamp(
                END_DATE,
                tz="UTC"
            )


        return pd.Timestamp.now(
            tz="UTC"
        )



    # ======================================================
    # EXISTING DATA CHECK
    # ======================================================


    def get_last_timestamp(
        self,
        file_path
    ):


        if not file_path.exists():

            return None


        try:

            df = pd.read_csv(
                file_path,
                index_col=0
            )


            df.index = pd.to_datetime(
                df.index,
                utc=True,
                errors="coerce"
            )


            last = df.index.max()


            return last


        except Exception:

            return None



    # ======================================================
    # BACKUP
    # ======================================================


    def backup_file(
        self,
        file_path
    ):


        if file_path.exists():

            backup = file_path.parent / (
                file_path.stem +
                "_backup.csv"
            )


            shutil.copy(
                file_path,
                backup
            )



    # ======================================================
    # SAVE UPDATE
    # ======================================================


    def update_csv(
        self,
        new_data,
        file_path,
        column_name
    ):


        if new_data is None:

            return


        if len(new_data) == 0:

            print(
                "No new data received"
            )

            return



        # convert index UTC

        new_data.index = pd.to_datetime(
            new_data.index,
            utc=True
        )


        new_data = new_data.sort_index()



        if file_path.exists():


            old = pd.read_csv(
                file_path,
                index_col=0
            )


            old.index = pd.to_datetime(
                old.index,
                utc=True,
                errors="coerce"
            )


            combined = pd.concat(
                [
                    old,
                    new_data
                ]
            )


            combined = combined[
                ~combined.index.duplicated(
                    keep="last"
                )
            ]


        else:


            combined = new_data



        combined = combined.sort_index()



        self.backup_file(
            file_path
        )


        combined.to_csv(
            file_path
        )


        print(
            "Saved:",
            file_path
        )


        print(
            "Rows:",
            len(combined)
        )


        print(
            "Latest:",
            combined.index.max()
        )



    # ======================================================
    # RETRY
    # ======================================================


    def retry_request(
        self,
        func,
        retries=3,
        delay=10
    ):


        for attempt in range(retries):

            try:

                return func()


            except Exception as e:


                print(
                    f"Attempt {attempt+1}/{retries} failed"
                )

                print(e)


                if attempt < retries-1:

                    time.sleep(delay)

                else:

                    return None




    # ======================================================
    # DOWNLOAD FUNCTIONS
    # ======================================================


    def get_query_range(
        self,
        file_path
    ):


        last = self.get_last_timestamp(
            file_path
        )


        if last:


            start = last + pd.Timedelta(
                minutes=15
            )


            print(
                "Existing data until:",
                last
            )


        else:


            start = self.get_full_start_date()


            print(
                "No existing data. Starting:",
                start
            )



        end = self.get_end_date()


        return start, end




    # ======================================================
    # LOAD
    # ======================================================


    def update_load(
        self,
        country
    ):


        folder = (
            self.raw_dir /
            country
        )


        folder.mkdir(
            exist_ok=True
        )


        file = (
            folder /
            "load.csv"
        )


        start,end = self.get_query_range(
            file
        )


        if start >= end:

            print(
                "Load already updated"
            )

            return



        domain = COUNTRIES[country]["domain"]


        print(
            f"{country.upper()} LOAD"
        )


        data = self.retry_request(

            lambda:

            self.client.query_load(
                domain,
                start=start,
                end=end
            )

        )


        if isinstance(
            data,
            pd.Series
        ):

            data = data.to_frame(
                "load_mw"
            )



        self.update_csv(
            data,
            file,
            "load_mw"
        )




    # ======================================================
    # DAY AHEAD PRICE
    # ======================================================


    def update_prices(
        self,
        country
    ):


        folder = (
            self.raw_dir /
            country
        )


        file = (
            folder /
            "day_ahead.csv"
        )


        start,end = self.get_query_range(
            file
        )


        if start >= end:

            print(
                "Prices already updated"
            )

            return



        domain = COUNTRIES[country]["domain"]


        print(
            f"{country.upper()} PRICES"
        )


        data = self.retry_request(

            lambda:

            self.client.query_day_ahead_prices(
                domain,
                start=start,
                end=end
            )

        )


        if data is not None:

            data = data.to_frame(
                "day_ahead_price"
            )


        self.update_csv(
            data,
            file,
            "day_ahead_price"
        )



    # ======================================================
    # GENERATION
    # ======================================================


    def update_generation(
        self,
        country
    ):


        folder = (
            self.raw_dir /
            country
        )


        file = (
            folder /
            "generation.csv"
        )


        start,end = self.get_query_range(
            file
        )


        if start >= end:

            print(
                "Generation already updated"
            )

            return



        domain = COUNTRIES[country]["domain"]


        print(
            f"{country.upper()} GENERATION"
        )


        data = self.retry_request(

            lambda:

            self.client.query_generation(
                domain,
                start=start,
                end=end
            )

        )


        if data is not None:

            data.columns = [
                str(c)
                for c in data.columns
            ]



        self.update_csv(
            data,
            file,
            "generation"
        )



    # ======================================================
    # COUNTRY UPDATE
    # ======================================================


    def update_country(
        self,
        country
    ):


        print("\n")
        print("="*60)
        print(country.upper())
        print("="*60)


        self.update_load(
            country
        )


        self.update_prices(
            country
        )


        self.update_generation(
            country
        )



# ==========================================================
# MAIN
# ==========================================================


def main():


    print("="*70)
    print(
        "ENTSO-E INCREMENTAL MARKET UPDATE"
    )
    print("="*70)



    loader = EntsoeLoader()



    for country in COUNTRIES:


        loader.update_country(
            country
        )



    print("\n")
    print("="*70)
    print(
        "ENTSO-E UPDATE COMPLETED"
    )
    print("="*70)




if __name__ == "__main__":

    main()