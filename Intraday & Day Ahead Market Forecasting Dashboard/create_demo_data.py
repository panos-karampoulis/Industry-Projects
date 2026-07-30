import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


# =========================
# MARKET DATA
# =========================

market_file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "europe_intraday_prices.csv"
)


market = pd.read_csv(
    market_file
)


market_demo = market.tail(20000)


market_demo.to_csv(
    BASE_DIR
    /
    "demo_data"
    /
    "market"
    /
    "europe_intraday_prices.csv",
    index=False
)


print(
    "Market demo created:",
    market_demo.shape
)



# =========================
# BACKTESTING
# =========================


files = [

    "intraday_backtest_results.csv",

    "day_ahead_backtest_results.csv"

]


for file in files:


    source = (

        BASE_DIR
        /
        "data"
        /
        "backtesting"
        /
        file

    )


    df = pd.read_csv(source)


    demo = df.tail(5000)


    demo.to_csv(

        BASE_DIR
        /
        "demo_data"
        /
        "backtesting"
        /
        file,

        index=False

    )


    print(
        file,
        demo.shape
    )