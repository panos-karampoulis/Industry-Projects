import pandas as pd


def stress_test(
    portfolio_value,
    scenarios=None
):

    """
    Portfolio stress testing scenarios
    """


    if scenarios is None:

        scenarios = {

            "Market Correction -10%": -0.10,

            "Severe Crash -20%": -0.20,

            "Financial Crisis -30%": -0.30,

            "Volatility Shock +50%": -0.50

        }


    results = []


    for name, shock in scenarios.items():

        loss = (
            portfolio_value *
            shock
        )


        results.append({

            "Scenario": name,

            "Shock": shock,

            "Portfolio Impact (€)": loss

        })


    return pd.DataFrame(results)