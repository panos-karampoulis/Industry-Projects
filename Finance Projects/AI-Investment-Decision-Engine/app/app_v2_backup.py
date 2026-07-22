import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)


# ==========================
# Page config
# ==========================

st.set_page_config(
    page_title="AI Investment Decision Engine",
    layout="wide"
)


# ==========================
# Title
# ==========================

st.title(
    "AI Investment Decision Engine"
)

st.caption(
    "Machine Learning based stock selection and portfolio analytics"
)


# ==========================
# Load Data
# ==========================

metrics = pd.read_csv(
    DATA_DIR / "performance_metrics.csv",
    index_col=0
)


equity = pd.read_csv(
    DATA_DIR / "equity_curves.csv",
    index_col=0,
    parse_dates=True
)


ml_signals = pd.read_csv(
    DATA_DIR / "ml_signals.csv"
)


feature_importance = pd.read_csv(
    DATA_DIR / "feature_importance.csv"
)


shap_df = pd.read_csv(
    DATA_DIR / "shap_values.csv"
)


# ==========================
# KPI Cards
# ==========================

st.subheader(
    "AI Portfolio Overview"
)


ai_metrics = metrics.loc[
    "AI Portfolio"
]


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Annual Return",
        f"{ai_metrics['Annual Return']:.2%}"
    )


with col2:

    st.metric(
        "Sharpe Ratio",
        f"{ai_metrics['Sharpe Ratio']:.2f}"
    )


with col3:

    st.metric(
        "Volatility",
        f"{ai_metrics['Annual Volatility']:.2%}"
    )


with col4:

    st.metric(
        "Maximum Drawdown",
        f"{ai_metrics['Maximum Drawdown']:.2%}"
    )


# ==========================
# Performance Table
# ==========================

st.subheader(
    "Portfolio Performance"
)


st.dataframe(
    metrics.style.format(
        "{:.2%}"
    ),
    use_container_width=True
)


# ==========================
# Equity Curve
# ==========================

st.subheader(
    "AI Portfolio vs SPY"
)


fig, ax = plt.subplots(
    figsize=(12,5)
)


ax.plot(
    equity.index,
    equity["AI Portfolio"],
    label="AI Portfolio"
)


ax.plot(
    equity.index,
    equity["SPY"],
    label="SPY"
)


ax.set_ylabel(
    "Growth of $1"
)


ax.legend()

ax.grid()


st.pyplot(fig)


# ==========================
# Drawdown
# ==========================

st.subheader(
    "Drawdown Comparison"
)


ai_dd = (
    equity["AI Portfolio"]
    /
    equity["AI Portfolio"].cummax()
) - 1


spy_dd = (
    equity["SPY"]
    /
    equity["SPY"].cummax()
) - 1


fig, ax = plt.subplots(
    figsize=(12,5)
)


ax.plot(
    ai_dd.index,
    ai_dd,
    label="AI Portfolio"
)


ax.plot(
    spy_dd.index,
    spy_dd,
    label="SPY"
)


ax.set_ylabel(
    "Drawdown"
)


ax.legend()

ax.grid()


st.pyplot(fig)



# ==========================
# ML Ranking
# ==========================

st.subheader(
    "ML Stock Ranking"
)


st.dataframe(
    ml_signals,
    use_container_width=True
)



# ==========================
# Feature Importance
# ==========================

st.subheader(
    "Feature Importance"
)


fi = (
    feature_importance
    .sort_values(
        "Importance",
        ascending=True
    )
)


fig, ax = plt.subplots(
    figsize=(10,6)
)


ax.barh(
    fi["Feature"],
    fi["Importance"]
)


ax.set_xlabel(
    "Importance"
)


ax.grid()


st.pyplot(fig)



# ==========================
# SHAP Explanation
# ==========================

st.subheader(
    "SHAP Model Explanation"
)


selected_stock = st.selectbox(
    "Select Stock",
    shap_df["symbol"].unique()
)


stock_shap = (
    shap_df[
        shap_df["symbol"] == selected_stock
    ]
    .drop(
        columns=["symbol"]
    )
    .T
)


stock_shap.columns = [
    "SHAP Value"
]


stock_shap = (
    stock_shap
    .sort_values(
        "SHAP Value"
    )
)


fig, ax = plt.subplots(
    figsize=(10,6)
)


ax.barh(
    stock_shap.index,
    stock_shap["SHAP Value"]
)


ax.set_title(
    f"Model explanation for {selected_stock}"
)


ax.grid()


st.pyplot(fig)


# ==========================
# Footer
# ==========================

st.divider()

st.write(
    "AI Investment Decision Engine | ML + Portfolio Analytics"
)