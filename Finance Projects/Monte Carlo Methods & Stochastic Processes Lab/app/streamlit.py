import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)



import streamlit as st
import numpy as np
import pandas as pd



from src.brownian_motion import simulate_gbm


from src.monte_carlo import (
    european_call_mc,
    european_put_mc
)


from src.black_scholes import (
    black_scholes_call,
    black_scholes_put
)


from src.statistics import (
    confidence_interval,
    pricing_error
)


from src.plotting import (
    plot_gbm_paths,
    plot_terminal_distribution,
    plot_price_comparison
)



# -----------------------------
# CONFIG
# -----------------------------

st.set_page_config(

    page_title="Monte Carlo Pricing Lab",

    layout="wide"

)



st.title(
    "Monte Carlo Methods & Stochastic Processes Lab"
)


st.subheader(
    "European Option Pricing Dashboard"
)



# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header(
    "Model Parameters"
)



S0 = st.sidebar.number_input(

    "Initial Stock Price",

    value=100.0

)



K = st.sidebar.number_input(

    "Strike Price",

    value=100.0

)



r = st.sidebar.slider(

    "Risk Free Rate",

    0.0,

    0.20,

    0.05

)



sigma = st.sidebar.slider(

    "Volatility",

    0.05,

    1.0,

    0.20

)



T = st.sidebar.slider(

    "Time Horizon",

    0.1,

    5.0,

    1.0

)



simulations = st.sidebar.selectbox(

    "Simulations",

    [

        1000,

        5000,

        10000,

        50000

    ],

    index=2

)



option_type = st.sidebar.selectbox(

    "Option Type",

    [

        "European Call",

        "European Put"

    ]

)



run = st.sidebar.button(

    "Run Simulation"

)



# -----------------------------
# CACHE SIMULATION
# -----------------------------


@st.cache_data


def run_simulation(

    S0,

    r,

    sigma,

    T,

    simulations

):


    return simulate_gbm(

        S0=S0,

        mu=r,

        sigma=sigma,

        T=T,

        steps=252,

        simulations=simulations,

        seed=42

    )





# -----------------------------
# MAIN
# -----------------------------


if run:


    paths = run_simulation(

        S0,

        r,

        sigma,

        T,

        simulations

    )


    terminal_prices = paths[-1]



    # Pricing

    if option_type == "European Call":


        mc_price = european_call_mc(

            terminal_prices,

            K,

            r,

            T

        )


        bs_price = black_scholes_call(

            S0,

            K,

            r,

            sigma,

            T

        )


        payoff = np.maximum(

            terminal_prices-K,

            0

        )



    else:


        mc_price = european_put_mc(

            terminal_prices,

            K,

            r,

            T

        )


        bs_price = black_scholes_put(

            S0,

            K,

            r,

            sigma,

            T

        )


        payoff = np.maximum(

            K-terminal_prices,

            0

        )



    discounted_payoffs = (

        np.exp(-r*T)

        *

        payoff

    )



    mean, lower, upper = confidence_interval(

        discounted_payoffs

    )


    error = pricing_error(

        mc_price,

        bs_price

    )



    # -----------------------------
    # KPI CARDS
    # -----------------------------


    c1,c2,c3,c4 = st.columns(4)



    c1.metric(

        "Monte Carlo Price",

        f"${mc_price:.4f}"

    )



    c2.metric(

        "Black-Scholes",

        f"${bs_price:.4f}"

    )



    c3.metric(

        "Pricing Error",

        f"${error:.4f}"

    )



    c4.metric(

        "95% Confidence Interval",

        f"{lower:.2f}-{upper:.2f}"

    )



    st.divider()



    # -----------------------------
    # CHARTS
    # -----------------------------


    st.plotly_chart(

        plot_gbm_paths(paths),

        use_container_width=True

    )



    st.plotly_chart(

        plot_terminal_distribution(
            terminal_prices
        ),

        use_container_width=True

    )



    st.plotly_chart(

        plot_price_comparison(

            mc_price,

            bs_price

        ),

        use_container_width=True

    )



    # -----------------------------
    # TABLE
    # -----------------------------


    results = pd.DataFrame({

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

    })


    st.subheader(
        "Pricing Results"
    )


    st.dataframe(

        results,

        use_container_width=True

    )