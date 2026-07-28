import os
from dotenv import load_dotenv


load_dotenv()


ENTSOE_API_KEY = os.getenv(
    "ENTSOE_API_KEY"
)


# ==========================================================
# DATE CONFIG
# ==========================================================

START_YEAR = 2020
END_YEAR = 2026

END_DATE = "2026-07-24"


# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = {


    "germany": {

        "domain": "10Y1001A1001A82H"

    },


    "netherlands": {

        "domain": "10YNL----------L"

    },


    "france": {

        "domain": "10YFR-RTE------C"

    },


    "spain": {

        "domain": "10YES-REE------0"

    },


    "italy": {

        # Italy North bidding zone
        "domain": "10Y1001A1001A70O"

    }

}