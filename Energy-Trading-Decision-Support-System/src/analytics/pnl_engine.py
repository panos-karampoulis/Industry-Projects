from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[2]

RESULTS_DIR = BASE_DIR / "results"

OUTPUT_FILE = RESULTS_DIR / "trading_pnl.csv"


def calculate_pnl(df):

    df = df.copy()

    df["position"] = (
        df["trading_signal"]
        .map(
            {
                "BUY": 1,
                "SELL": -1,
                "HOLD": 0
            }
        )
        .fillna(0)
    )

    df["price_change"] = (
        df["day_ahead_price"]
        .diff()
    )

    df["price_change"] = (
        df["price_change"]
        .fillna(0)
    )

    df["hourly_pnl"] = (
        df["position"].shift(1).fillna(0)
        *
        df["price_change"]
    )

    df["cumulative_pnl"] = (
        df["hourly_pnl"]
        .cumsum()
    )

    df["trade_id"] = (
        (
            df["position"]
            !=
            df["position"].shift()
        )
        .cumsum()
    )

    return df


def calculate_metrics(df):

    pnl = df["hourly_pnl"]

    total_return = pnl.sum()

    total_trades = (
        df["position"] != 0
    ).sum()

    winning = (
        pnl > 0
    ).sum()

    losing = (
        pnl < 0
    ).sum()

    hit_ratio = (
        winning /
        max(
            winning + losing,
            1
        )
    )

    gross_profit = pnl[pnl > 0].sum()

    gross_loss = abs(
        pnl[pnl < 0].sum()
    )

    profit_factor = (
        gross_profit /
        gross_loss
        if gross_loss != 0
        else np.nan
    )

    equity = df["cumulative_pnl"]

    rolling_max = equity.cummax()

    drawdown = (
        equity
        -
        rolling_max
    )

    max_drawdown = drawdown.min()

    return {

        "total_pnl": round(total_return, 2),

        "total_trades": int(total_trades),

        "winning_trades": int(winning),

        "losing_trades": int(losing),

        "hit_ratio": round(hit_ratio * 100, 2),

        "profit_factor": round(profit_factor, 2),

        "max_drawdown": round(max_drawdown, 2),

        "best_trade": round(
            pnl.max(),
            2
        ),

        "worst_trade": round(
            pnl.min(),
            2
        ),

        "average_trade": round(
            pnl.mean(),
            2
        )
    }


def run():

    file = (
        RESULTS_DIR
        /
        "trading_decisions_all_countries.csv"
    )

    df = pd.read_csv(file)

    pnl_df = calculate_pnl(df)

    pnl_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    metrics = calculate_metrics(pnl_df)

    print()

    print("=" * 60)

    print("PnL SUMMARY")

    print("=" * 60)

    for k, v in metrics.items():

        print(f"{k}: {v}")

    print()

    print("Saved:")

    print(OUTPUT_FILE)


if __name__ == "__main__":

    run()