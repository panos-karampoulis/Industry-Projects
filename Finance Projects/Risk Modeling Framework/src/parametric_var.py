import numpy as np
from scipy.stats import norm



def parametric_var(
    portfolio_returns,
    confidence=0.95
):
    """
    Parametric VaR assuming normal distribution
    """

    mu = portfolio_returns.mean()

    sigma = portfolio_returns.std()


    z = norm.ppf(
        1-confidence
    )


    var = -(mu + z*sigma)


    return var



def parametric_var_amount(
    portfolio_returns,
    portfolio_value,
    confidence=0.95
):

    var = parametric_var(
        portfolio_returns,
        confidence
    )


    return var * portfolio_value