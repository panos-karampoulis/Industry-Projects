import pandas as pd
import numpy as np


def portfolio_returns(
    returns: pd.DataFrame,
    weights: np.ndarray
) -> pd.Series:
    """
    Calculate daily portfolio returns.
    """

    portfolio = (
        returns
        @ weights
    )

    return portfolio



def cumulative_returns(
    portfolio_returns: pd.Series
) -> pd.Series:
    """
    Calculate cumulative performance.
    """

    return (
        1 + portfolio_returns
    ).cumprod()



def maximum_drawdown(
    cumulative: pd.Series
) -> float:
    """
    Calculate maximum drawdown.
    """

    running_max = (
        cumulative
        .cummax()
    )

    drawdown = (
        cumulative - running_max
    ) / running_max


    return drawdown.min()



def rolling_volatility(
    portfolio_returns: pd.Series,
    window=60
) -> pd.Series:
    """
    Rolling annualized volatility.
    """

    return (
        portfolio_returns
        .rolling(window)
        .std()
        * np.sqrt(252)
    )