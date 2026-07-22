import pandas as pd


def apply_transaction_costs(
    returns,
    positions,
    cost=0.001
):
    """
    Apply transaction costs.

    cost:
        transaction cost per position change
    """

    trades = (
        positions
        .diff()
        .abs()
    )

    costs = (
        trades
        * cost
    )

    net_returns = (
        returns
        - costs
    )

    return net_returns