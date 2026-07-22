def calculate_returns(prices):

    returns = (
        prices
        .pct_change()
        .dropna()
    )

    return returns