import os
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(
    BASE_DIR / ".env"
)

from src.config.countries import COUNTRIES


# ============================================================
# API KEY
# ============================================================

API_KEY = os.getenv(
    "ENTSOE_API_KEY"
)


client = EntsoePandasClient(
    api_key=API_KEY
)



# ============================================================
# PATHS
# ============================================================

RAW_DIR = (

    BASE_DIR

    /

    "data"

    /

    "raw"

)



# ============================================================
# GENERATION TYPES
# ============================================================

GENERATION_TYPES = {


    "wind_onshore": "B19",


    "wind_offshore": "B18",


    "solar": "B16",


    "hydro_run_of_river": "B11",


    "hydro_reservoir": "B12"

}



# ============================================================
# DOWNLOAD FUNCTION
# ============================================================

def download_generation(
    country,
    start_year=2020,
    end_year=2026
):


    config = COUNTRIES[country]


    domain = config["domain"]


    timezone = config["timezone"]



    print()

    print("=" * 70)

    print(
        f"DOWNLOADING GENERATION: {country.upper()}"
    )

    print("=" * 70)



    country_dir = (

        RAW_DIR

        /

        country

    )


    country_dir.mkdir(
        parents=True,
        exist_ok=True
    )



    all_data = []



    for year in range(
        start_year,
        end_year + 1
    ):


        print(
            f"Generation {year}"
        )


        start = pd.Timestamp(
            f"{year}-01-01",
            tz=timezone
        )


        end = pd.Timestamp(
            f"{year+1}-01-01",
            tz=timezone
        )



        try:


            df = client.query_generation(

                domain,

                start=start,

                end=end

            )



            if isinstance(
                df.columns,
                pd.MultiIndex
            ):


                df.columns = [

                    "_".join(col)

                    for col in df.columns

                ]



            df = df.reset_index()



            df["country"] = country



            all_data.append(
                df
            )



            print(
                "Downloaded:",
                len(df)
            )



        except Exception as e:


            print(
                "FAILED YEAR:",
                year
            )

            print(
                e
            )



    if len(all_data) == 0:


        print(
            "NO DATA"
        )

        return



    final = pd.concat(
        all_data,
        ignore_index=True
    )



    output = (

        country_dir

        /

        "generation.csv"

    )



    final.to_csv(
        output,
        index=False
    )



    print()

    print(
        "Saved:",
        output
    )





# ============================================================
# RUN ALL COUNTRIES
# ============================================================

def run_generation_pipeline():


    for country, config in COUNTRIES.items():


        if config["enabled"]:


            download_generation(
                country
            )





if __name__ == "__main__":

    run_generation_pipeline()