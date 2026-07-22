import pandas as pd


def worst_loss_days(
    portfolio_returns,
    portfolio_value=100000,
    n_days=10
):
    """
    Returns the worst historical loss days
    """

    losses = (
        portfolio_returns
        .sort_values()
        .head(n_days)
    )


    report = pd.DataFrame({

        "Return": losses,

        "Loss (€)": (
            losses *
            portfolio_value
        )

    })


    return report