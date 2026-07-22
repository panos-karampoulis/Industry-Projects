import pandas as pd
import numpy as np


def calculate_factor_backtest(
    prices,
    fundamentals,
    rebalance="ME"
):

    monthly_prices = (
    prices
    .resample("ME")
    .last()
    )


    monthly_returns = (
        monthly_prices
        .pct_change()
    )


    portfolio_returns = []


    dates = monthly_prices.index


    for i in range(13, len(dates)-1):

        current_date = dates[i]


        history = (
            monthly_prices
            .loc[:current_date]
        )


        # Momentum 12 months
        momentum = (
            history.iloc[-1]
            /
            history.iloc[-13]
            - 1
        )


        # Volatility 12 months
        volatility = (
            history
            .pct_change()
            .tail(12)
            .std()
        )


        # Normalize factors

        momentum_score = (
            momentum
            .rank(pct=True)
        )


        volatility_score = (
            1 -
            volatility
            .rank(pct=True)
        )


        quality_score = (
            fundamentals
            .set_index("Ticker")["ROE"]
            .rank(pct=True)
        )


        scores = pd.DataFrame({
            "Momentum": momentum_score,
            "LowVol": volatility_score,
            "Quality": quality_score
        })


        scores["Composite"] = (
            0.4 * scores["Momentum"]
            +
            0.3 * scores["Quality"]
            +
            0.3 * scores["LowVol"]
        )


        ranking = (
            scores
            .sort_values(
                "Composite",
                ascending=False
            )
        )


        cutoff = max(
            int(len(ranking)*0.2),
            1
        )


        long_stocks = (
            ranking
            .head(cutoff)
            .index
        )


        short_stocks = (
            ranking
            .tail(cutoff)
            .index
        )


        next_return = (
            monthly_returns
            .loc[dates[i+1]]
        )


        long_return = (
            next_return[long_stocks]
            .mean()
        )


        short_return = (
            next_return[short_stocks]
            .mean()
        )


        factor_return = long_return


        portfolio_returns.append(
            factor_return
        )


    return pd.Series(
        portfolio_returns,
        index=dates[14:]
    )