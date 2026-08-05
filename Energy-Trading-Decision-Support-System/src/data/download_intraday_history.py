import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)





import requests
import os
from pathlib import Path

from config import (
    COUNTRIES,
    START_YEAR,
    END_YEAR,
    ENTSOE_API_KEY
)


# ==========================================================
# API CONFIG
# ==========================================================

BASE_URL = "https://web-api.tp.entsoe.eu/api"


# ==========================================================
# OUTPUT
# ==========================================================

OUTPUT_DIR = Path(
    "data/raw/intraday_history"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# DOWNLOAD FUNCTION
# ==========================================================

def download_year(
    country,
    domain,
    year
):

    start = f"{year}01010000"

    if year == 2026:

        end = "202607240000"

    else:

        end = f"{year+1}01010000"


    params = {

        "securityToken": ENTSOE_API_KEY,

        "documentType": "A44",

        "businessType": "A62",

        "contract_MarketAgreement.type": "A01",

        "out_Domain": domain,

        "in_Domain": domain,

        "periodStart": start,

        "periodEnd": end

    }


    print(
        f"Downloading {country.upper()} {year}..."
    )


    response = requests.get(
        BASE_URL,
        params=params
    )


    if response.status_code != 200:

        print(
            "FAILED",
            response.status_code
        )

        print(
            response.text[:500]
        )

        return


    country_dir = (
        OUTPUT_DIR
        /
        country
    )


    country_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    filename = (
        country_dir
        /
        f"{country}_intraday_{year}.xml"
    )


    with open(
        filename,
        "wb"
    ) as file:

        file.write(
            response.content
        )


    print(
        "Saved:",
        filename
    )



# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country, config in COUNTRIES.items():


        print()
        print("=" * 70)
        print(country.upper())
        print("=" * 70)


        domain = config["domain"]


        for year in range(
            START_YEAR,
            END_YEAR + 1
        ):


            download_year(
                country,
                domain,
                year
            )


print()
print("=" * 70)
print("INTRADAY DOWNLOAD COMPLETED")
print("=" * 70)