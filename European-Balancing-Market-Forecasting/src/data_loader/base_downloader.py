import os
import json

from datetime import datetime

import pandas as pd



from src.config.settings import (
    RAW_DATA_DIR,
    METADATA_DIR
)



# ============================================================
# BASE DOWNLOADER
# ============================================================


class BaseDownloader:



    def __init__(
            self,
            country,
            country_config
    ):


        self.country = country

        self.config = country_config

        self.timezone = (
            country_config["timezone"]
        )


        self.country_dir = os.path.join(

            RAW_DATA_DIR,

            country

        )


        os.makedirs(

            self.country_dir,

            exist_ok=True

        )



    # ========================================================
    # DATE HANDLING
    # ========================================================


    def localize_dates(
            self,
            start,
            end
    ):


        start = pd.Timestamp(
            start
        )


        end = pd.Timestamp(
            end
        )


        if start.tzinfo is None:


            start = start.tz_localize(

                self.timezone

            )


        if end.tzinfo is None:


            end = end.tz_localize(

                self.timezone

            )


        return start, end




    # ========================================================
    # FIND LAST TIMESTAMP
    # ========================================================


    def get_last_timestamp(
            self,
            filename
    ):


        path = os.path.join(

            self.country_dir,

            filename

        )


        if not os.path.exists(path):

            return None



        df = pd.read_csv(

            path,

            parse_dates=[
                "timestamp"
            ]

        )


        if len(df)==0:

            return None



        last_timestamp = (

            df["timestamp"]
            .max()

        )


        return pd.Timestamp(
            last_timestamp
        )




    # ========================================================
    # SAVE DATA
    # ========================================================


    def save_csv(
            self,
            df,
            filename
    ):


        path = os.path.join(

            self.country_dir,

            filename

        )


        df.to_csv(

            path,

            index=False

        )


        print(

            f"Saved: {path}"

        )


        return path




    # ========================================================
    # APPEND UPDATE
    # ========================================================


    def append_or_replace(
            self,
            new_df,
            filename
    ):


        path = os.path.join(

            self.country_dir,

            filename

        )


        if os.path.exists(path):


            old_df = pd.read_csv(

                path,

                parse_dates=[
                    "timestamp"
                ]

            )


            df = pd.concat(

                [
                    old_df,
                    new_df
                ],

                ignore_index=True

            )


        else:


            df = new_df



        df = (

            df

            .drop_duplicates(

                subset=[
                    "timestamp"
                ]

            )

            .sort_values(

                "timestamp"

            )

            .reset_index(
                drop=True
            )

        )


        df.to_csv(

            path,

            index=False

        )


        print(

            f"Updated: {path}"

        )



        return df




    # ========================================================
    # METADATA LOG
    # ========================================================


    def save_metadata(
            self,
            dataset,
            rows,
            filename
    ):


        metadata_file = os.path.join(

            METADATA_DIR,

            "data_quality.json"

        )



        if os.path.exists(
            metadata_file
        ):


            with open(
                metadata_file,
                "r",
                encoding="utf-8"
            ) as f:

                metadata = json.load(f)


        else:

            metadata = {}



        metadata_key = (

            f"{self.country}_{dataset}"

        )


        metadata[metadata_key] = {


            "country": self.country,


            "dataset": dataset,


            "file": filename,


            "rows": rows,


            "last_update":

                datetime.utcnow()
                .isoformat()


        }



        with open(

            metadata_file,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                metadata,

                f,

                indent=4

            )