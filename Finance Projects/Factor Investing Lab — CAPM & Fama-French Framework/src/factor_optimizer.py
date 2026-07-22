import numpy as np
import pandas as pd



def optimize_factor_weights(
        portfolio_returns
):


    names = list(
        portfolio_returns.columns
    )


    returns = (
        portfolio_returns
        .mean()
        *
        252
    )


    cov = (
        portfolio_returns
        .cov()
        *
        252
    )


    best_sharpe = -999

    best_weights = None


    for _ in range(10000):

        weights = np.random.random(
            len(names)
        )


        weights /= weights.sum()


        port_return = (
            weights @ returns
        )


        port_vol = np.sqrt(
            weights.T
            @ cov
            @ weights
        )


        sharpe = (
            port_return /
            port_vol
        )


        if sharpe > best_sharpe:

            best_sharpe = sharpe

            best_weights = weights



    result = pd.DataFrame({

        "Factor":
            names,

        "Weight":
            best_weights

    })


    return result, best_sharpe