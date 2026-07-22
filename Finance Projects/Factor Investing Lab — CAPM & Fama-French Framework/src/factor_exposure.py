import pandas as pd
import statsmodels.api as sm



def fama_french_exposure(
        asset_returns,
        factors
):

    data = pd.concat(
        [
            asset_returns,
            factors
        ],
        axis=1
    ).dropna()


    y = data.iloc[:,0]

    X = data[
        [
            "MKT_RF",
            "SMB",
            "HML"
        ]
    ]


    X = sm.add_constant(X)


    model = sm.OLS(
        y,
        X
    ).fit()


    results = {

        "Alpha":
            model.params["const"],

        "Market Beta":
            model.params["MKT_RF"],

        "SMB Beta":
            model.params["SMB"],

        "HML Beta":
            model.params["HML"],

        "R Squared":
            model.rsquared

    }


    return results, model



def rolling_beta(
        asset_returns,
        market_returns,
        window=252
):

    beta = (
        asset_returns
        .rolling(window)
        .cov(
            market_returns
        )
        /
        market_returns
        .rolling(window)
        .var()
    )


    return beta