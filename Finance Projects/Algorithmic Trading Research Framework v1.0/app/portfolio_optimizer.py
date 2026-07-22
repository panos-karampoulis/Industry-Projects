import pandas as pd



def calculate_sharpe_weights(
        sharpe_ratios
):

    """
    Convert strategy Sharpe ratios
    into portfolio weights
    """

    
    sharpe = pd.Series(
        sharpe_ratios
    )


    # avoid negative weights

    sharpe = sharpe.clip(
        lower=0
    )


    weights = (

        sharpe
        /
        sharpe.sum()

    )


    return weights