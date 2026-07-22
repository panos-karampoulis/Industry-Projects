import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



def plot_equity_curve(
        portfolio,
        title="Equity Curve"
):

    equity = portfolio.value()



    plt.figure(
        figsize=(12,5)
    )


    plt.plot(
        equity.index,
        equity
    )


    plt.title(title)

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "Portfolio Value"
    )

    plt.grid()

    plt.show()



def plot_drawdown(
        portfolio,
        title="Drawdown"
):

    drawdown = portfolio.drawdown()

    plt.figure(
        figsize=(12,5)
    )

    plt.plot(
        drawdown.index,
        drawdown.values
    )

    plt.title(
        title
    )

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "Drawdown"
    )

    plt.grid()

    plt.show()





def plot_strategy_comparison(
        performance_df
):


    plt.figure(
        figsize=(10,6)
    )


    performance_df["Return"].plot(
        kind="bar"
    )


    plt.title(
        "Strategy Return Comparison"
    )


    plt.ylabel(
        "Total Return"
    )


    plt.grid()

    plt.show()





def plot_correlation_heatmap(
        returns
):


    corr = (
        returns
        .corr()
    )


    plt.figure(
        figsize=(8,6)
    )


    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm"
    )


    plt.title(
        "Strategy Correlation Matrix"
    )


    plt.show()





def plot_contribution(
        contribution
):


    plt.figure(
        figsize=(8,5)
    )


    contribution.plot(
        kind="bar"
    )


    plt.title(
        "Return Contribution"
    )


    plt.ylabel(
        "Contribution"
    )


    plt.grid()

    plt.show()