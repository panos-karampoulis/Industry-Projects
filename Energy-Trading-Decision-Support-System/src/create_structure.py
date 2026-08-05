import os

from config import (
    RAW_DIR,
    PROCESSED_DIR,
    COUNTRIES
)



def create_folders():

    for country in COUNTRIES:

        raw_country = os.path.join(
            RAW_DIR,
            country
        )

        processed_country = os.path.join(
            PROCESSED_DIR,
            country
        )


        os.makedirs(
            raw_country,
            exist_ok=True
        )

        os.makedirs(
            processed_country,
            exist_ok=True
        )


        print(
            f"Created structure for {country}"
        )



if __name__ == "__main__":

    create_folders()