import pandas as pd


def equal_weight_portfolio(
    returns_list
):
    """
    Combine multiple strategy returns
    using equal weights.
    """

    returns_df = pd.concat(
        returns_list,
        axis=1
    )

    portfolio_returns = (
        returns_df
        .mean(axis=1)
    )

    return portfolio_returns