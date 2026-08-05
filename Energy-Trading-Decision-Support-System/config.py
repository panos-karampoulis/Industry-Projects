import os
from dotenv import load_dotenv


# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv()


ENTSOE_API_KEY = os.getenv(
    "ENTSOE_API_KEY"
)



# ==========================================================
# DATE CONFIG
# ==========================================================

START_YEAR = 2020


# None means:
# use latest available data from ENTSO-E

END_DATE = None



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



# ==========================================================
# PATHS
# ==========================================================


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)



DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)



RAW_DIR = os.path.join(
    DATA_DIR,
    "raw"
)



PROCESSED_DIR = os.path.join(
    DATA_DIR,
    "processed"
)



FEATURES_DIR = os.path.join(
    DATA_DIR,
    "features"
)



FORECASTS_DIR = os.path.join(
    DATA_DIR,
    "forecasts"
)



RESULTS_DIR = os.path.join(
    DATA_DIR,
    "results"
)