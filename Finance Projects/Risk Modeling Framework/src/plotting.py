import plotly.graph_objects as go
import plotly.express as px



def plot_return_distribution(
    portfolio_returns,
    var=None,
    es=None
):

    fig = px.histogram(
        portfolio_returns,
        nbins=80,
        title="Portfolio Return Distribution"
    )


    if var:

        fig.add_vline(
            x=-var,
            line_dash="dash",
            annotation_text=f"VaR {var:.2%}",
            annotation_position="top left"
        )


    if es:

        fig.add_vline(
            x=-es,
            line_dash="dot",
            annotation_text=f"ES {es:.2%}",
            annotation_position="top right"
        )


    fig.update_layout(
        height=500,
        xaxis_title="Daily Return",
        yaxis_title="Frequency"
    )


    return fig




def plot_cumulative_returns(
    portfolio_returns
):

    cumulative = (
        1 + portfolio_returns
    ).cumprod()


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            y=cumulative,
            mode="lines",
            name="Portfolio"
        )
    )


    fig.update_layout(
        height=500,
        title="Portfolio Growth"
    )


    return fig


def plot_drawdown(
    portfolio_returns
):

    cumulative = (
        1 + portfolio_returns
    ).cumprod()


    peak = cumulative.cummax()


    drawdown = (
        cumulative - peak
    ) / peak


    fig = go.Figure()


    fig.add_trace(

        go.Scatter(

            x=drawdown.index,

            y=drawdown,

            mode="lines",

            fill="tozeroy",

            name="Drawdown"

        )

    )


    fig.update_layout(

        title="Portfolio Drawdown",

        height=500,

        xaxis_title="Date",

        yaxis_title="Drawdown %",

        yaxis_tickformat=".1%"

    )


    return fig
