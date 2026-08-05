import pandas as pd
import numpy as np
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

SIGNALS_DIR = (
    BASE_DIR
    /
    "data"
    /
    "results"
    /
    "trading_signals"
)


ACTUAL_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "results"
    /
    "backtesting"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# PARAMETERS
# ============================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]


# 15 min intervals
# 4 = 1 hour holding

HOLDING_PERIOD = 4


TRANSACTION_COST = 0.5



# ============================================================
# LOAD SIGNALS
# ============================================================

def load_signals(country):


    file = (

        SIGNALS_DIR
        /
        f"{country}_trading_signals.csv"

    )


    df = pd.read_csv(
        file
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    return df.sort_values(
        "timestamp"
    )




# ============================================================
# LOAD ACTUAL MARKET PRICE
# ============================================================

def load_actual_prices(country):


    file = (

        ACTUAL_DIR
        /
        f"{country}_intraday_prices.csv"

    )


    df = pd.read_csv(
        file
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.sort_values(
        "timestamp"
    )


    return df




# ============================================================
# BACKTEST
# ============================================================

def run_backtest(country):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    signals = load_signals(
        country
    )


    actual = load_actual_prices(
        country
    )



    # Keep only required columns

    actual = actual[

        [
            "timestamp",
            "price_eur_mwh"

        ]

    ]



    df = pd.merge_asof(

        signals.sort_values(
            "timestamp"
        ),

        actual.sort_values(
            "timestamp"
        ),

        on="timestamp",

        direction="nearest"

    )



    trades = []



    for i,row in df.iterrows():


        signal = row["signal"]


        if signal not in [

            "BUY",
            "SELL"

        ]:

            continue



        entry_time = row["timestamp"]


        entry_price = row["price_eur_mwh"]



        exit_index = (

            i
            +
            HOLDING_PERIOD

        )



        if exit_index >= len(df):

            continue



        exit_row = df.iloc[
            exit_index
        ]



        exit_time = (
            exit_row["timestamp"]
        )


        exit_price = (
            exit_row["price_eur_mwh"]
        )



        if signal == "BUY":

            position = 1


            pnl = (

                exit_price
                -
                entry_price

            )


        else:

            position = -1


            pnl = (

                entry_price
                -
                exit_price

            )



        pnl -= TRANSACTION_COST



        trades.append(

            {

            "country":
                country,

            "entry_time":
                entry_time,

            "exit_time":
                exit_time,

            "signal":
                signal,

            "entry_price":
                entry_price,

            "exit_price":
                exit_price,

            "position":
                position,

            "pnl":
                pnl

            }

        )




    trades_df = pd.DataFrame(
        trades
    )



    if trades_df.empty:

        print(
            "No trades"
        )

        return None




    trades_df["cum_pnl"] = (

        trades_df["pnl"]
        .cumsum()

    )



    # ========================================================
    # METRICS
    # ========================================================


    trades_count = len(
        trades_df
    )


    wins = (

        trades_df["pnl"] > 0

    ).sum()



    win_rate = (

        wins
        /
        trades_count
        *
        100

    )



    total_pnl = (

        trades_df["pnl"]
        .sum()

    )



    average_trade = (

        trades_df["pnl"]
        .mean()

    )



    returns = trades_df["pnl"]



    if returns.std() != 0:


        sharpe = (

            returns.mean()
            /
            returns.std()

        ) * np.sqrt(252)


    else:

        sharpe = 0



    running_max = (

        trades_df["cum_pnl"]
        .cummax()

    )


    drawdown = (

        trades_df["cum_pnl"]
        -
        running_max

    )


    max_drawdown = drawdown.min()



    summary = pd.DataFrame(

        [

            {

            "country":
                country,

            "trades":
                trades_count,

            "win_rate":
                round(
                    win_rate,
                    2
                ),

            "total_pnl":
                round(
                    total_pnl,
                    2
                ),

            "average_trade":
                round(
                    average_trade,
                    2
                ),

            "sharpe":
                round(
                    sharpe,
                    3
                ),

            "max_drawdown":
                round(
                    max_drawdown,
                    2
                )

            }

        ]

    )



    trade_file = (

        OUTPUT_DIR
        /
        f"{country}_strategy_backtest.csv"

    )


    trades_df.to_csv(

        trade_file,

        index=False

    )


    print(
        "Saved:",
        trade_file
    )


    print(
        summary
    )


    return summary




# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    results = []


    for country in COUNTRIES:


        result = run_backtest(
            country
        )


        if result is not None:

            results.append(
                result
            )



    if results:


        portfolio = pd.concat(
            results
        )


        portfolio.to_csv(

            OUTPUT_DIR
            /
            "portfolio_backtest_summary.csv",

            index=False

        )



        print("\n")
        print("="*60)
        print(
            "PORTFOLIO BACKTEST COMPLETED"
        )
        print("="*60)

        print(
            portfolio
        )