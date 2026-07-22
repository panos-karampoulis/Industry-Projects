import numpy as np



def monte_carlo_var(
    portfolio_returns,
    confidence=0.95,
    simulations=100000
):
    """
    Monte Carlo VaR
    """

    mu = portfolio_returns.mean()

    sigma = portfolio_returns.std()


    simulated_returns = np.random.normal(
        mu,
        sigma,
        simulations
    )


    percentile = (
        1-confidence
    )*100


    var = -np.percentile(
        simulated_returns,
        percentile
    )


    return var



def monte_carlo_var_amount(
    portfolio_returns,
    portfolio_value,
    confidence=0.95,
    simulations=100000
):

    var = monte_carlo_var(
        portfolio_returns,
        confidence,
        simulations
    )


    return var * portfolio_value