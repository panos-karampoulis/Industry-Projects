import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(
    r"D:\Portfolio\Energy-Trading-Decision-Support-System"
)


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
    "market_prices"
    /
    "intraday"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "results"
    /
    "backtesting_v3_1"
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


HOLDING_PERIODS = {

    "15min":1,
    "30min":2,
    "1h":4,
    "2h":8

}


EXECUTION_DELAY = 1
# 15 minutes


TRANSACTION_COST = 0.5


MIN_MOVE = 1
# €/MWh



# ============================================================
# LOAD DATA
# ============================================================


def load_country_data(country):


    signals = pd.read_csv(

        SIGNALS_DIR
        /
        f"{country}_trading_signals.csv"

    )


    actual = pd.read_csv(

        ACTUAL_DIR
        /
        f"{country}_intraday_actual.csv"

    )



    signals["timestamp"] = pd.to_datetime(
        signals["timestamp"],
        utc=True
    )


    actual["timestamp"] = pd.to_datetime(
        actual["timestamp"],
        utc=True
    )



    if "country" in signals.columns:

        signals = signals.drop(
            columns=["country"]
        )


    if "country" in actual.columns:

        actual = actual.drop(
            columns=["country"]
        )


    return signals, actual





# ============================================================
# METRICS
# ============================================================


def calculate_metrics(trades):


    if len(trades)==0:

        return {

            "trades":0,
            "win_rate":0,
            "total_pnl":0,
            "average_trade":0,
            "sharpe":0,
            "max_drawdown":0

        }



    pnl = trades["pnl"]


    cumulative = pnl.cumsum()


    drawdown = (
        cumulative
        -
        cumulative.cummax()
    )



    sharpe = 0


    if pnl.std()!=0:

        sharpe = (
            pnl.mean()
            /
            pnl.std()
        ) * np.sqrt(252)



    return {


        "trades":len(trades),


        "win_rate":
            round(
                (pnl>0).mean()*100,
                2
            ),


        "total_pnl":
            round(
                pnl.sum(),
                2
            ),


        "average_trade":
            round(
                pnl.mean(),
                2
            ),


        "sharpe":
            round(
                sharpe,
                3
            ),


        "max_drawdown":
            round(
                drawdown.min(),
                2
            )

    }





# ============================================================
# BACKTEST
# ============================================================


def run_backtest(
        country,
        holding_name,
        holding_bars
):


    print("\n")
    print("="*60)
    print(country.upper())
    print(holding_name)
    print("="*60)



    signals, actual = load_country_data(
        country
    )



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



    trades=[]



    for i,row in df.iterrows():


        signal=row["signal"]



        if signal=="HOLD":

            continue



        entry_index = (
            i
            +
            EXECUTION_DELAY
        )



        exit_index = (

            entry_index
            +
            holding_bars

        )



        if exit_index >= len(df):

            continue



        entry_price = df.iloc[
            entry_index
        ][
            "intraday_price_eur_mwh"
        ]



        exit_price = df.iloc[
            exit_index
        ][
            "intraday_price_eur_mwh"
        ]



        move = (
            exit_price-entry_price
        )



        if abs(move)<MIN_MOVE:

            continue




        if signal=="BUY":

            pnl = move


        else:

            pnl = -move



        pnl -= TRANSACTION_COST




        trades.append({

            "country":country,

            "signal_time":
                row["timestamp"],

            "entry_time":
                df.iloc[entry_index]["timestamp"],

            "exit_time":
                df.iloc[exit_index]["timestamp"],

            "signal":
                signal,


            "entry_price":
                entry_price,


            "exit_price":
                exit_price,


            "price_move":
                move,


            "pnl":
                pnl

        })



    trades=pd.DataFrame(
        trades
    )



    metrics = calculate_metrics(
        trades
    )


    metrics["country"]=country

    metrics["holding_period"]=holding_name



    if len(trades)>0:

        trades.to_csv(

            OUTPUT_DIR
            /
            f"{country}_{holding_name}_trades.csv",

            index=False

        )



    print(metrics)



    return metrics





# ============================================================
# MAIN
# ============================================================


if __name__=="__main__":


    results=[]


    for country in COUNTRIES:


        for period,bars in HOLDING_PERIODS.items():


            result = run_backtest(

                country,

                period,

                bars

            )


            results.append(
                result
            )



    summary=pd.DataFrame(
        results
    )



    summary.to_csv(

        OUTPUT_DIR
        /
        "portfolio_backtest_v3_1_summary.csv",

        index=False

    )



    print("\n")
    print("="*60)
    print(
        "BACKTEST V3.1 COMPLETED"
    )
    print("="*60)


    print(summary)