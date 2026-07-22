import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

import sys
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(
    BASE_DIR
)



from src.spread import (
    estimate_hedge_ratio,
    calculate_spread,
    calculate_zscore
)

from src.signals import (
    generate_signals
)

from src.backtest import (
    calculate_strategy_returns
)


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Statistical Arbitrage Research Framework",
    layout="wide"
)


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data"
)


# -----------------------------
# Load data
# -----------------------------

@st.cache_data
def load_data():

    pair_results = pd.read_csv(
        os.path.join(
            DATA_PATH,
            "pair_backtest_results.csv"
        )
    )

    portfolio_results = pd.read_csv(
        os.path.join(
            DATA_PATH,
            "portfolio_results.csv"
        )
    )

    cost_analysis = pd.read_csv(
        os.path.join(
            DATA_PATH,
            "transaction_cost_analysis.csv"
        )
    )

    prices = pd.read_csv(
    os.path.join(
        DATA_PATH,
        "raw",
        "prices.csv"
        ),
    index_col=0,
    parse_dates=True
    )

    return (
    prices,
    pair_results,
    portfolio_results,
    cost_analysis
)


    


(
    prices,
    pair_results,
    portfolio_results,
    cost_analysis
) = load_data()


# -----------------------------
# Title
# -----------------------------

st.title(
    "Statistical Arbitrage Research Framework"
)

st.subheader(
    "Pairs Trading: Mean Reversion Research Dashboard"
)


# -----------------------------
# Overview metrics
# -----------------------------

st.header("Research Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Pairs Tested",
        "153"
    )


with col2:
    st.metric(
        "Cointegrated Pairs",
        "12"
    )


with col3:

    best_pair = (
        pair_results
        .sort_values(
            "Sharpe Ratio",
            ascending=False
        )
        .iloc[0]["Pair"]
    )

    st.metric(
        "Best Pair",
        best_pair
    )


with col4:

    sharpe = portfolio_results.iloc[0]["Sharpe Ratio"]

    st.metric(
        "Portfolio Sharpe",
        round(sharpe,3)
    )



# -----------------------------
# Pair Ranking
# -----------------------------

st.header(
    "Pair Backtest Ranking"
)


st.dataframe(
    pair_results.sort_values(
        "Sharpe Ratio",
        ascending=False
    ),
    use_container_width=True
)



# -----------------------------
# Best pairs chart
# -----------------------------

st.header(
    "Pair Performance"
)


fig, ax = plt.subplots(
    figsize=(10,4)
)


chart_data = (
    pair_results
    .sort_values(
        "Total Return",
        ascending=False
    )
)


ax.bar(
    chart_data["Pair"],
    chart_data["Total Return"]
)


plt.xticks(
    rotation=45
)


ax.set_ylabel(
    "Total Return"
)


ax.set_title(
    "Total Return by Pair"
)


st.pyplot(fig)



# -----------------------------
# Portfolio Results
# -----------------------------

st.header(
    "Portfolio Performance"
)


portfolio_results



col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Return",
        f"{portfolio_results.iloc[0]['Total Return']:.2%}"
    )


with col2:

    st.metric(
        "Sharpe",
        round(
            portfolio_results.iloc[0]['Sharpe Ratio'],
            3
        )
    )


with col3:

    st.metric(
        "Max Drawdown",
        f"{portfolio_results.iloc[0]['Max Drawdown']:.2%}"
    )



# -----------------------------
# Transaction Cost Analysis
# -----------------------------

st.header(
    "Transaction Cost Sensitivity"
)


st.dataframe(
    cost_analysis,
    use_container_width=True
)



fig2, ax2 = plt.subplots(
    figsize=(10,4)
)


ax2.plot(
    cost_analysis["Cost"],
    cost_analysis["Total Return"],
    marker="o"
)


ax2.set_xlabel(
    "Transaction Cost"
)


ax2.set_ylabel(
    "Total Return"
)


ax2.set_title(
    "Return Sensitivity to Trading Costs"
)


st.pyplot(fig2)



# -----------------------------
# Conclusion
# -----------------------------

st.header(
    "Research Conclusion"
)


st.write(
"""
The statistical arbitrage framework identifies
cointegrated equity pairs and evaluates their
mean-reversion characteristics.

Portfolio construction improves risk-adjusted
performance through diversification.

However, profitability is sensitive to transaction
cost assumptions, highlighting the importance of
realistic execution modelling.
"""
)


# -----------------------------
# Pair Explorer
# -----------------------------

st.header(
    "Pair Explorer"
)


# -----------------------------
# Sidebar Controls
# -----------------------------

st.sidebar.header(
    "Research Controls"
)


selected_pair = st.sidebar.selectbox(
    "Select Pair",
    pair_results["Pair"].tolist()
)


entry_threshold = st.sidebar.slider(
    "Entry Z-score Threshold",
    min_value=1.0,
    max_value=3.5,
    value=2.0,
    step=0.5
)


exit_threshold = st.sidebar.slider(
    "Exit Z-score Threshold",
    min_value=0.0,
    max_value=1.5,
    value=0.0,
    step=0.25
)


transaction_cost = st.sidebar.slider(
    "Transaction Cost",
    min_value=0.0,
    max_value=0.003,
    value=0.001,
    step=0.0005,
    format="%.4f"
)


stock_1, stock_2 = selected_pair.split("-")


series_y = prices[stock_1]

series_x = prices[stock_2]


alpha, beta = estimate_hedge_ratio(
    series_y,
    series_x
)


spread = calculate_spread(
    series_y,
    series_x,
    beta
)


zscore = calculate_zscore(
    spread
)


signals = generate_signals(
    zscore
)


returns = calculate_strategy_returns(
    series_y,
    series_x,
    beta,
    signals["Position"]
)


equity = (
    1 + returns
).cumprod()



st.subheader(
    "Spread"
)


fig, ax = plt.subplots(
    figsize=(10,4)
)

ax.plot(
    spread
)

ax.set_title(
    f"{selected_pair} Spread"
)

st.pyplot(fig)



st.subheader(
    "Z-Score Trading Signals"
)


fig, ax = plt.subplots(
    figsize=(10,4)
)


ax.plot(
    zscore,
    label="Z-score",
    color="black"
)


# Entry thresholds

ax.axhline(
    entry_threshold,
    linestyle="--",
    color="red",
    label="Short Entry"
)


ax.axhline(
    -entry_threshold,
    linestyle="--",
    color="green",
    label="Long Entry"
)


# Long entries

long_entries = zscore[
    zscore < -entry_threshold
]


ax.scatter(
    long_entries.index,
    long_entries.values,
    color="green",
    label="Long Entry"
)


# Short entries

short_entries = zscore[
    zscore > entry_threshold
]


ax.scatter(
    short_entries.index,
    short_entries.values,
    color="red",
    label="Short Entry"
)


# Exit zone

ax.axhline(
    0,
    linestyle=":",
    color="gray"
)


ax.set_title(
    f"{selected_pair} Z-score Signals"
)


ax.legend()


st.pyplot(fig)



st.subheader(
    "Equity Curve"
)


fig, ax = plt.subplots(
    figsize=(10,4)
)

ax.plot(
    equity
)

ax.set_title(
    f"{selected_pair} Strategy Equity Curve"
)

st.pyplot(fig)


# -----------------------------
# Drawdown
# -----------------------------

st.subheader(
    "Drawdown Analysis"
)


running_max = equity.cummax()


drawdown = (
    equity - running_max
) / running_max



fig, ax = plt.subplots(
    figsize=(10,4)
)


ax.plot(
    drawdown,
    color="red",
    label="Drawdown"
)


ax.axhline(
    0,
    color="black",
    linestyle="--"
)


ax.set_title(
    f"{selected_pair} Drawdown"
)


ax.set_ylabel(
    "Drawdown %"
)


ax.legend()


st.pyplot(fig)