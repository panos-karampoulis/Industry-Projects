import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from pathlib import Path


from src.data import load_prices

from src.optimization import (
    portfolio_return,
    portfolio_volatility,
    minimum_variance_portfolio,
    maximum_sharpe_portfolio,
    risk_parity_portfolio
)

from src.efficient_frontier import (
    generate_random_portfolios
)

from src.performance import (
    portfolio_risk_metrics
)

from src.risk import (
    portfolio_returns
)

from src.plotting import (
    plot_efficient_frontier,
    plot_cumulative_returns,
    plot_drawdown
)



# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Portfolio Optimization Dashboard",
    layout="wide"
)


st.title(
    "Portfolio Optimization & Risk Dashboard"
)


st.markdown(
    """
    Compare portfolio construction methods:

    - Equal Weight
    - Minimum Variance
    - Maximum Sharpe
    - Risk Parity
    """
)



# ==========================
# SIDEBAR
# ==========================

st.sidebar.header(
    "Model Parameters"
)


risk_free_rate = st.sidebar.slider(
    "Risk Free Rate",
    min_value=0.0,
    max_value=0.10,
    value=0.02,
    step=0.005
)


n_simulations = st.sidebar.slider(
    "Efficient Frontier Simulations",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=1000
)


run_model = st.sidebar.button(
    "Run Optimization"
)



# ==========================
# LOAD DATA
# ==========================


@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent


    price_path = (
        BASE_DIR
        /
        "data"
        /
        "raw"
        /
        "prices.csv"
    )


    return load_prices(
        price_path
    )



# ==========================
# RUN MODEL
# ==========================


if run_model:


    prices = load_data()


    returns = (
        prices
        .pct_change()
        .dropna()
    )


    expected_returns = (
        returns.mean()
        *
        252
    )


    covariance = (
        returns.cov()
        *
        252
    )


    n_assets = len(
        expected_returns
    )


    equal_weights = np.array(
        [1/n_assets] * n_assets
    )


    min_var_weights = np.array(
        minimum_variance_portfolio(
            covariance
        )
    )


    max_sharpe_weights = np.array(
        maximum_sharpe_portfolio(
            expected_returns,
            covariance
        )
    )


    risk_parity_weights = np.array(
        risk_parity_portfolio(
            covariance
        )
    )



    portfolios = {


        "Equal Weight":
            equal_weights,


        "Minimum Variance":
            min_var_weights,


        "Maximum Sharpe":
            max_sharpe_weights,


        "Risk Parity":
            risk_parity_weights

    }



    frontier = generate_random_portfolios(

        expected_returns,

        covariance,

        n_portfolios=n_simulations,

        risk_free_rate=risk_free_rate

    )



    # Save everything

    st.session_state["prices"] = prices

    st.session_state["returns"] = returns

    st.session_state["expected_returns"] = expected_returns

    st.session_state["covariance"] = covariance

    st.session_state["portfolios"] = portfolios

    st.session_state["frontier"] = frontier


    st.session_state["parameters"] = {

        "risk_free_rate": risk_free_rate,

        "n_simulations": n_simulations

    }



# ==========================
# DISPLAY ONLY IF RESULTS EXIST
# ==========================


if "returns" in st.session_state:


    params = st.session_state["parameters"]


    if (
        params["risk_free_rate"] == risk_free_rate
        and
        params["n_simulations"] == n_simulations
    ):


        prices = st.session_state["prices"]

        returns = st.session_state["returns"]

        expected_returns = st.session_state["expected_returns"]

        covariance = st.session_state["covariance"]

        portfolios = st.session_state["portfolios"]

        frontier = st.session_state["frontier"]



        st.caption(

            f"""
            Report Parameters:
            Risk Free Rate = {risk_free_rate:.2%}
            |
            Frontier Simulations = {n_simulations}
            """

        )



        # ======================
        # PERFORMANCE TABLE
        # ======================


        st.subheader(
            "Portfolio Performance Comparison"
        )


        results = []


        for name, weights in portfolios.items():


            results.append(

                portfolio_risk_metrics(

                    name,

                    returns,

                    weights,

                    expected_returns,

                    covariance

                )

            )


        risk_summary = pd.DataFrame(
            results
        )


        st.dataframe(
            risk_summary,
            use_container_width=True
        )


        # ======================
        # DOWNLOAD RESULTS
        # ======================

        csv = risk_summary.to_csv(
            index=False
        )


        st.download_button(

            label="📥 Download Portfolio Results CSV",

            data=csv,

            file_name="portfolio_results.csv",

            mime="text/csv"

        )

        # ======================
        # DOWNLOAD WEIGHTS
        # ======================


        weights_df = pd.DataFrame(
            portfolios["Maximum Sharpe"],
            index=prices.columns,
            columns=["Weight"]
        )


        weights_csv = weights_df.to_csv()


        st.download_button(

            label="📥 Download Maximum Sharpe Weights",

            data=weights_csv,

            file_name="maximum_sharpe_weights.csv",

            mime="text/csv"

        )



        # ======================
        # KPI CARDS
        # ======================


        best_portfolio = (
            risk_summary
            .sort_values(
                "Sharpe Ratio",
                ascending=False
            )
            .iloc[0]
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)



        with col1:

            st.metric(

             label="🏆 Best Portfolio",

            value=best_portfolio["Portfolio"]

         )



        with col2:

            st.metric(

                label="📈 Annual Return",

                value=f"{best_portfolio['Annual Return']:.2%}"

            )



            with col3:

                st.metric(

                    label="📊 Sharpe Ratio",

                    value=f"{best_portfolio['Sharpe Ratio']:.2f}"

                )



            with col4:

                st.metric(

                    label="📉 Maximum Drawdown",

                    value=f"{best_portfolio['Max Drawdown']:.2%}"

                )


        # ======================
        # EFFICIENT FRONTIER
        # ======================

        st.divider()
        st.subheader(
            "Efficient Frontier"
        )


        points = []


        for name, weights in portfolios.items():


            points.append(

                {

                "Portfolio": name,


                "Return":
                    portfolio_return(
                        weights,
                        expected_returns
                    ),


                "Volatility":
                    portfolio_volatility(
                        weights,
                        covariance
                    )

                }

            )


        frontier_fig = plot_efficient_frontier(
            frontier,
            points
        )


        st.plotly_chart(
            frontier_fig,
            use_container_width=True
        )



        # ======================
        # GROWTH
        # ======================


        st.subheader(
            "Portfolio Growth"
        )


        daily_returns = {}


        for name, weights in portfolios.items():


            daily_returns[name] = portfolio_returns(

                returns,

                weights

            )


        daily_returns = pd.DataFrame(
            daily_returns
        )


        cumulative = (

            1 + daily_returns

        ).cumprod()



        st.plotly_chart(

            plot_cumulative_returns(
                cumulative
            ),

            use_container_width=True

        )



        # ======================
        # DRAWDOWN
        # ======================


        st.subheader(
            "Portfolio Drawdown"
        )


        drawdown = (

            cumulative /

            cumulative.cummax()

        ) - 1



        st.plotly_chart(

            plot_drawdown(
                drawdown
            ),

            use_container_width=True

        )



        # ======================
        # ALLOCATION
        # ======================


        st.subheader(
            "Maximum Sharpe Allocation"
        )


        weights = portfolios[
            "Maximum Sharpe"
        ]


        allocation = pd.DataFrame(

            {

            "Ticker": prices.columns,

            "Weight": weights

            }

        )


        allocation = allocation[
            allocation["Weight"] > 0.001
        ]



        pie = px.pie(

            allocation,

            names="Ticker",

            values="Weight",

            title="Maximum Sharpe Portfolio Weights"

        )


        st.plotly_chart(

            pie,

            use_container_width=True

        )



    else:


        st.warning(

            "Parameters changed. Press Run Optimization again."

        )


else:


    st.info(

        "Select parameters and press Run Optimization."

    )