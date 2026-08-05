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
    "backtesting_v2"
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


# test different holding periods
HOLDING_PERIODS = {

    "15min": 1,
    "30min": 2,
    "1h": 4,
    "2h": 8

}


TRANSACTION_COST = 0.5



# ============================================================
# LOAD DATA
# ============================================================

def load_data(country):


    signal_file = (

        SIGNALS_DIR
        /
        f"{country}_trading_signals.csv"

    )


    actual_file = (

        ACTUAL_DIR
        /
        f"{country}_intraday_prices.csv"

    )



    signals = pd.read_csv(
        signal_file
    )


    actual = pd.read_csv(
        actual_file
    )



    signals["timestamp"] = pd.to_datetime(
        signals["timestamp"],
        utc=True
    )


    actual["timestamp"] = pd.to_datetime(
        actual["timestamp"],
        utc=True
    )


    actual = actual[

        [
            "timestamp",
            "price_eur_mwh"
        ]

    ]



    return (

        signals.sort_values("timestamp"),

        actual.sort_values("timestamp")

    )





# ============================================================
# BACKTEST ENGINE
# ============================================================

def run_backtest(
        country,
        holding_name,
        holding_period
):


    print("\n")
    print("="*60)
    print(country.upper())
    print(
        holding_name
    )
    print("="*60)



    signals, actual = load_data(
        country
    )



    df = pd.merge_asof(

        signals,

        actual,

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
            holding_period

        )



        if exit_index >= len(df):

            continue



        exit_row = df.iloc[
            exit_index
        ]



        exit_time = exit_row["timestamp"]


        exit_price = exit_row["price_eur_mwh"]




        if signal == "BUY":


            gross_pnl = (

                exit_price
                -
                entry_price

            )


            position = 1



        else:


            gross_pnl = (

                entry_price
                -
                exit_price

            )


            position = -1




        net_pnl = (

            gross_pnl
            -
            TRANSACTION_COST

        )



        trades.append(

            {

            "country":
                country,


            "holding_period":
                holding_name,


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


            "gross_pnl":
                gross_pnl,


            "net_pnl":
                net_pnl

            }

        )





    trades_df = pd.DataFrame(
        trades
    )



    if trades_df.empty:

        return None




    trades_df["cum_pnl"] = (

        trades_df["net_pnl"]
        .cumsum()

    )



    # =============================
    # METRICS
    # =============================


    trades_count = len(
        trades_df
    )


    wins = (

        trades_df["net_pnl"] > 0

    ).sum()



    win_rate = (

        wins
        /
        trades_count

    ) * 100



    total_pnl = (

        trades_df["net_pnl"]
        .sum()

    )



    average_trade = (

        trades_df["net_pnl"]
        .mean()

    )



    gross_profit = (

        trades_df.loc[
            trades_df["net_pnl"] > 0,
            "net_pnl"
        ]
        .sum()

    )


    gross_loss = abs(

        trades_df.loc[
            trades_df["net_pnl"] < 0,
            "net_pnl"
        ]
        .sum()

    )



    if gross_loss != 0:

        profit_factor = (

            gross_profit
            /
            gross_loss

        )

    else:

        profit_factor = 0



    returns = trades_df["net_pnl"]



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




    summary = {


        "country":
            country,


        "holding_period":
            holding_name,


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


        "profit_factor":
            round(
                profit_factor,
                3
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




    filename = (

        OUTPUT_DIR
        /
        f"{country}_{holding_name}_trades.csv"

    )


    trades_df.to_csv(

        filename,

        index=False

    )



    print(
        "Saved:",
        filename
    )


    print(
        pd.DataFrame(
            [summary]
        )
    )



    return summary




# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":



    results = []



    for country in COUNTRIES:


        for name,period in HOLDING_PERIODS.items():


            result = run_backtest(

                country,

                name,

                period

            )


            if result:

                results.append(
                    result
                )




    summary = pd.DataFrame(
        results
    )



    summary.to_csv(

        OUTPUT_DIR
        /
        "portfolio_strategy_summary.csv",

        index=False

    )



    print("\n")
    print("="*60)
    print(
        "BACKTEST V2 COMPLETED"
    )
    print("="*60)


    print(
        summary
    )