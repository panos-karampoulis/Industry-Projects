import numpy as np



def confidence_interval(
    discounted_payoffs,
    confidence=0.95
):
    """
    Calculate Monte Carlo confidence interval
    """


    mean = discounted_payoffs.mean()


    std = discounted_payoffs.std(
        ddof=1
    )


    n = len(discounted_payoffs)


    standard_error = std / np.sqrt(n)


    z = 1.96


    lower = (
        mean
        -
        z * standard_error
    )


    upper = (
        mean
        +
        z * standard_error
    )


    return mean, lower, upper



def pricing_error(
    monte_carlo_price,
    benchmark_price
):
    """
    Absolute pricing error
    """


    return abs(
        monte_carlo_price
        -
        benchmark_price
    )