import pandas as pd



def sma_crossover_strategy(df):

    """
    SMA 50 / SMA 200 crossover strategy
    """


    signals = pd.DataFrame(
        index=df.index
    )


    signals["position"] = 0


    signals.loc[
        df["SMA_50"] > df["SMA_200"],
        "position"
    ] = 1


    signals.loc[
        df["SMA_50"] < df["SMA_200"],
        "position"
    ] = 0


    return signals

def rsi_mean_reversion(
        df,
        lower=30,
        upper=70
):

    signals = pd.DataFrame(
        index=df.index
    )


    signals["position"] = 0


    signals.loc[
        df["RSI"] < lower,
        "position"
    ] = 1


    signals.loc[
        df["RSI"] > upper,
        "position"
    ] = 0


    return signals

def momentum_strategy(
        df,
        window=252
):

    signals = pd.DataFrame(
        index=df.index
    )


    momentum = (
        df["Close"]
        .pct_change(window)
    )


    signals["position"] = 0


    signals.loc[
        momentum > 0,
        "position"
    ] = 1


    return signals