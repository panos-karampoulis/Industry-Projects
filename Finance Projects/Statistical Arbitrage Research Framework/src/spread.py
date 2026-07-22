"""
Spread construction utilities for the Statistical Arbitrage Research Framework.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression


def estimate_hedge_ratio(
    series_y: pd.Series,
    series_x: pd.Series
) -> tuple[float, float]:
    """
    Estimate hedge ratio using linear regression.

    Model:

    Y = alpha + beta * X

    Parameters
    ----------
    series_y : pd.Series
        Dependent variable.

    series_x : pd.Series
        Independent variable.

    Returns
    -------
    tuple
        alpha, beta
    """

    model = LinearRegression()

    X = series_x.values.reshape(-1, 1)

    y = series_y.values

    model.fit(
        X,
        y
    )

    alpha = model.intercept_

    beta = model.coef_[0]

    return alpha, beta



def calculate_spread(
    series_y: pd.Series,
    series_x: pd.Series,
    beta: float,
    alpha: float = 0
) -> pd.Series:
    """
    Calculate the spread between two assets.

    Spread:

    Y - beta*X - alpha

    Parameters
    ----------
    series_y : pd.Series

    series_x : pd.Series

    beta : float

    alpha : float

    Returns
    -------
    pd.Series
    """

    spread = (
        series_y
        -
        (alpha + beta * series_x)
    )

    return spread



def calculate_zscore(
    spread: pd.Series,
    window: int = 60
) -> pd.Series:
    """
    Calculate rolling z-score of spread.

    Formula:

    Z = (Spread - Mean) / Std

    Parameters
    ----------
    spread : pd.Series

    window : int

    Returns
    -------
    pd.Series
    """

    mean = spread.rolling(
        window
    ).mean()

    std = spread.rolling(
        window
    ).std()

    zscore = (
        spread - mean
    ) / std

    return zscore



def spread_statistics(
    spread: pd.Series
) -> pd.DataFrame:
    """
    Summary statistics of the spread.
    """

    stats = pd.DataFrame({

        "Mean": [spread.mean()],

        "Std": [spread.std()],

        "Min": [spread.min()],

        "Max": [spread.max()],

        "Last Value": [spread.iloc[-1]]

    })

    return stats


def calculate_half_life(
    spread: pd.Series
) -> float:
    """
    Estimate mean reversion half-life.

    The half-life measures the expected time
    required for the spread to revert halfway
    towards its mean.

    Parameters
    ----------
    spread : pd.Series

    Returns
    -------
    float
        Estimated half-life in periods.
    """

    spread_lag = spread.shift(1)

    spread_diff = spread.diff()

    df = pd.concat(
        [
            spread_lag,
            spread_diff
        ],
        axis=1
    )

    df.columns = [
        "lag",
        "diff"
    ]

    df = df.dropna()

    model = LinearRegression()

    X = df["lag"].values.reshape(-1, 1)

    y = df["diff"].values

    model.fit(
        X,
        y
    )

    beta = model.coef_[0]

    if beta >= 0:
        return np.inf

    half_life = (
        -np.log(2) / beta
    )

    return half_life



def calculate_hurst_exponent(
    series: pd.Series,
    max_lag: int = 100
) -> float:
    """
    Estimate Hurst exponent.

    Interpretation:

    H < 0.5  -> Mean reverting
    H = 0.5  -> Random walk
    H > 0.5  -> Trending

    Parameters
    ----------
    series : pd.Series

    max_lag : int

    Returns
    -------
    float
    """

    lags = range(
        2,
        max_lag
    )

    tau = []

    for lag in lags:

        diff = (
            series.diff(
                lag
            )
            .dropna()
        )

        tau.append(
            np.sqrt(
                diff.std()
            )
        )

    poly = np.polyfit(
        np.log(list(lags)),
        np.log(tau),
        1
    )

    hurst = poly[0] * 2

    return hurst