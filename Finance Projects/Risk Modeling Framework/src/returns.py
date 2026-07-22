import numpy as np


def calculate_returns(prices):

    """
    Daily percentage returns
    """

    returns = prices.pct_change()

    return returns.dropna()



def calculate_log_returns(prices):

    """
    Daily logarithmic returns
    """

    log_returns = np.log(
        prices / prices.shift(1)
    )

    return log_returns.dropna()



def calculate_portfolio_returns(
    returns,
    weights
):

    """
    Portfolio return calculation
    """

    weights = np.array(weights)


    portfolio_returns = (
        returns * weights
    ).sum(axis=1)


    return portfolio_returns