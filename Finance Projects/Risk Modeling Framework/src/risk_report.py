import pandas as pd


def create_risk_report(
    historical95,
    historical99,
    parametric95,
    parametric99,
    monte_carlo95,
    monte_carlo99,
    es95,
    es99,
    portfolio_value
):

    report = pd.DataFrame({

        "Metric": [
            "Historical VaR",
            "Parametric VaR",
            "Monte Carlo VaR",
            "Expected Shortfall"
        ],

        "95%": [
            historical95,
            parametric95,
            monte_carlo95,
            es95
        ],

        "99%": [
            historical99,
            parametric99,
            monte_carlo99,
            es99
        ]

    })


    report["95% (€)"] = (
        report["95%"]
        *
        portfolio_value
    )


    report["99% (€)"] = (
        report["99%"]
        *
        portfolio_value
    )


    return report