"""
Cointegration utilities for the Statistical Arbitrage Research Framework.
"""

from __future__ import annotations

import pandas as pd

from statsmodels.tsa.stattools import coint


def cointegration_test(
    series_1: pd.Series,
    series_2: pd.Series
) -> tuple[float, float]:
    """
    Perform the Engle-Granger cointegration test.

    Parameters
    ----------
    series_1 : pd.Series

    series_2 : pd.Series

    Returns
    -------
    tuple
        test statistic, p-value
    """

    statistic, pvalue, _ = coint(
        series_1,
        series_2
    )

    return statistic, pvalue


def analyze_pairs(
    prices: pd.DataFrame,
    ranking: pd.DataFrame
) -> pd.DataFrame:
    """
    Run cointegration test on every pair.

    Parameters
    ----------
    prices : pd.DataFrame

    ranking : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """

    results = []

    for _, row in ranking.iterrows():

        stock_1 = row["Stock_1"]
        stock_2 = row["Stock_2"]

        statistic, pvalue = cointegration_test(
            prices[stock_1],
            prices[stock_2]
        )

        results.append({

            "Stock_1": stock_1,

            "Stock_2": stock_2,

            "Correlation": row["Correlation"],

            "Test_Statistic": statistic,

            "P_Value": pvalue,

            "Cointegrated": pvalue < 0.05

        })

    results = pd.DataFrame(results)

    results = results.sort_values(
        "P_Value"
    ).reset_index(drop=True)

    return results


def cointegrated_pairs(
    results: pd.DataFrame,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Return statistically cointegrated pairs.
    """

    filtered = results[
        results["P_Value"] < alpha
    ].copy()

    filtered.reset_index(
        drop=True,
        inplace=True
    )

    return filtered