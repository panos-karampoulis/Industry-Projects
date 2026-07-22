import yfinance  as yf
import pandas  as pd


def download_prices(
    tickers,
    start="2015-01-01",
    end="2025-12-31"
):

    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True
    )

    prices = data["Close"]

    return prices