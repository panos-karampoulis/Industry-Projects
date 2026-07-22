import numpy as np
from scipy.stats import norm



def black_scholes_call(
    S0,
    K,
    r,
    sigma,
    T
):
    """
    Black-Scholes European Call Option Price
    """


    d1 = (
        np.log(S0 / K)
        +
        (r + 0.5 * sigma**2) * T
    ) / (
        sigma * np.sqrt(T)
    )


    d2 = (
        d1
        -
        sigma * np.sqrt(T)
    )


    call_price = (
        S0 * norm.cdf(d1)
        -
        K * np.exp(-r*T) * norm.cdf(d2)
    )


    return call_price



def black_scholes_put(
    S0,
    K,
    r,
    sigma,
    T
):
    """
    Black-Scholes European Put Option Price
    """


    d1 = (
        np.log(S0 / K)
        +
        (r + 0.5*sigma**2)*T
    ) / (
        sigma*np.sqrt(T)
    )


    d2 = (
        d1
        -
        sigma*np.sqrt(T)
    )


    put_price = (
        K*np.exp(-r*T)*norm.cdf(-d2)
        -
        S0*norm.cdf(-d1)
    )


    return put_price