import numpy as np




def calculate_volatility(portfolio):

    returns = portfolio.returns()

    return returns.std() * np.sqrt(252)




def calculate_sortino(portfolio):

    returns = portfolio.returns()

    downside = returns[returns < 0]

    if len(downside) == 0:
        return np.nan


    downside_std = (
        downside.std()
        *
        np.sqrt(252)
    )


    return (
        returns.mean()
        *
        252
        /
        downside_std
    )




def calculate_calmar(portfolio):

    annual_return = (
        portfolio.annualized_return(
            freq="1D"
        )
    )


    max_dd = abs(
        portfolio.max_drawdown()
    )


    if max_dd == 0:
        return np.nan


    return annual_return / max_dd




def calculate_win_rate(portfolio):

    trades = (
        portfolio
        .trades
        .records_readable
    )


    if len(trades) == 0:
        return 0


    winning = (
        trades["PnL"] > 0
    ).sum()


    return winning / len(trades)




def generate_performance_report(portfolio):


    sharpe = portfolio.sharpe_ratio()


    if sharpe == float("inf") or sharpe == float("-inf"):

        sharpe = 0



    report = {

        "Total Return":
            portfolio.total_return(),


        "Annual Return":
            portfolio.annualized_return(),


        "Volatility":
            calculate_volatility(
                portfolio
            ),


        "Sharpe Ratio":
            sharpe,


        "Sortino Ratio":
            portfolio.sortino_ratio(),


        "Calmar Ratio":
            portfolio.calmar_ratio(),


        "Maximum Drawdown":
            portfolio.max_drawdown(),


        "Trades":
            portfolio.trades.count(),


        "Win Rate":
            portfolio.trades.win_rate()

    }


    return report