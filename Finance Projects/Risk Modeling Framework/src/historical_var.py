import numpy as np


def historical_var(
    portfolio_returns,
    confidence=0.95
):
    """
    Historical Simulation VaR
    """

    percentile = (1-confidence)*100

    var = -np.percentile(
        portfolio_returns,
        percentile
    )

    return var



def historical_var_amount(
    portfolio_returns,
    portfolio_value,
    confidence=0.95
):

    var = historical_var(
        portfolio_returns,
        confidence
    )

    return var * portfolio_value