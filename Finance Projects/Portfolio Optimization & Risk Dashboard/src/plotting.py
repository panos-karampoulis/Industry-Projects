import plotly.express as px
import plotly.graph_objects as go


def plot_efficient_frontier(
    frontier,
    portfolios
):

    fig = px.scatter(
        frontier,
        x="Volatility",
        y="Return",
        color="Sharpe",
        title="Efficient Frontier",
        labels={
            "Volatility": "Risk (Volatility)",
            "Return": "Expected Return"
        },
        width=1000,
        height=700
    )


    # Move Sharpe color bar
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Sharpe",
            x=1.05,
            len=0.6
        )
    )


    # Add portfolio markers
    for portfolio in portfolios:

        fig.add_trace(
            go.Scatter(
                x=[
                    portfolio["Volatility"]
                ],
                y=[
                    portfolio["Return"]
                ],
                mode="markers+text",
                marker=dict(
                    size=18
                ),
                text=[
                    portfolio["Portfolio"]
                ],
                textposition="top center",
                name=portfolio["Portfolio"]
            )
        )


    fig.update_layout(
        legend=dict(
            x=0.02,
            y=0.98
        ),
        margin=dict(
            l=60,
            r=120,
            t=80,
            b=60
        )
    )


    

    return fig


import plotly.graph_objects as go


def plot_cumulative_returns(
    cumulative_data
):
    """
    Plot portfolio growth.
    """

    fig = go.Figure()


    for column in cumulative_data.columns:

        fig.add_trace(
            go.Scatter(
                x=cumulative_data.index,
                y=cumulative_data[column],
                mode="lines",
                name=column
            )
        )


    fig.update_layout(
        title="Portfolio Growth",
        xaxis_title="Date",
        yaxis_title="Growth of $1",
        height=500
    )


    

    return fig


def plot_drawdown(
    drawdown_data
):
    """
    Plot portfolio drawdown.
    """

    fig = go.Figure()


    for column in drawdown_data.columns:

        fig.add_trace(
            go.Scatter(
                x=drawdown_data.index,
                y=drawdown_data[column],
                mode="lines",
                name=column
            )
        )


    fig.update_layout(
        title="Portfolio Drawdown",
        xaxis_title="Date",
        yaxis_title="Drawdown",
        height=500
    )


    

    return fig