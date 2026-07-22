import pandas as pd



def combine_strategies(
        strategy_returns,
        weights=None
):


    """
    Combine multiple strategy returns
    into one portfolio
    """


    if weights is None:

        weights = {

            col:1/len(strategy_returns.columns)

            for col in strategy_returns.columns

        }



    portfolio_returns = pd.Series(
        0,
        index=strategy_returns.index
    )



    for strategy, weight in weights.items():

        portfolio_returns += (

            strategy_returns[strategy]
            *
            weight

        )



    return portfolio_returns