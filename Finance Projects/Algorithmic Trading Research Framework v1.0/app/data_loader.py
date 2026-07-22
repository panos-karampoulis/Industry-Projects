import yfinance as yf
import pandas as pd



def load_market_data(
        ticker,
        start_date="2015-01-01",
        end_date=None
):

    """
    Download historical OHLCV data
    """

    df = yf.download(
    ticker,
    start=start_date,
    end=end_date,
    auto_adjust=True,
    progress=False
    )


    if df.empty:

        raise ValueError(
            f"No market data found for {ticker}"
        )


    df = df.dropna()



        # Fix yfinance MultiIndex columns

    if isinstance(df.columns, pd.MultiIndex):

        df.columns = (
            df.columns
            .get_level_values(0)
        )

    return df




def validate_data(df):

    """
    Check required market columns
    """

    required = [

        "Open",
        "High",
        "Low",
        "Close",
        "Volume"

    ]


    return all(
        col in df.columns
        for col in required
    )




def get_close_price(df):

    """
    Return closing prices
    """

    close = df["Close"].copy()

    close.name = "Close"


    return close