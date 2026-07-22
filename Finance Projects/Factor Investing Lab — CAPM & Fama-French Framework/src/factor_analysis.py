import pandas as pd

from src.performance import (
    annual_return,
    annual_volatility,
    sharpe_ratio,
    max_drawdown
)



def factor_performance_table(portfolios):

    results = []


    for name, returns in portfolios.items():

        results.append({

            "Portfolio": name,

            "Annual Return":
                annual_return(returns),

            "Annual Volatility":
                annual_volatility(returns),

            "Sharpe Ratio":
                sharpe_ratio(returns),

            "Maximum Drawdown":
                max_drawdown(returns)

        })


    return pd.DataFrame(results)