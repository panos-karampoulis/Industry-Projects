import pandas as pd


def calculate_returns(
    prices: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate daily percentage returns.

    Parameters
    ----------
    prices : pd.DataFrame
        Historical prices.

    Returns
    -------
    pd.DataFrame
        Daily returns.
    """

    returns = (
        prices
        .pct_change()
        .dropna()
    )

    return returns


def annualized_returns(
    returns: pd.DataFrame
) -> pd.Series:
    """
    Calculate annualized expected returns.
    """

    return (
        returns.mean()
        * 252
    )


def annualized_covariance(
    returns: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate annualized covariance matrix.
    """

    return (
        returns.cov()
        * 252
    )


def annualized_volatility(
    returns: pd.DataFrame
) -> pd.Series:
    """
    Calculate annualized volatility.
    """

    return (
        returns.std()
        * (252 ** 0.5)
    )