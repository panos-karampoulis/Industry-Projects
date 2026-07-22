import numpy as np



def sharpe_ratio(
    returns,
    rf=0
):

    excess = returns - rf

    return (
        excess.mean()
        /
        excess.std()
        *
        np.sqrt(252)
    )



def annual_return(
    returns
):

    return (
        (1 + returns.mean())**252
        -1
    )



def annual_volatility(
    returns
):

    return (
        returns.std()
        *
        np.sqrt(252)
    )



def max_drawdown(
    returns
):

    cumulative = (
        1 + returns
    ).cumprod()


    peak = cumulative.cummax()


    drawdown = (
        cumulative - peak
    ) / peak


    return drawdown.min()