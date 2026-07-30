# ============================================================
# European Electricity Market Forecasting Engine
# Main Dashboard
# ============================================================

import os
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="European Energy Forecasting Engine",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


DATA_DIR = BASE_DIR / "data"


FORECAST_DIR = (
    DATA_DIR
    /
    "forecasts"
)


BACKTEST_DIR = (
    DATA_DIR
    /
    "backtesting"
)


REFRESH_FILE = (
    DATA_DIR
    /
    "last_refresh.txt"
)



# ============================================================
# LOAD FUNCTIONS
# ============================================================

@st.cache_data
def load_intraday_features():

    possible_files = [

        # Local real data
        DATA_DIR
        /
        "processed"
        /
        "europe_intraday_weather_features.csv",


        # Streamlit demo data
        BASE_DIR
        /
        "demo_data"
        /
        "features"
        /
        "europe_intraday_weather_features.csv"

    ]


    file = None


    for path in possible_files:

        if path.exists():

            file = path
            break


    if file is None:

        return None


    df = pd.read_csv(
        file
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )


    return df



@st.cache_data
def load_backtest():

    possible_files = [

        # Local path
        DATA_DIR
        /
        "backtesting"
        /
        "intraday_backtest_results.csv",


        # Streamlit Cloud demo path
        BASE_DIR
        /
        "demo_data"
        /
        "backtesting"
        /
        "intraday_backtest_results.csv"

    ]


    file = None


    for path in possible_files:

        if path.exists():

            file = path
            break


    if file is None:

        return None


    df = pd.read_csv(
        file
    )


    return df


def get_last_refresh():

    if REFRESH_FILE.exists():

        with open(
            REFRESH_FILE,
            "r"
        ) as f:

            return f.read()

    return "No refresh available"



# ============================================================
# TITLE
# ============================================================

st.title(
    "⚡ European Electricity Market Forecasting Engine"
)


st.markdown(
"""
## AI-driven Energy Market Analytics Platform

Machine Learning forecasting system for European electricity markets.

Covered markets:

🇩🇪 Germany  
🇫🇷 France  
🇮🇹 Italy  
🇳🇱 Netherlands  
🇪🇸 Spain  


Models:

- XGBoost
- Random Forest


Forecast horizons:

- Intraday Forecast → 24 hours (15 min resolution)
- Day Ahead Forecast → D+1 / D+7 / 30 Days

"""
)



# ============================================================
# LOAD DATA
# ============================================================

features = load_intraday_features()

backtest = load_backtest()



# ============================================================
# KPI SECTION
# ============================================================


st.divider()


st.subheader(
    "System Overview"
)



col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(
        "Markets",
        "5 Countries"
    )


with col2:

    st.metric(
        "Resolution",
        "15 Minutes"
    )


with col3:

    st.metric(
        "Forecast Models",
        "XGBoost + RF"
    )


with col4:

    st.metric(
        "Intraday Horizon",
        "24 Hours"
    )



# ============================================================
# DATA STATUS
# ============================================================


st.divider()


st.subheader(
    "Data Status"
)



col1, col2 = st.columns(2)



with col1:

    st.info(
        f"""
        Last Data Refresh:

        {get_last_refresh()}
        """
    )


with col2:

    if features is not None:

        latest = (
            features["timestamp"]
            .max()
        )

        st.success(
            f"""
            Latest Market Data:

            {latest}
            """
        )

    else:

        st.warning(
            "Feature dataset not found"
        )



# ============================================================
# MARKET SNAPSHOT
# ============================================================


if features is not None:


    st.divider()


    st.subheader(
        "Latest Market Snapshot"
    )


    latest_rows = (
        features
        .sort_values(
            "timestamp"
        )
        .groupby(
            "country"
        )
        .tail(1)
    )


    fig = px.bar(
        latest_rows,
        x="country",
        y="price_eur_mwh",
        title="Latest Electricity Prices (€/MWh)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ============================================================
# BACKTEST SUMMARY
# ============================================================


if backtest is not None:


    st.divider()


    st.subheader(
        "Intraday Model Performance"
    )


    mae = (
        backtest["absolute_error"]
        .mean()
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Average MAE",
            f"{mae:.2f} €/MWh"
        )


    with col2:

        st.metric(
            "Forecast Records",
            f"{len(backtest):,}"
        )



# ============================================================
# FOOTER
# ============================================================


st.divider()


st.caption(
"""
European Energy Forecasting Engine  
Built with Python, XGBoost, Pandas, Streamlit & ENTSO-E market data.
"""
)