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
import pandas as pd
import matplotlib.pyplot as plt

from src.factor_backtest import calculate_factor_backtest
from src.performance import calculate_performance_metrics


st.set_page_config(
    page_title="Factor Investing Research",
    layout="wide"
)


st.title("📈 Factor Investing Research Dashboard")

st.markdown(
"""
Multi-factor equity research platform.

Factors:

- Momentum (12M return)
- Quality (ROE)
- Low Volatility

Portfolio:
- Top 20% stocks
- Monthly rebalance
"""
)


@st.cache_data
def load_data():

    prices = pd.read_csv(
        "data/raw/prices.csv",
        index_col=0,
        parse_dates=True
    )

    fundamentals = pd.read_csv(
        "data/raw/fundamentals.csv"
    )

    return prices, fundamentals



prices, fundamentals = load_data()



st.sidebar.header("Portfolio Settings")

weight_momentum = st.sidebar.slider(
    "Momentum Weight",
    0.0,
    1.0,
    0.4
)

weight_quality = st.sidebar.slider(
    "Quality Weight",
    0.0,
    1.0,
    0.3
)

weight_lowvol = st.sidebar.slider(
    "Low Volatility Weight",
    0.0,
    1.0,
    0.3
)



if st.sidebar.button("Run Backtest"):


    returns = calculate_factor_backtest(
        prices,
        fundamentals
    )


    metrics = calculate_performance_metrics(
        returns
    )


    st.subheader("Performance Metrics")

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Annual Return",
        f"{metrics.iloc[0,0]:.2%}"
    )

    col2.metric(
        "Sharpe Ratio",
        f"{metrics.iloc[0,1]:.2f}"
    )

    col3.metric(
        "Max Drawdown",
        f"{metrics.iloc[0,2]:.2%}"
    )



    st.subheader("Cumulative Returns")


    cumulative = (
        1 + returns
    ).cumprod()


    fig, ax = plt.subplots(
        figsize=(10,4)
    )

    ax.plot(
        cumulative.index,
        cumulative
    )

    ax.set_title(
        "Factor Portfolio Growth"
    )

    ax.set_ylabel(
        "Portfolio Value"
    )

    ax.grid(True)


    st.pyplot(fig)



    st.subheader("Monthly Returns Distribution")


    fig2, ax2 = plt.subplots(
        figsize=(8,3)
    )

    ax2.hist(
        returns.dropna(),
        bins=30
    )

    ax2.set_title(
        "Monthly Factor Returns"
    )


    st.pyplot(fig2)



    st.subheader("Return Statistics")

    st.dataframe(
        returns.describe()
    )