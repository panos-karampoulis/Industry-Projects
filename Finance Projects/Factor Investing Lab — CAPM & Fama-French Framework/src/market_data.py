import yfinance as yf


def download_prices(
    tickers,
    start,
    end
):

    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True
    )


    prices = data["Close"]

    return prices

prices = download_prices(
    [
        "AAPL",
        "MSFT",
        "NVDA",
        "SPY"
    ],
    "2020-01-01",
    "2025-01-01"
)