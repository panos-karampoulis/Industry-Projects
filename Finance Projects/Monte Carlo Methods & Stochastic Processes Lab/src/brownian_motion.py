import numpy as np


def simulate_gbm(
    S0,
    mu,
    sigma,
    T,
    steps,
    simulations,
    seed=None
):
    """
    Simulate Geometric Brownian Motion paths.

    Parameters
    ----------
    S0 : float
        Initial asset price

    mu : float
        Drift parameter

    sigma : float
        Volatility

    T : float
        Time horizon in years

    steps : int
        Number of time steps

    simulations : int
        Number of simulated paths

    seed : int
        Random seed for reproducibility


    Returns
    -------
    prices : ndarray
        Simulated price paths
    """

    if seed is not None:
        np.random.seed(seed)


    dt = T / steps


    Z = np.random.normal(
        0,
        1,
        (steps, simulations)
    )


    prices = np.zeros(
        (steps + 1, simulations)
    )


    prices[0] = S0


    for t in range(1, steps + 1):

        prices[t] = prices[t-1] * np.exp(

            (mu - 0.5 * sigma**2) * dt

            +

            sigma * np.sqrt(dt) * Z[t-1]

        )


    return prices