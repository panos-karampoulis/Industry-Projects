import pandas as pd
from pathlib import Path



# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(
    r"D:\Portfolio\Energy-Trading-Decision-Support-System"
)



# ============================================================
# PATHS
# ============================================================

INTRADAY_FORECAST_DIR = (
    BASE_DIR
    /
    "data"
    /
    "forecasts"
    /
    "intraday"
)


DAY_AHEAD_FORECAST_DIR = (
    BASE_DIR
    /
    "data"
    /
    "forecasts"
    /
    "day_ahead_long_term"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "results"
    /
    "trading_signals"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]



# ============================================================
# TRADING PARAMETERS
# ============================================================

BUY_THRESHOLD = -10

SELL_THRESHOLD = 10



# ============================================================
# LOAD FORECASTS
# ============================================================

def load_forecasts(country):


    intraday_file = (

        INTRADAY_FORECAST_DIR
        /
        f"{country}_intraday_forecast.csv"

    )


    day_ahead_file = (

        DAY_AHEAD_FORECAST_DIR
        /
        f"{country}_day_ahead_30d_forecast.csv"

    )


    print(
        "Loading:"
    )

    print(
        intraday_file
    )

    print(
        day_ahead_file
    )


    intraday = pd.read_csv(
        intraday_file
    )


    day_ahead = pd.read_csv(
        day_ahead_file
    )


    intraday["timestamp"] = pd.to_datetime(
        intraday["timestamp"],
        utc=True
    )


    day_ahead["timestamp"] = pd.to_datetime(
        day_ahead["timestamp"],
        utc=True
    )


    return (
        intraday,
        day_ahead
    )



# ============================================================
# SIGNAL GENERATION
# ============================================================

def generate_signal(spread):


    if spread <= BUY_THRESHOLD:

        return "BUY"


    elif spread >= SELL_THRESHOLD:

        return "SELL"


    else:

        return "HOLD"



# ============================================================
# CONFIDENCE SCORE
# ============================================================

def calculate_confidence(spread):


    confidence = min(
        abs(spread) * 5,
        100
    )


    return round(
        confidence,
        2
    )



# ============================================================
# COUNTRY ENGINE
# ============================================================

def run_country_engine(country):


    print("\n")
    print("=" * 60)
    print(country.upper())
    print("=" * 60)



    intraday, day_ahead = load_forecasts(
        country
    )



    # --------------------------------------------------------
    # MERGE FORECASTS
    # --------------------------------------------------------

    df = pd.merge_asof(

        intraday.sort_values(
            "timestamp"
        ),

        day_ahead.sort_values(
            "timestamp"
        ),

        on="timestamp",

        direction="nearest"

    )



    print("\nColumns after merge:")

    print(
        df.columns.tolist()
    )



    # --------------------------------------------------------
    # PRICE SPREAD
    # --------------------------------------------------------

    df["spread"] = (

        df["forecast_price"]

        -

        df["forecast_price_eur_mwh"]

    )



    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    df["signal"] = (

        df["spread"]

        .apply(
            generate_signal
        )

    )



    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    df["confidence"] = (

        df["spread"]

        .apply(
            calculate_confidence
        )

    )


    df["country"] = country



    # --------------------------------------------------------
    # SAVE OUTPUT
    # --------------------------------------------------------

    output_file = (

        OUTPUT_DIR
        /
        f"{country}_trading_signals.csv"

    )


    df.to_csv(

        output_file,

        index=False

    )



    print(
        "\nSaved:"
    )

    print(
        output_file
    )


    print(
        "\nLatest signals:"
    )


    print(

        df[

            [

                "timestamp",

                "spread",

                "signal",

                "confidence"

            ]

        ]

        .tail()

    )



# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    for country in COUNTRIES:


        run_country_engine(
            country
        )


    print("\n")
    print("=" * 60)
    print(
        "TRADING ENGINE COMPLETED"
    )
    print("=" * 60)