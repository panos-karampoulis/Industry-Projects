import numpy as np
import pandas as pd
from scipy.optimize import minimize


def equal_weight_portfolio(
    returns: pd.DataFrame
) -> np.ndarray:
    """
    Create an equally weighted portfolio.

    Parameters
    ----------
    returns : pd.DataFrame

    Returns
    -------
    np.ndarray
        Portfolio weights.
    """

    n_assets = returns.shape[1]

    weights = np.ones(
        n_assets
    ) / n_assets

    return weights




def portfolio_return(
    weights: np.ndarray,
    expected_returns: pd.Series
) -> float:
    """
    Expected annual portfolio return.
    """

    return np.dot(
        weights,
        expected_returns
    )


def portfolio_volatility(
    weights: np.ndarray,
    covariance: pd.DataFrame
) -> float:
    """
    Annual portfolio volatility.
    """

    return np.sqrt(
        np.dot(
            weights.T,
            np.dot(
                covariance,
                weights
            )
        )
    )


def portfolio_sharpe(
    weights,
    expected_returns,
    covariance,
    risk_free_rate=0.02
):
    """
    Portfolio Sharpe ratio.
    """

    ret = portfolio_return(
        weights,
        expected_returns
    )

    vol = portfolio_volatility(
        weights,
        covariance
    )

    return (
        ret - risk_free_rate
    ) / vol


def minimum_variance_portfolio(
    covariance
):
    """
    Compute the minimum variance portfolio.
    """

    n_assets = len(covariance)

    initial_weights = (
        np.ones(n_assets)
        / n_assets
    )


    bounds = tuple(
        (0, 1)
        for _ in range(n_assets)
    )


    constraints = (
        {
            "type": "eq",
            "fun": lambda w: np.sum(w) - 1
        },
    )


    result = minimize(
        portfolio_volatility,
        initial_weights,
        args=(covariance,),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )


    return result.x


def negative_sharpe(
    weights,
    expected_returns,
    covariance,
    risk_free_rate=0.02
):
    """
    Negative Sharpe ratio
    because scipy minimizes.
    """

    return -portfolio_sharpe(
        weights,
        expected_returns,
        covariance,
        risk_free_rate
    )

def maximum_sharpe_portfolio(
    expected_returns,
    covariance,
    risk_free_rate=0.02
):
    """
    Calculate maximum Sharpe portfolio.
    """

    n_assets = len(expected_returns)


    initial_weights = (
        np.ones(n_assets)
        / n_assets
    )


    bounds = tuple(
        (0,1)
        for _ in range(n_assets)
    )


    constraints = (
        {
            "type": "eq",
            "fun": lambda w: np.sum(w)-1
        },
    )


    result = minimize(
        negative_sharpe,
        initial_weights,
        args=(
            expected_returns,
            covariance,
            risk_free_rate
        ),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )


    return result.x


def risk_contribution(
    weights,
    covariance
):
    """
    Calculate risk contribution of each asset.
    """

    portfolio_vol = portfolio_volatility(
        weights,
        covariance
    )

    marginal_contribution = (
        covariance @ weights
    )

    return (
        weights * marginal_contribution
    ) / portfolio_vol


def risk_parity_objective(
    weights,
    covariance
):
    """
    Minimize difference between
    risk contributions.
    """

    contributions = risk_contribution(
        weights,
        covariance
    )

    target = (
        np.ones(len(weights))
        / len(weights)
    )

    return np.sum(
        (contributions - target * contributions.sum()) ** 2
    )


def risk_parity_portfolio(
    covariance
):
    """
    Compute risk parity weights.
    """

    n_assets = len(covariance)


    initial_weights = (
        np.ones(n_assets)
        / n_assets
    )


    bounds = tuple(
        (0,1)
        for _ in range(n_assets)
    )


    constraints = (
        {
            "type": "eq",
            "fun": lambda w: np.sum(w)-1
        },
    )


    result = minimize(
        risk_parity_objective,
        initial_weights,
        args=(covariance,),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )


    return result.x