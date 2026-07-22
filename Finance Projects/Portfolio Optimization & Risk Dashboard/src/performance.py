import pandas as pd

from src.optimization import (
    portfolio_return,
    portfolio_volatility,
    portfolio_sharpe
)


def portfolio_metrics(
    name,
    weights,
    expected_returns,
    covariance,
    risk_free_rate=0.02
):
    """
    Calculate portfolio performance metrics.
    """

    from src.optimization import (
        portfolio_return,
        portfolio_volatility,
        portfolio_sharpe
    )


    return {
        "Portfolio": name,
        "Annual Return": portfolio_return(
            weights,
            expected_returns
        ),
        "Volatility": portfolio_volatility(
            weights,
            covariance
        ),
        "Sharpe Ratio": portfolio_sharpe(
            weights,
            expected_returns,
            covariance,
            risk_free_rate
        )
    }



def create_comparison_table(results):
    """
    Convert results list into dataframe.
    """

    return pd.DataFrame(results)


def portfolio_risk_metrics(
    name,
    returns,
    weights,
    expected_returns,
    covariance
):

    from src.risk import (
        portfolio_returns,
        cumulative_returns,
        maximum_drawdown
    )


    daily_returns = portfolio_returns(
        returns,
        weights
    )


    cumulative = cumulative_returns(
        daily_returns
    )


    return {
        "Portfolio": name,
        "Annual Return": portfolio_return(
            weights,
            expected_returns
        ),
        "Volatility": portfolio_volatility(
            weights,
            covariance
        ),
        "Sharpe Ratio": portfolio_sharpe(
            weights,
            expected_returns,
            covariance
        ),
        "Max Drawdown": maximum_drawdown(
            cumulative
        )
    }