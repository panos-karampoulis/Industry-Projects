import pandas as pd
import numpy as np



def momentum_scores(
    prices,
    lookback=252
):

    scores = (
        prices
        /
        prices.shift(lookback)
        - 1
    )

    return scores.iloc[-1]



def volatility_scores(
    returns,
    window=252
):

    vol = (
        returns
        .rolling(window)
        .std()
        *
        np.sqrt(252)
    )


    return vol.iloc[-1]



def select_top_assets(
    scores,
    n=3,
    ascending=False
):

    return (
        scores
        .sort_values(
            ascending=ascending
        )
        .head(n)
        .index
        .tolist()
    )



def equal_weight_portfolio(
    assets
):

    weight = 1 / len(assets)

    return {
        asset: weight
        for asset in assets
    }