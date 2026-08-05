import pandas as pd
import numpy as np
import json

from pathlib import Path


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


RESULT_DIR = (
    BASE_DIR /
    "results"
)


RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


SIGNALS_FILE = (
    RESULT_DIR /
    "trading_decisions_all_countries.csv"
)


OUTPUT_FILE = (
    RESULT_DIR /
    "backtest_results.csv"
)


METRICS_FILE = (
    RESULT_DIR /
    "strategy_metrics.json"
)



# ==========================================================
# PARAMETERS
# ==========================================================

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]


INITIAL_CAPITAL = 100000


TRANSACTION_COST = 0.5
# €/MWh


MIN_HOLDING_PERIOD = 4
# hours



# ==========================================================
# LOAD DATA
# ==========================================================

def load_data():

    df = pd.read_csv(
        SIGNALS_FILE
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.sort_values(
        [
            "country",
            "timestamp"
        ]
    )


    return df



# ==========================================================
# SIGNAL MAPPING
# ==========================================================

def create_position(signal):


    if signal == "BUY":

        return 1


    elif signal == "SELL":

        return -1


    else:

        return 0



# ==========================================================
# HOLDING PERIOD CONTROL
# ==========================================================

def apply_holding_period(
    positions
):


    last_position = 0

    counter = 0


    final_positions = []



    for position in positions:


        if position != last_position:


            if counter < MIN_HOLDING_PERIOD:


                position = last_position


            else:

                last_position = position

                counter = 0



        counter += 1


        final_positions.append(
            position
        )


    return final_positions



# ==========================================================
# BACKTEST ENGINE
# ==========================================================

def run_backtest(df):


    results = []

    metrics = {}



    for country in COUNTRIES:


        print("\n")
        print("="*70)
        print(country.upper())
        print("="*70)



        data = df[

            df["country"]
            ==
            country

        ].copy()



        if data.empty:

            continue



        # --------------------------------------------------
        # POSITION
        # --------------------------------------------------

        data["position"] = (

            data["trading_signal"]
            .apply(
                create_position
            )

        )



        data["position"] = apply_holding_period(

            data["position"]
            .tolist()

        )



        # --------------------------------------------------
        # PRICE MOVEMENT
        # --------------------------------------------------

        data["price_change"] = (

            data["day_ahead_price"]
            -
            data["day_ahead_price"].shift(1)

        )



        data["price_change"] = (

            data["price_change"]
            .fillna(0)

        )



        # --------------------------------------------------
        # PNL
        # --------------------------------------------------

        data["hourly_pnl"] = (

            data["position"]
            *
            data["price_change"]

        )



        # --------------------------------------------------
        # TRANSACTION COST
        # --------------------------------------------------

        data["position_change"] = (

            data["position"]
            .diff()
            .abs()
            .fillna(0)

        )



        data["transaction_cost"] = (

            data["position_change"]
            *
            TRANSACTION_COST

        )



        data["hourly_pnl"] = (

            data["hourly_pnl"]
            -
            data["transaction_cost"]

        )



        # --------------------------------------------------
        # EQUITY CURVE
        # --------------------------------------------------

        data["cumulative_pnl"] = (

            data["hourly_pnl"]
            .cumsum()

        )


        data["equity_curve"] = (

            INITIAL_CAPITAL
            +
            data["cumulative_pnl"]

        )



        # --------------------------------------------------
        # DRAWDOWN
        # --------------------------------------------------

        running_max = (

            data["equity_curve"]
            .cummax()

        )


        data["drawdown"] = (

            data["equity_curve"]
            -
            running_max

        )



        max_drawdown = (

            data["drawdown"]
            .min()

        )



        # --------------------------------------------------
        # METRICS
        # --------------------------------------------------

        total_pnl = (

            data["hourly_pnl"]
            .sum()

        )



        volatility = (

            data["hourly_pnl"]
            .std()
            *
            np.sqrt(252)

        )



        if data["hourly_pnl"].std() != 0:


            sharpe = (

                data["hourly_pnl"]
                .mean()
                /
                data["hourly_pnl"]
                .std()

                *
                np.sqrt(252)

            )

        else:

            sharpe = 0



        trades = (

            data["position"]
            .diff()
            .abs()
            .sum()

        )



        winning_trades = (

            data["hourly_pnl"]
            >
            0

        ).sum()



        losing_trades = (

            data["hourly_pnl"]
            <
            0

        ).sum()



        total_trades = (

            winning_trades
            +
            losing_trades

        )



        if total_trades > 0:

            win_rate = (

                winning_trades
                /
                total_trades

            )

        else:

            win_rate = 0



        gross_profit = (

            data.loc[
                data["hourly_pnl"] > 0,
                "hourly_pnl"
            ]
            .sum()

        )



        gross_loss = abs(

            data.loc[
                data["hourly_pnl"] < 0,
                "hourly_pnl"
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



        metrics[country] = {


            "total_pnl_eur":
                round(
                    float(total_pnl),
                    2
                ),


            "volatility":
                round(
                    float(volatility),
                    2
                ),


            "sharpe_ratio":
                round(
                    float(sharpe),
                    4
                ),


            "max_drawdown_eur":
                round(
                    float(max_drawdown),
                    2
                ),


            "trades":
                int(trades),


            "win_rate":
                round(
                    float(win_rate),
                    4
                ),


            "profit_factor":
                round(
                    float(profit_factor),
                    4
                )

        }



        results.append(
            data
        )



        print(
            metrics[country]
        )



    final_results = pd.concat(
        results,
        ignore_index=True
    )


    return final_results, metrics



# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    print("="*70)

    print(
        "RUNNING ENERGY TRADING BACKTEST"
    )

    print("="*70)



    df = load_data()



    backtest_results, metrics = run_backtest(
        df
    )



    backtest_results.to_csv(
        OUTPUT_FILE,
        index=False
    )



    with open(
        METRICS_FILE,
        "w"
    ) as f:


        json.dump(
            metrics,
            f,
            indent=4
        )



    print("\n")

    print("="*70)

    print(
        "BACKTEST COMPLETED"
    )

    print("="*70)



    print("\nMETRICS")


    print("="*70)



    for country, values in metrics.items():


        print("\n")
        print(country.upper())


        for key,value in values.items():

            print(
                f"{key}: {value}"
            )



    print("\nSaved:")

    print(
        OUTPUT_FILE
    )

    print(
        METRICS_FILE
    )