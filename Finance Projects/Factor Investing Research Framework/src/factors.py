import pandas as pd


def calculate_momentum(
    prices,
    window=252
):
    """
    Calculate 12-month momentum.

    Momentum =
    Current Price / Price 252 days ago - 1
    """

    momentum = (
        prices
        /
        prices.shift(window)
        - 1
    )

    return momentum


def calculate_volatility(
    prices,
    window=252
):
    """
    Calculate annualized volatility.

    Volatility =
    daily return std * sqrt(252)
    """

    returns = prices.pct_change()

    volatility = (
        returns
        .rolling(window)
        .std()
        *
        (252 ** 0.5)
    )

    return volatility