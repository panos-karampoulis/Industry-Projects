import pandas as pd



def load_prices(path):

    prices = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True
    )

    return prices



def load_market(path):

    market = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True
    )

    return market