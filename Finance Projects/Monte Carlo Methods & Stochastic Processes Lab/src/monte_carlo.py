import numpy as np



def european_call_mc(
    terminal_prices,
    K,
    r,
    T
):
    """
    Monte Carlo European Call Option Pricing
    """


    payoff = np.maximum(
        terminal_prices - K,
        0
    )


    price = np.exp(
        -r*T
    ) * payoff.mean()


    return price



def european_put_mc(
    terminal_prices,
    K,
    r,
    T
):
    """
    Monte Carlo European Put Option Pricing
    """


    payoff = np.maximum(
        K - terminal_prices,
        0
    )


    price = np.exp(
        -r*T
    ) * payoff.mean()


    return price