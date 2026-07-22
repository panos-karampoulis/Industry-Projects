import statsmodels.api as sm



def fama_french_regression(
    asset_returns,
    factors
):


    data = asset_returns.to_frame(
        "Asset"
    )


    data = data.join(
        factors,
        how="inner"
    )


    data["Excess_Return"] = (
        data["Asset"]
        -
        data["RF"]
    )


    X = data[
        [
            "MKT_RF",
            "SMB",
            "HML"
        ]
    ]


    X = sm.add_constant(
        X
    )


    y = data[
        "Excess_Return"
    ]


    model = sm.OLS(
        y,
        X
    ).fit()



    return {

        "Alpha":
            model.params["const"],

        "Market Beta":
            model.params["MKT_RF"],

        "SMB Beta":
            model.params["SMB"],

        "HML Beta":
            model.params["HML"],

        "R_squared":
            model.rsquared,

        "model":
            model
    }