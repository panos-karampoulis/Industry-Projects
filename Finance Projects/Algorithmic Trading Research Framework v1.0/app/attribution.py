import pandas as pd
import numpy as np



def calculate_return_contribution(
        strategy_returns,
        weights
):

    """
    Calculates contribution of each strategy
    to total portfolio return
    """


    contributions = {}


    for strategy in strategy_returns.columns:


        contribution = (

            strategy_returns[strategy]
            .mean()

            *
            weights[strategy]

        )


        contributions[strategy] = contribution



    return pd.Series(
        contributions
    )





def calculate_risk_contribution(
        strategy_returns,
        weights
):

    """
    Approximate volatility contribution
    """


    portfolio_volatility = (

        strategy_returns
        .mul(
            pd.Series(weights)
        )
        .sum(axis=1)
        .std()

    )


    risk = {}



    for strategy in strategy_returns.columns:


        strategy_vol = (

            strategy_returns[strategy]
            .std()

        )


        risk[strategy] = (

            strategy_vol
            *
            weights[strategy]
            /
            portfolio_volatility

        )



    return pd.Series(
        risk
    )





def correlation_matrix(
        strategy_returns
):


    return (
        strategy_returns
        .corr()
    )