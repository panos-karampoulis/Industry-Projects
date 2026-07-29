import os
from datetime import datetime

from dotenv import load_dotenv


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env"
    )
)


# ============================================================
# DIRECTORIES
# ============================================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


RAW_DATA_DIR = os.path.join(
    DATA_DIR,
    "raw"
)


PROCESSED_DATA_DIR = os.path.join(
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


METADATA_DIR = os.path.join(
    DATA_DIR,
    "metadata"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)



# ============================================================
# DATA RANGE
# ============================================================

HISTORICAL_START_DATE = (
    "2020-01-01"
)


def get_current_date():

    return datetime.utcnow().strftime(
        "%Y-%m-%d"
    )



# ============================================================
# DATA SETTINGS
# ============================================================

DEFAULT_FREQUENCY = "15min"


AUTO_UPDATE = True



# ============================================================
# API
# ============================================================

ENTSOE_API_KEY = os.getenv(
    "ENTSOE_API_KEY"
)



# ============================================================
# CREATE DIRECTORIES
# ============================================================

DIRECTORIES = [

    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    FEATURES_DIR,
    FORECASTS_DIR,
    METADATA_DIR,
    MODEL_DIR

]


for directory in DIRECTORIES:

    os.makedirs(
        directory,
        exist_ok=True
    )