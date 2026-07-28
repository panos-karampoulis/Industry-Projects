# ============================================================
# Intraday Forecast Dashboard
# European Electricity Market Forecasting Engine
# ============================================================

import os
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Intraday Forecast",
    page_icon="⚡",
    layout="wide"
)



# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]


FORECAST_DIR = (
    BASE_DIR
    /
    "data"
    /
    "forecasts"
    /
    "intraday"
)



# ============================================================
# CONFIG
# ============================================================

COUNTRIES = {

    "Germany 🇩🇪": "germany",

    "France 🇫🇷": "france",

    "Italy 🇮🇹": "italy",

    "Netherlands 🇳🇱": "netherlands",

    "Spain 🇪🇸": "spain"

}



# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_forecast(country):


    file = (
        FORECAST_DIR
        /
        f"{country}_intraday_forecast.csv"
    )


    if not file.exists():

        return None



    df = pd.read_csv(
        file
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )


    return df



# ============================================================
# TITLE
# ============================================================


st.title(
    "⚡ Intraday Electricity Price Forecast"
)


st.markdown(
"""
### Next 24 Hours Electricity Price Forecast

Forecast resolution:

**15 minutes**

Model:

**XGBoost Machine Learning Forecasting Engine**

"""
)



# ============================================================
# SIDEBAR
# ============================================================


st.sidebar.header(
    "Market Selection"
)


selected = st.sidebar.selectbox(

    "Select Country",

    list(COUNTRIES.keys())

)



country = COUNTRIES[selected]



# ============================================================
# LOAD
# ============================================================


df = load_forecast(
    country
)



if df is None:


    st.error(
        "Forecast file not found"
    )

    st.stop()



# ============================================================
# KPI
# ============================================================


col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(

        "Country",

        selected

    )



with col2:

    st.metric(

        "Forecast Points",

        len(df)

    )



with col3:

    st.metric(

        "Average Forecast",

        f"{df['forecast_price'].mean():.2f} €/MWh"

    )



with col4:

    st.metric(

        "Max Price",

        f"{df['forecast_price'].max():.2f} €/MWh"

    )



# ============================================================
# CHART
# ============================================================


st.divider()


st.subheader(
    "24 Hour Price Forecast"
)



fig = px.line(

    df,

    x="timestamp",

    y="forecast_price",

    markers=True,

    title=f"{selected} Intraday Forecast"

)



fig.update_layout(

    xaxis_title="Time",

    yaxis_title="Price €/MWh",

    hovermode="x unified"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ============================================================
# TABLE
# ============================================================


st.divider()


st.subheader(
    "Forecast Details"
)



display_df = df.copy()


display_df["timestamp"] = (

    display_df["timestamp"]

    .dt.strftime(
        "%Y-%m-%d %H:%M"
    )

)



st.dataframe(

    display_df,

    use_container_width=True

)



# ============================================================
# DOWNLOAD
# ============================================================


csv = df.to_csv(
    index=False
)



st.download_button(

    label="Download Forecast CSV",

    data=csv,

    file_name=f"{country}_intraday_forecast.csv",

    mime="text/csv"

)