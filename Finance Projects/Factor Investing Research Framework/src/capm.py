import statsmodels.api as sm
import pandas as pd


def capm_regression(
    portfolio_returns,
    market_returns
):

    excess_market = market_returns

    X = sm.add_constant(
        excess_market
    )


    model = sm.OLS(
        portfolio_returns,
        X
    ).fit()


    results = pd.DataFrame({
        "Alpha":[model.params.iloc[0]],
        "Beta":[model.params.iloc[1]],
        "R_squared":[model.rsquared],
        "P_value":[model.pvalues.iloc[0]]
    })


    return results