import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def plot_gbm_paths(paths, simulations=50):

    fig = go.Figure()


    for i in range(min(simulations, paths.shape[1])):

        fig.add_trace(
            go.Scatter(
                y=paths[:, i],
                mode="lines",
                opacity=0.35,
                showlegend=False
            )
        )


    fig.update_layout(
        title="Geometric Brownian Motion Paths",
        xaxis_title="Time Steps",
        yaxis_title="Asset Price",
        template="plotly_white",
        height=500
    )


    return fig




def plot_terminal_distribution(terminal_prices):

    df = pd.DataFrame(
        {
            "Terminal Price": terminal_prices
        }
    )


    fig = px.histogram(
        df,
        x="Terminal Price",
        nbins=60,
        title="Terminal Price Distribution"
    )


    fig.update_layout(
        template="plotly_white",
        height=450
    )


    return fig




def plot_price_comparison(mc_price, bs_price):

    df = pd.DataFrame(
        {
            "Model":
            [
                "Monte Carlo",
                "Black-Scholes"
            ],

            "Price":
            [
                mc_price,
                bs_price
            ]
        }
    )


    fig = px.bar(
        df,
        x="Model",
        y="Price",
        text="Price",
        title="Option Pricing Comparison"
    )


    fig.update_layout(
        template="plotly_white",
        height=400
    )


    return fig