"""
Pair selection utilities for the Statistical Arbitrage Research Framework.
"""

from __future__ import annotations

from itertools import combinations

import pandas as pd


def generate_pairs(
    tickers: list[str]
) -> list[tuple[str, str]]:
    """
    Generate all unique stock pairs.

    Parameters
    ----------
    tickers : list[str]
        List of ticker symbols.

    Returns
    -------
    list[tuple[str, str]]
        All unique ticker pairs.
    """

    return list(combinations(tickers, 2))


def correlation_matrix(
    returns: pd.DataFrame
) -> pd.DataFrame:
    """
    Compute the Pearson correlation matrix.

    Parameters
    ----------
    returns : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """

    return returns.corr()


def rank_pairs(
    returns: pd.DataFrame
) -> pd.DataFrame:
    """
    Rank all stock pairs by correlation.

    Parameters
    ----------
    returns : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Ranked correlation table.
    """

    corr = correlation_matrix(returns)

    pairs = generate_pairs(list(corr.columns))

    results = []

    for stock1, stock2 in pairs:

        results.append(
            {
                "Stock_1": stock1,
                "Stock_2": stock2,
                "Correlation": corr.loc[stock1, stock2]
            }
        )

    ranking = pd.DataFrame(results)

    ranking = ranking.sort_values(
        "Correlation",
        ascending=False
    ).reset_index(drop=True)

    return ranking


def top_pairs(
    ranking: pd.DataFrame,
    n: int = 10
) -> pd.DataFrame:
    """
    Return the top n correlated pairs.

    Parameters
    ----------
    ranking : pd.DataFrame

    n : int

    Returns
    -------
    pd.DataFrame
    """

    return ranking.head(n)


def filter_pairs(
    ranking: pd.DataFrame,
    minimum_correlation: float = 0.80
) -> pd.DataFrame:
    """
    Filter pairs above a correlation threshold.

    Parameters
    ----------
    ranking : pd.DataFrame

    minimum_correlation : float

    Returns
    -------
    pd.DataFrame
    """

    filtered = ranking[
        ranking["Correlation"] >= minimum_correlation
    ].copy()

    filtered.reset_index(
        drop=True,
        inplace=True
    )

    return filtered