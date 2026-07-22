import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="AI Investment Decision Engine",
    layout="wide"
)


st.title(
    "AI Investment Decision Engine"
)


st.subheader(
    "Portfolio Performance"
)


# Load data

metrics = pd.read_csv(
    "data/processed/performance_metrics.csv",
    index_col=0
)


equity = pd.read_csv(
    "data/processed/equity_curves.csv",
    index_col=0,
    parse_dates=True
)


ai_returns = pd.read_csv(
    "data/processed/ai_returns.csv",
    index_col=0,
    parse_dates=True
)


spy_returns = pd.read_csv(
    "data/processed/spy_returns.csv",
    index_col=0,
    parse_dates=True
)


# Metrics table

st.dataframe(
    metrics,
    use_container_width=True
)


# Equity curve

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


# Drawdown

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


# -------------------------
# ML Ranking
# -------------------------

st.subheader(
    "ML Stock Ranking"
)


ml_signals = pd.read_csv(
    "data/processed/ml_signals.csv"
)


st.dataframe(
    ml_signals,
    use_container_width=True
)


# -------------------------
# Feature Importance
# -------------------------

st.subheader(
    "Feature Importance"
)


feature_importance = pd.read_csv(
    "data/processed/feature_importance.csv"
)


feature_importance = (
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
    feature_importance["Feature"],
    feature_importance["Importance"]
)


ax.set_xlabel(
    "Importance"
)


ax.set_title(
    "Model Feature Importance"
)


ax.grid()


st.pyplot(fig)

# -------------------------
# SHAP Explanation
# -------------------------

st.subheader(
    "SHAP Model Explanation"
)


shap_df = pd.read_csv(
    "data/processed/shap_values.csv"
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
    f"Why the model selected {selected_stock}"
)


ax.set_xlabel(
    "SHAP Contribution"
)


ax.grid()


st.pyplot(fig)