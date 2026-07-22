"""
Backtesting utilities for pairs trading strategies.
"""

from __future__ import annotations

import numpy as np
import pandas as pd



def calculate_strategy_returns(
    series_y: pd.Series,
    series_x: pd.Series,
    beta: float,
    positions: pd.Series
) -> pd.Series:
    """
    Calculate dollar neutral pairs trading returns.

    Long spread:
        Long Y
        Short beta * X

    Short spread:
        Short Y
        Long beta * X
    """

    y_returns = series_y.pct_change()

    x_returns = series_x.pct_change()


    spread_returns = (
        y_returns
        -
        beta * x_returns
    )


    strategy_returns = (
        positions.shift(1)
        *
        spread_returns
    )


    return strategy_returns



def cumulative_returns(
    returns: pd.Series
) -> pd.Series:
    """
    Calculate cumulative returns.

    Parameters
    ----------
    returns : pd.Series

    Returns
    -------
    pd.Series
    """

    cumulative = (
        1 + returns.fillna(0)
    ).cumprod()

    return cumulative



def sharpe_ratio(
    returns: pd.Series,
    periods: int = 252
) -> float:
    """
    Calculate annualized Sharpe ratio.

    Parameters
    ----------
    returns : pd.Series

    periods : int

    Returns
    -------
    float
    """

    return (
        returns.mean()
        /
        returns.std()
        *
        np.sqrt(periods)
    )



def maximum_drawdown(
    cumulative: pd.Series
) -> float:
    """
    Calculate maximum drawdown.

    Parameters
    ----------
    cumulative : pd.Series

    Returns
    -------
    float
    """

    running_max = (
        cumulative
        .cummax()
    )

    drawdown = (
        cumulative - running_max
    ) / running_max

    return drawdown.min()



def performance_summary(
    returns: pd.Series
) -> pd.DataFrame:
    """
    Create performance report.
    """

    cumulative = cumulative_returns(
        returns
    )

    summary = pd.DataFrame({

        "Total Return": [
            cumulative.iloc[-1] - 1
        ],

        "Sharpe Ratio": [
            sharpe_ratio(
                returns
            )
        ],

        "Max Drawdown": [
            maximum_drawdown(
                cumulative
            )
        ]

    })

    return summary