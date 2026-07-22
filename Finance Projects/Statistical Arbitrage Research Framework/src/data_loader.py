"""
Data loading utilities for the Statistical Arbitrage Research Framework.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf


def load_market_data(
    tickers: list[str],
    start: str,
    end: str,
) -> pd.DataFrame:
    """
    Download adjusted closing prices from Yahoo Finance.

    Parameters
    ----------
    tickers : list[str]
        List of ticker symbols.

    start : str
        Start date (YYYY-MM-DD).

    end : str
        End date (YYYY-MM-DD).

    Returns
    -------
    pd.DataFrame
        Daily closing prices.
    """

    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
    )

    prices = data["Close"]

    prices = prices.dropna(
        axis=1,
        how="all"
    )

    prices = prices.ffill()

    return prices


def calculate_returns(
    prices: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate daily percentage returns.
    """

    returns = prices.pct_change()

    returns = returns.dropna()

    return returns


def summary_statistics(
    prices: pd.DataFrame
) -> pd.DataFrame:
    """
    Basic summary statistics.
    """

    summary = pd.DataFrame({

        "Start Price": prices.iloc[0],

        "End Price": prices.iloc[-1],

        "Observations": prices.count(),

        "Missing Values": prices.isna().sum()

    })

    return summary