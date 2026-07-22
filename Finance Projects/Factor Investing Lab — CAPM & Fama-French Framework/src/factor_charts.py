import matplotlib.pyplot as plt



def cumulative_returns_chart(
    portfolios
):

    fig, ax = plt.subplots(
        figsize=(10,5)
    )


    for name, returns in portfolios.items():

        cumulative = (
            1 + returns
        ).cumprod()


        ax.plot(
            cumulative.index,
            cumulative,
            label=name
        )


    ax.set_title(
        "Factor Portfolio Growth"
    )

    ax.set_ylabel(
        "Growth of $1"
    )

    ax.legend()

    ax.grid(True)

    plt.close(fig)
    return fig



def risk_return_scatter(
    factor_table
):

    fig, ax = plt.subplots(
        figsize=(8,5)
    )


    ax.scatter(
        factor_table["Annual Volatility"],
        factor_table["Annual Return"]
    )


    for i,row in factor_table.iterrows():

        ax.annotate(
            row["Portfolio"],
            (
                row["Annual Volatility"],
                row["Annual Return"]
            )
        )


    ax.set_xlabel(
        "Volatility"
    )

    ax.set_ylabel(
        "Return"
    )


    ax.set_title(
        "Risk Return Profile"
    )


    ax.grid(True)

    plt.close(fig)
    return fig



def sharpe_bar_chart(
    factor_table
):

    fig, ax = plt.subplots(
        figsize=(8,5)
    )


    ax.bar(
        factor_table["Portfolio"],
        factor_table["Sharpe Ratio"]
    )


    ax.set_title(
        "Sharpe Ratio Comparison"
    )


    ax.set_ylabel(
        "Sharpe"
    )


    ax.tick_params(
        axis="x",
        rotation=45
    )

    plt.close(fig)
    return fig