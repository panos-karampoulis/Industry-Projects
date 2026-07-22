import pandas as pd


def create_factor_portfolios(
    factor_ranking,
    quantile=0.2
):

    n = len(factor_ranking)

    cutoff = int(
        n * quantile
    )


    long_portfolio = (
        factor_ranking
        .head(cutoff)
        .index
    )


    short_portfolio = (
        factor_ranking
        .tail(cutoff)
        .index
    )


    return (
        list(long_portfolio),
        list(short_portfolio)
    )