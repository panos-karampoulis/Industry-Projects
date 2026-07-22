import numpy as np



def expected_shortfall(
    portfolio_returns,
    confidence=0.95
):
    """
    Historical Expected Shortfall
    """

    var = np.percentile(
        portfolio_returns,
        (1-confidence)*100
    )


    losses = portfolio_returns[
        portfolio_returns <= var
    ]


    es = -losses.mean()


    return es



def expected_shortfall_amount(
    portfolio_returns,
    portfolio_value,
    confidence=0.95
):

    es = expected_shortfall(
        portfolio_returns,
        confidence
    )

    return es * portfolio_value