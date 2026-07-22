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
import numpy as np
import yfinance as yf
import joblib
import shap
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime


# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="SPY ML Trading Dashboard",
    page_icon="📈",
    layout="wide"
)


# ======================================================
# TITLE
# ======================================================

st.title("📈 SPY Machine Learning Trading Dashboard")

st.markdown(
"""
This dashboard presents predictions from the final
XGBoost + SMA200 regime strategy.

Model purpose:

- Market regime detection
- Direction probability estimation
- Risk management overlay

"""
)


# ======================================================
# LOAD MODEL
# ======================================================

@st.cache_resource
def load_model():

    model = joblib.load(
        "xgboost_spy_model.pkl"
    )

    return model


try:

    model = load_model()

except Exception as e:

    st.error(
        "Model file not found: xgboost_spy_model.pkl"
    )

    st.stop()



# ======================================================
# DATA DOWNLOAD
# ======================================================


@st.cache_data(ttl=3600)
def download_data():

    data = yf.download(
        "SPY",
        period="5y",
        interval="1d"
    )


    data.columns = data.columns.get_level_values(0)


    return data



if st.sidebar.button(
    "🔄 Refresh Data"
):

    st.cache_data.clear()



df = download_data()



# ======================================================
# FEATURE ENGINEERING
# ======================================================


def create_features(df):


    data = df.copy()


    data["Return"] = (
        data["Close"]
        .pct_change()
    )


    data["SMA50"] = (
        data["Close"]
        .rolling(50)
        .mean()
    )


    data["SMA100"] = (
        data["Close"]
        .rolling(100)
        .mean()
    )


    data["SMA200"] = (
        data["Close"]
        .rolling(200)
        .mean()
    )


    data["SMA50_SMA200"] = (
        data["SMA50"]
        -
        data["SMA200"]
    )


    data["Price_SMA200_Distance"] = (
        data["Close"]
        /
        data["SMA200"]
        -
        1
    )


    # Bollinger

    mid = (
        data["Close"]
        .rolling(20)
        .mean()
    )


    std = (
        data["Close"]
        .rolling(20)
        .std()
    )


    data["BB_Lower"] = (
        mid - 2*std
    )


    data["BB_Upper"] = (
        mid + 2*std
    )


    data["Volatility"] = (
        data["Return"]
        .rolling(20)
        .std()
    )


    data["Momentum20"] = (
        data["Close"]
        /
        data["Close"]
        .shift(20)
        -
        1
    )


    data["Volume_Change"] = (
        data["Volume"]
        .pct_change()
    )


    data = data.dropna()


    return data



features = create_features(df)



# ======================================================
# MODEL INPUT
# ======================================================


# Features used by final model

model_features = [

"SMA50",
"SMA100",
"SMA200",
"SMA50_SMA200",
"Price_SMA200_Distance",
"BB_Lower",
"BB_Upper",
"Volatility",
"Momentum20",
"Volume_Change"

]



X_latest = (
    features[
        model_features
    ]
    .tail(1)
)



# ======================================================
# PREDICTION
# ======================================================


st.sidebar.header(
    "Model Controls"
)


threshold = st.sidebar.slider(
    "BUY Threshold",
    0.1,
    0.9,
    0.5,
    0.05
)



if st.button(
    "🚀 Generate Prediction"
):


    probability = (
        model
        .predict_proba(
            X_latest
        )[0][1]
    )


    regime = (
        features["Close"].iloc[-1]
        >
        features["SMA200"].iloc[-1]
    )


    if (
        probability > threshold
        and regime
    ):

        signal="BUY"


    elif probability > threshold:

        signal="WAIT"


    else:

        signal="HOLD"



    # Save in session

    st.session_state["probability"] = probability
    st.session_state["signal"] = signal
    st.session_state["regime"] = regime




# ======================================================
# DISPLAY PREDICTION
# ======================================================


if "probability" in st.session_state:


    col1,col2,col3 = st.columns(3)


    col1.metric(
        "BUY Probability",
        f"{st.session_state['probability']:.2%}"
    )


    col2.metric(
        "Signal",
        st.session_state["signal"]
    )


    col3.metric(
        "SMA200 Regime",
        "Bullish"
        if st.session_state["regime"]
        else
        "Bearish"
    )



# ======================================================
# PRICE CHART
# ======================================================


st.subheader(
    "SPY Price & Trend"
)



fig = go.Figure()



fig.add_trace(
    go.Scatter(
        x=features.index,
        y=features["Close"],
        name="SPY"
    )
)



fig.add_trace(
    go.Scatter(
        x=features.index,
        y=features["SMA200"],
        name="SMA200"
    )
)



st.plotly_chart(
    fig,
    use_container_width=True
)



# ======================================================
# LATEST DATA TABLE
# ======================================================


st.subheader(
    "Latest Market Data"
)



st.dataframe(
    features.tail(10)
)



# ======================================================
# SHAP
# ======================================================


st.subheader(
    "Model Explainability"
)



try:


    explainer = shap.TreeExplainer(
        model
    )


    shap_values = (
        explainer
        .shap_values(
            X_latest
        )
    )


    shap_df = pd.DataFrame(
        {
            "Feature":
            model_features,

            "Impact":
            shap_values[0]
        }
    )


    shap_df = (
        shap_df
        .sort_values(
            "Impact"
        )
    )


    fig2 = go.Figure(
        go.Bar(
            x=shap_df["Impact"],
            y=shap_df["Feature"],
            orientation="h"
        )
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


except:

    st.info(
        "SHAP visualization unavailable"
    )



# ======================================================
# FOOTER
# ======================================================


st.markdown(
"""
---
### Disclaimer

This project is for research and educational purposes only.
It does not constitute financial advice.

"""
)