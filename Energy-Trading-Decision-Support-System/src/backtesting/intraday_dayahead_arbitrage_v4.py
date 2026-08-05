import os
import numpy as np
import pandas as pd


# ============================================================
# CONFIG
# ============================================================

BASE_PATH = r"D:\Portfolio\Energy-Trading-Decision-Support-System"

DAY_AHEAD_PATH = os.path.join(
    BASE_PATH,
    "data",
    "merged",
    "{country}",
    "day_ahead.csv"
)

INTRADAY_PATH = os.path.join(
    BASE_PATH,
    "data",
    "market_prices",
    "intraday",
    "{country}_intraday_actual.csv"
)


RESULT_PATH = os.path.join(
    BASE_PATH,
    "data",
    "results",
    "backtesting_v4"
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


HOLDING_PERIODS = {

    "15min": 1,
    "30min": 2,
    "1h": 4,
    "2h": 8

}


THRESHOLD = 10        # €/MWh
TRANSACTION_COST = 0.5


os.makedirs(
    RESULT_PATH,
    exist_ok=True
)



# ============================================================
# LOAD DAY AHEAD
# ============================================================

def load_day_ahead(country):

    path = DAY_AHEAD_PATH.format(
        country=country
    )

    df = pd.read_csv(path)


    df.rename(
        columns={
            "Unnamed: 0": "timestamp",
            "price_eur_mwh": "day_ahead_price"
        },
        inplace=True
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df[
        [
            "timestamp",
            "day_ahead_price"
        ]
    ]


    df = df.sort_values(
        "timestamp"
    )


    # hourly -> 15 minutes

    df = (
        df
        .set_index("timestamp")
        .resample("15min")
        .ffill()
        .reset_index()
    )


    return df




# ============================================================
# LOAD INTRADAY
# ============================================================

def load_intraday(country):

    path = INTRADAY_PATH.format(
        country=country
    )


    df = pd.read_csv(path)


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df.rename(
        columns={
            "intraday_price_eur_mwh":
            "intraday_price"
        },
        inplace=True
    )


    df = df[
        [
            "timestamp",
            "intraday_price"
        ]
    ]


    df = df.sort_values(
        "timestamp"
    )


    return df




# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(country):

    da = load_day_ahead(country)

    idm = load_intraday(country)


    df = pd.merge(
        idm,
        da,
        on="timestamp",
        how="inner"
    )


    df["spread"] = (
        df["intraday_price"]
        -
        df["day_ahead_price"]
    )


    return df




# ============================================================
# SIGNAL GENERATION
# ============================================================

def generate_signal(row):


    spread = row["spread"]


    if spread > THRESHOLD:

        return -1       # SELL intraday


    elif spread < -THRESHOLD:

        return 1        # BUY intraday


    else:

        return 0




# ============================================================
# BACKTEST
# ============================================================

def run_backtest(
        df,
        country,
        holding_name,
        holding_steps
):


    df = df.copy()


    df["signal"] = (
        df.apply(
            generate_signal,
            axis=1
        )
    )


    trades = []


    for i in range(
        len(df)-holding_steps
    ):


        signal = df.iloc[i]["signal"]


        if signal == 0:
            continue



        entry_time = df.iloc[i]["timestamp"]


        entry_price = (
            df.iloc[i]
            ["intraday_price"]
        )


        exit_row = df.iloc[
            i + holding_steps
        ]


        exit_time = exit_row["timestamp"]


        exit_price = (
            exit_row
            ["intraday_price"]
        )



        if signal == 1:

            # BUY

            pnl = (
                exit_price
                -
                entry_price
            )


        else:

            # SELL

            pnl = (
                entry_price
                -
                exit_price
            )


        pnl -= TRANSACTION_COST



        trades.append(

            {

            "country":country,

            "holding_period":
            holding_name,

            "entry_time":
            entry_time,

            "exit_time":
            exit_time,

            "signal":
            "BUY"
            if signal == 1
            else "SELL",


            "entry_price":
            entry_price,


            "exit_price":
            exit_price,


            "pnl":
            pnl

            }

        )



    trades_df = pd.DataFrame(
        trades
    )



    if len(trades_df)==0:

        return {

            "trades":0,
            "win_rate":0,
            "total_pnl":0,
            "profit_factor":0,
            "sharpe":0,
            "max_drawdown":0

        }



    trades_df["cum_pnl"] = (
        trades_df["pnl"]
        .cumsum()
    )



    wins = trades_df[
        trades_df.pnl > 0
    ]


    losses = trades_df[
        trades_df.pnl < 0
    ]



    win_rate = (
        len(wins)
        /
        len(trades_df)
    )



    profit_factor = (

        wins.pnl.sum()
        /
        abs(losses.pnl.sum())

        if len(losses)>0
        else 0

    )



    sharpe = (

        trades_df.pnl.mean()
        /
        trades_df.pnl.std()

        if trades_df.pnl.std()!=0
        else 0

    )



    max_dd = (

        trades_df.cum_pnl
        -
        trades_df.cum_pnl
        .cummax()

    ).min()



    metrics = {


        "country":
        country,

        "holding_period":
        holding_name,


        "trades":
        len(trades_df),


        "win_rate":
        round(win_rate,3),


        "total_pnl":
        round(
            trades_df.pnl.sum(),
            2
        ),


        "profit_factor":
        round(
            profit_factor,
            2
        ),


        "sharpe":
        round(
            sharpe,
            2
        ),


        "max_drawdown":
        round(
            max_dd,
            2
        )

    }


    filename = (

        f"{country}_"
        f"{holding_name}_trades.csv"

    )


    trades_df.to_csv(

        os.path.join(
            RESULT_PATH,
            filename
        ),

        index=False

    )



    return metrics




# ============================================================
# MAIN
# ============================================================


all_results=[]



for country in COUNTRIES:


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)


    df = prepare_data(country)


    print(
        "Rows:",
        len(df)
    )



    for hp,steps in HOLDING_PERIODS.items():


        result = run_backtest(

            df,
            country,
            hp,
            steps

        )


        print(
            hp,
            result
        )


        all_results.append(
            result
        )



results_df = pd.DataFrame(
    all_results
)


results_df.to_csv(

    os.path.join(
        RESULT_PATH,
        "portfolio_backtest_summary.csv"
    ),

    index=False

)


print("\n")
print("="*60)
print("BACKTEST V4 COMPLETED")
print("="*60)


print(results_df)