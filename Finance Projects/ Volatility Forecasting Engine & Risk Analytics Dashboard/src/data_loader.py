import yfinance as yf
import os


def download_market_data(
    ticker,
    start_date,
    end_date
):

    print(f"Downloading {ticker} data...")

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    return data


def save_data(data, ticker):

    os.makedirs(
        "data",
        exist_ok=True
    )

    file_path = f"data/{ticker}_market_data.csv"

    data.to_csv(file_path)

    print(f"Data saved to {file_path}")


if __name__ == "__main__":

    ticker = "SPY"

    data = download_market_data(
        ticker,
        "2010-01-01",
        "2026-01-01"
    )

    print(data.head())

    save_data(
        data,
        ticker
    )