import pandas as pd


def calculate_portfolio_returns(
    prices,
    stocks
):

    returns = (
        prices[stocks]
        .pct_change()
    )

    portfolio_returns = (
        returns
        .mean(axis=1)
    )

    return portfolio_returns



def calculate_long_short_returns(
    prices,
    long_stocks,
    short_stocks
):

    long_returns = (
        calculate_portfolio_returns(
            prices,
            long_stocks
        )
    )


    short_returns = (
        calculate_portfolio_returns(
            prices,
            short_stocks
        )
    )


    long_short = (
        long_returns
        -
        short_returns
    )


    return (
        long_returns,
        short_returns,
        long_short
    )