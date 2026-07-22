import numpy as np
import pandas as pd

from src.optimization import (
    portfolio_return,
    portfolio_volatility,
    portfolio_sharpe
)


def generate_random_portfolios(
    expected_returns,
    covariance,
    n_portfolios=5000,
    risk_free_rate=0.02
):
    """
    Generate random portfolios
    for efficient frontier.
    """

    results = []

    n_assets = len(expected_returns)


    for _ in range(n_portfolios):

        weights = np.random.random(
            n_assets
        )

        weights /= np.sum(weights)


        ret = portfolio_return(
            weights,
            expected_returns
        )


        vol = portfolio_volatility(
            weights,
            covariance
        )


        sharpe = portfolio_sharpe(
            weights,
            expected_returns,
            covariance,
            risk_free_rate
        )


        results.append(
            [
                ret,
                vol,
                sharpe,
                weights
            ]
        )


    frontier = pd.DataFrame(
        results,
        columns=[
            "Return",
            "Volatility",
            "Sharpe",
            "Weights"
        ]
    )


    return frontier