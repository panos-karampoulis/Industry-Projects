import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(
    r"D:\Portfolio\Energy-Trading-Decision-Support-System"
)


# ============================================================
# PARAMETERS
# ============================================================

IMBALANCE_THRESHOLD = 5   # €/MWh



# ============================================================
# CALCULATE IMBALANCE
# ============================================================


def calculate_imbalance(
        day_ahead_price,
        actual_price
):


    deviation = (
        actual_price
        -
        day_ahead_price
    )


    if deviation > IMBALANCE_THRESHOLD:

        direction = "LONG_IMBALANCE"


    elif deviation < -IMBALANCE_THRESHOLD:

        direction = "SHORT_IMBALANCE"


    else:

        direction = "BALANCED"



    return {

        "price_deviation":
            deviation,

        "direction":
            direction

    }



# ============================================================
# APPLY TO DATAFRAME
# ============================================================


def add_imbalance_features(df):


    df["price_deviation"] = (

        df["actual_price"]
        -
        df["day_ahead_price"]

    )


    df["imbalance_direction"] = (

        df["price_deviation"]
        .apply(
            lambda x:

            "LONG_IMBALANCE"
            if x > IMBALANCE_THRESHOLD

            else

            "SHORT_IMBALANCE"
            if x < -IMBALANCE_THRESHOLD

            else

            "BALANCED"

        )

    )


    return df