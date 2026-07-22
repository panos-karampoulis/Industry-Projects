import numpy as np
import pandas as pd


def calculate_performance_metrics(
    returns
):

    cumulative_return = (
        (1 + returns)
        .cumprod()
        .iloc[-1]
        - 1
    )


    annual_return = (
    (1 + cumulative_return)
    ** (12 / len(returns))
    - 1
    )


    annual_volatility = (
    returns.std()
    *
    np.sqrt(12)
    )


    sharpe_ratio = (
        annual_return
        /
        annual_volatility
    )


    cumulative = (
        1 + returns
    ).cumprod()


    running_max = (
        cumulative
        .cummax()
    )


    drawdown = (
        cumulative
        /
        running_max
        - 1
    )


    max_drawdown = (
        drawdown
        .min()
    )


    return pd.DataFrame({
        "Annual Return":[annual_return],
        "Sharpe Ratio":[sharpe_ratio],
        "Max Drawdown":[max_drawdown]
    })