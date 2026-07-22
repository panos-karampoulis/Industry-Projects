import statsmodels.api as sm



def capm_regression(
    asset_returns,
    market_returns,
    risk_free=0
):

    """

    CAPM:

    Ri-Rf =
    alpha +
    beta(Rm-Rf)

    """


    excess_asset = (
        asset_returns -
        risk_free
    )


    excess_market = (
        market_returns -
        risk_free
    )


    X = sm.add_constant(
        excess_market
    )


    model = sm.OLS(
        excess_asset,
        X
    ).fit()


    alpha = model.params.iloc[0]

    beta = model.params.iloc[1]


    return {

        "Alpha": alpha,

        "Beta": beta,

        "R_squared":
            model.rsquared,

        "p_value":
            model.pvalues.iloc[1],

        "model":
            model
    }