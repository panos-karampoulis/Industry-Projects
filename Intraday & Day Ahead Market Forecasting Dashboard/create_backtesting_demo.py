import pandas as pd
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


ROWS_PER_COUNTRY = 5000


# ============================================================
# INTRADAY
# ============================================================

SOURCE_INTRADAY = Path(
    "data/backtesting/intraday_backtest_results.csv"
)


OUTPUT_INTRADAY = Path(
    "demo_data/backtesting/intraday_backtest_results.csv"
)



print("\nLoading intraday backtesting dataset...")


df = pd.read_csv(
    SOURCE_INTRADAY
)


print(
    "Original countries:"
)

print(
    df["country"].unique()
)



demo = (

    df[
        df["country"].isin(COUNTRIES)
    ]

    .groupby("country")

    .head(ROWS_PER_COUNTRY)

)



print("\nIntraday demo distribution:")


print(
    demo.groupby("country").size()
)



OUTPUT_INTRADAY.parent.mkdir(
    parents=True,
    exist_ok=True
)



demo.to_csv(
    OUTPUT_INTRADAY,
    index=False
)



print(
    "\nCreated:"
)

print(
    OUTPUT_INTRADAY
)


print(
    demo.shape
)



# ============================================================
# DAY AHEAD
# ============================================================


SOURCE_DAY_AHEAD = Path(
    "data/backtesting/day_ahead_backtest_results.csv"
)


OUTPUT_DAY_AHEAD = Path(
    "demo_data/backtesting/day_ahead_backtest_results.csv"
)



print("\nLoading day ahead backtesting dataset...")


df = pd.read_csv(
    SOURCE_DAY_AHEAD
)



print(
    "Original countries:"
)

print(
    df["country"].unique()
)



demo = (

    df[
        df["country"].isin(COUNTRIES)
    ]

    .groupby("country")

    .head(ROWS_PER_COUNTRY)

)



print("\nDay Ahead demo distribution:")


print(
    demo.groupby("country").size()
)



demo.to_csv(
    OUTPUT_DAY_AHEAD,
    index=False
)



print(
    "\nCreated:"
)

print(
    OUTPUT_DAY_AHEAD
)


print(
    demo.shape
)


print(
    "\nDONE"
)