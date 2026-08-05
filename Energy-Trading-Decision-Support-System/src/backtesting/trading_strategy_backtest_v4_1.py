# ============================================================
# Energy Trading Decision Support System
# V4.1 - Realistic Intraday Arbitrage Backtester
#
# Strategy:
# Day Ahead vs Intraday Price Deviation
#
# Improvements vs V4:
# - No look-ahead bias
# - Lagged signals
# - Rolling volatility filter
# - Transaction costs
# - Position sizing
# ============================================================


import os
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_PATH = (
    r"D:\Portfolio\Energy-Trading-Decision-Support-System"
)


DAY_AHEAD_PATH = (
    BASE_PATH +
    r"\data\merged"
)


INTRADAY_PATH = (
    BASE_PATH +
    r"\data\market_prices\intraday"
)


RESULTS_PATH = (
    BASE_PATH +
    r"\data\results\backtesting_v4_1"
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


# Trading parameters

POSITION_SIZE_MWH = 10

TRANSACTION_COST = 0.15

SPREAD_THRESHOLD = 2

ROLLING_WINDOW = 96     # 24 hours * 4


os.makedirs(
    RESULTS_PATH,
    exist_ok=True
)



# ============================================================
# LOAD DAY AHEAD
# ============================================================


def load_day_ahead(country):

    path = (
        DAY_AHEAD_PATH
        + f"\\{country}\\day_ahead.csv"
    )


    df = pd.read_csv(path)


    df = df.rename(
        columns={
            "Unnamed: 0": "timestamp"
        }
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.rename(
        columns={
            "price_eur_mwh":
            "day_ahead_price"
        }
    )


    df = df[
        [
            "timestamp",
            "day_ahead_price"
        ]
    ]


    return df



# ============================================================
# LOAD INTRADAY
# ============================================================


def load_intraday(country):


    path = (
        INTRADAY_PATH
        + f"\\{country}_intraday_actual.csv"
    )


    df = pd.read_csv(path)


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.rename(
        columns={
            "intraday_price_eur_mwh":
            "intraday_price"
        }
    )


    df = df[
        [
            "timestamp",
            "intraday_price"
        ]
    ]


    return df



# ============================================================
# MERGE MARKETS
# ============================================================


def prepare_dataset(country):


    print(
        f"Loading {country}"
    )


    da = load_day_ahead(country)

    intra = load_intraday(country)



    # Sort

    da = da.sort_values(
        "timestamp"
    )

    intra = intra.sort_values(
        "timestamp"
    )



    # Align hourly DA with 15min intraday

    df = pd.merge_asof(
        intra,
        da,
        on="timestamp",
        direction="backward"
    )



    # Remove missing

    df = df.dropna()



    # --------------------------------------------------------
    # Spread calculation
    # --------------------------------------------------------

    df["spread"] = (
        df["intraday_price"]
        -
        df["day_ahead_price"]
    )


    # --------------------------------------------------------
    # NO LOOK AHEAD
    # --------------------------------------------------------

    df["spread_lag"] = (
        df["spread"]
        .shift(1)
    )


    df["spread_mean"] = (
        df["spread_lag"]
        .rolling(
            ROLLING_WINDOW
        )
        .mean()
    )


    df["spread_std"] = (
        df["spread_lag"]
        .rolling(
            ROLLING_WINDOW
        )
        .std()
    )


    df["z_score"] = (
        (
            df["spread_lag"]
            -
            df["spread_mean"]
        )
        /
        df["spread_std"]
    )



    df = df.dropna()



    return df

# ============================================================
# SIGNAL GENERATION
# ============================================================


def generate_signals(df):


    df = df.copy()



    # BUY:
    # Intraday cheaper than DA
    # Extreme negative deviation


    df["signal"] = 0



    df.loc[
        df["z_score"] < -SPREAD_THRESHOLD,
        "signal"
    ] = 1



    # SELL:
    # Intraday expensive vs DA


    df.loc[
        df["z_score"] > SPREAD_THRESHOLD,
        "signal"
    ] = -1



    return df



# ============================================================
# BACKTEST ENGINE
# ============================================================


def run_strategy(
        df,
        country,
        holding_period
):


    periods = HOLDING_PERIODS[
        holding_period
    ]


    trades = []



    for i in range(
        len(df) - periods
    ):


        row = df.iloc[i]


        signal = row["signal"]



        if signal == 0:
            continue



        entry_price = (
            df.iloc[i]["intraday_price"]
        )


        exit_price = (
            df.iloc[
                i + periods
            ]
            ["intraday_price"]
        )



        # BUY

        if signal == 1:

            pnl = (
                exit_price
                -
                entry_price
            )


        # SELL

        else:

            pnl = (
                entry_price
                -
                exit_price
            )



        # Position sizing

        pnl = (
            pnl
            *
            POSITION_SIZE_MWH
        )



        # Transaction cost

        pnl -= (
            TRANSACTION_COST
            *
            POSITION_SIZE_MWH
        )



        trades.append(
            {

                "timestamp":
                row["timestamp"],


                "signal":
                signal,


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


    return trades_df



# ============================================================
# PERFORMANCE METRICS
# ============================================================


def calculate_metrics(
        trades_df,
        country,
        holding_period
):


    if trades_df.empty:


        return {

            "country":
            country,

            "holding_period":
            holding_period,

            "trades":
            0,

            "win_rate":
            0,

            "total_pnl":
            0,

            "profit_factor":
            0,

            "sharpe":
            0,

            "max_drawdown":
            0

        }



    pnl = trades_df["pnl"]



    wins = pnl[
        pnl > 0
    ]

    losses = pnl[
        pnl < 0
    ]



    win_rate = (
        len(wins)
        /
        len(pnl)
    )



    profit_factor = (

        wins.sum()
        /
        abs(losses.sum())

        if losses.sum() != 0
        else np.inf

    )



    sharpe = (

        pnl.mean()
        /
        pnl.std()

        if pnl.std() != 0
        else 0

    )



    equity_curve = (
        pnl
        .cumsum()
    )



    drawdown = (
        equity_curve
        -
        equity_curve
        .cummax()
    )



    return {


        "country":
        country,


        "holding_period":
        holding_period,


        "trades":
        len(trades_df),


        "win_rate":
        round(
            win_rate,
            3
        ),


        "total_pnl":
        round(
            pnl.sum(),
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
            drawdown.min(),
            2
        )

    }



# ============================================================
# FULL BACKTEST RUNNER
# ============================================================


def run_backtest(country):


    print("\n")
    print("="*60)
    print(country.upper())
    print("="*60)



    df = prepare_dataset(
        country
    )


    df = generate_signals(
        df
    )



    results = []



    for hp in HOLDING_PERIODS:


        trades = run_strategy(
            df,
            country,
            hp
        )


        metrics = calculate_metrics(
            trades,
            country,
            hp
        )


        print(
            hp,
            metrics
        )


        results.append(
            metrics
        )


        if not trades.empty:


            file = (

                RESULTS_PATH
                +
                f"\\{country}_{hp}_trades.csv"

            )


            trades.to_csv(
                file,
                index=False
            )



    return results



# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":



    all_results = []



    # TEST FIRST COUNTRY ONLY

    for country in COUNTRIES:


        result = run_backtest(
            country
        )


        all_results.extend(
            result
        )



    summary = pd.DataFrame(
        all_results
    )



    summary.to_csv(
        RESULTS_PATH
        +
        "\\portfolio_summary.csv",
        index=False
    )



    print("\n")
    print("="*60)
    print("BACKTEST V4.1 COMPLETED")
    print("="*60)


    print(summary)