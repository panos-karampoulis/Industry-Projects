import pandas as pd


def load_prices(path):

    """
    Load historical adjusted prices
    """

    prices = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True
    )

    return prices