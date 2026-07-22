import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands




def add_sma(
        df,
        window=50
):

    df[f"SMA_{window}"] = (
        SMAIndicator(
            close=df["Close"],
            window=window
        )
        .sma_indicator()
    )

    return df




def add_ema(
        df,
        window=50
):

    df[f"EMA_{window}"] = (
        EMAIndicator(
            close=df["Close"],
            window=window
        )
        .ema_indicator()
    )

    return df




def add_rsi(
        df,
        window=14
):

    df["RSI"] = (
        RSIIndicator(
            close=df["Close"],
            window=window
        )
        .rsi()
    )

    return df




def add_macd(df):

    macd = MACD(
        close=df["Close"]
    )

    df["MACD"] = (
        macd.macd()
    )

    df["MACD_SIGNAL"] = (
        macd.macd_signal()
    )

    return df




def add_bollinger_bands(
        df,
        window=20
):

    bb = BollingerBands(
        close=df["Close"],
        window=window
    )


    df["BB_HIGH"] = (
        bb.bollinger_hband()
    )


    df["BB_LOW"] = (
        bb.bollinger_lband()
    )


    df["BB_MIDDLE"] = (
        bb.bollinger_mavg()
    )


    return df




def build_indicators(df):

    """
    Add all indicators
    """

    df = df.copy()


    df = add_sma(
        df,
        50
    )


    df = add_sma(
        df,
        200
    )


    df = add_ema(
        df,
        50
    )


    df = add_rsi(
        df
    )


    df = add_macd(
        df
    )


    df = add_bollinger_bands(
        df
    )


    return df