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

from src.factor_pipeline import run_factor_pipeline



import streamlit as st
import pandas as pd
import plotly.express as px


from src.factor_pipeline import run_factor_pipeline

from src.factor_exposure import (
    fama_french_exposure,
    rolling_beta
)

from src.factor_optimizer import (
    optimize_factor_weights
)



# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Factor Investing Lab",
    page_icon="📈",
    layout="wide"
)



st.title(
    "📈 Factor Investing Research Lab"
)


st.markdown(
    """
    Quantitative factor research dashboard

    Models:
    - Momentum
    - Value (HML)
    - Low Volatility
    - Fama-French Exposure
    """
)



# =====================================
# SIDEBAR
# =====================================


st.sidebar.header(
    "Research Controls"
)



start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime("2020-01-01")
)



end_date = st.sidebar.date_input(
    "End Date",
    pd.to_datetime("2025-01-01")
)



n_assets = st.sidebar.slider(
    "Assets per Factor",
    3,
    10,
    5
)



run = st.sidebar.button(
    "🚀 Run Analysis"
)



# =====================================
# UNIVERSE
# =====================================


tickers = [

    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "META",
    "GOOGL",
    "TSLA",
    "JPM",
    "BAC",
    "XOM",
    "CVX",
    "JNJ",
    "PFE",
    "KO",
    "PEP",
    "WMT",
    "COST",
    "V",
    "MA",
    "UNH",
    "HD",
    "NKE",
    "DIS",
    "SPY"

]



# =====================================
# RUN PIPELINE
# =====================================


if run:


    with st.spinner(
        "Running factor engine..."
    ):


        results = run_factor_pipeline(

            tickers,

            str(start_date),

            str(end_date),

            n_assets

        )


        st.session_state.results = results



# =====================================
# DASHBOARD
# =====================================


if "results" in st.session_state:


    results = st.session_state.results


    performance = results["performance"]

    portfolios = results["portfolios"]

    assets = results["assets"]

    returns = results["returns"]

    factors = results["factors"]



    # -----------------------------
    # PERFORMANCE TABLE
    # -----------------------------


    st.header(
        "📊 Factor Performance"
    )


    st.dataframe(
        performance,
        use_container_width=True
    )



    # -----------------------------
    # KPI
    # -----------------------------


    col1,col2,col3 = st.columns(3)



    best_return = performance.loc[
        performance["Annual Return"].idxmax()
    ]


    best_sharpe = performance.loc[
        performance["Sharpe Ratio"].idxmax()
    ]


    lowest_vol = performance.loc[
        performance["Annual Volatility"].idxmin()
    ]



    col1.metric(

        "Best Return",

        best_return["Portfolio"],

        f"{best_return['Annual Return']:.2%}"

    )



    col2.metric(

        "Best Sharpe",

        best_sharpe["Portfolio"],

        f"{best_sharpe['Sharpe Ratio']:.2f}"

    )



    col3.metric(

        "Lowest Volatility",

        lowest_vol["Portfolio"],

        f"{lowest_vol['Annual Volatility']:.2%}"

    )



    # -----------------------------
    # GROWTH
    # -----------------------------


    st.header(
        "📈 Portfolio Growth"
    )



    growth = pd.DataFrame()



    for name,ret in portfolios.items():

        growth[name] = (
            1+ret
        ).cumprod()



    fig_growth = px.line(

        growth,

        title="Growth of $1"

    )


    st.plotly_chart(

        fig_growth,

        use_container_width=True

    )



    # -----------------------------
    # RISK RETURN
    # -----------------------------


    st.header(
        "⚖️ Risk Return Profile"
    )



    fig_risk = px.scatter(

        performance,

        x="Annual Volatility",

        y="Annual Return",

        text="Portfolio",

        size="Sharpe Ratio",

        title="Risk / Return"

    )


    st.plotly_chart(

        fig_risk,

        use_container_width=True

    )



    # -----------------------------
    # SHARPE
    # -----------------------------


    st.header(
        "🏆 Sharpe Ranking"
    )


    fig_sharpe = px.bar(

        performance,

        x="Portfolio",

        y="Sharpe Ratio"

    )


    st.plotly_chart(

        fig_sharpe,

        use_container_width=True

    )



    # -----------------------------
    # FACTOR ASSETS
    # -----------------------------


    st.header(
        "🔬 Factor Constituents"
    )


    for factor,stocks in assets.items():

        st.subheader(
            factor
        )

        st.write(
            stocks
        )



    # =====================================
    # FACTOR EXPOSURE
    # =====================================


    st.header(
        "📐 Fama-French Factor Exposure"
    )



    selected_asset = st.selectbox(

        "Select Asset",

        returns.columns

    )



    exposure,model = fama_french_exposure(

        returns[selected_asset],

        factors

    )



    exposure_table = pd.DataFrame(

        exposure,

        index=["Value"]

    ).T



    st.dataframe(
        exposure_table
    )



    st.write(
        model.summary()
    )



    # =====================================
    # ROLLING BETA
    # =====================================


    st.header(
        "📉 Rolling Market Beta"
    )



    beta = rolling_beta(

        returns[selected_asset],

        returns["SPY"]

    )



    beta_df = pd.DataFrame({

        "Rolling Beta": beta

    })


    st.line_chart(
        beta_df
    )



    # =====================================
    # OPTIMIZER
    # =====================================


    st.header(
        "⚖️ Maximum Sharpe Factor Portfolio"
    )



    factor_returns = pd.DataFrame({

        "Momentum":
            portfolios["Momentum"],

        "Value":
            portfolios["Value"],

        "Low Volatility":
            portfolios["Low Volatility"]

    })



    weights,optimized_sharpe = optimize_factor_weights(

        factor_returns

    )



    st.dataframe(
        weights
    )



    st.metric(

        "Optimized Sharpe",

        round(
            optimized_sharpe,
            2
        )

    )



    # =====================================
    # DOWNLOAD
    # =====================================


    st.header(
        "⬇️ Export"
    )



    csv = performance.to_csv(
        index=False
    )


    st.download_button(

        "Download CSV",

        csv,

        "factor_performance.csv"

    )



else:


    st.info(
        "Press RUN ANALYSIS"
    )