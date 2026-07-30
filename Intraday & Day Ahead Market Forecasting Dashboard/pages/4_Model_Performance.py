import os
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Model Performance",

    page_icon="📊",

    layout="wide"

)



# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]


DEMO_DIR = (

    BASE_DIR

    /

    "demo_data"

)


BACKTEST_DIR = (

    DEMO_DIR

    /

    "backtesting"

)


FEATURE_DIR = (

    DEMO_DIR

    /

    "feature_importance"

)



INTRADAY_FILE = (

    BACKTEST_DIR

    /

    "intraday_backtest_results.csv"

)



DAY_AHEAD_FILE = (

    BACKTEST_DIR

    /

    "day_ahead_backtest_results.csv"

)



# ============================================================
# TITLE
# ============================================================


st.title(

    "📊 Electricity Forecast Model Performance"

)



st.markdown(
"""
Machine Learning model monitoring dashboard.

Includes:

- Forecast accuracy
- Error analysis
- Model comparison
- Feature importance
"""
)



# ============================================================
# LOAD DATA
# ============================================================


@st.cache_data

def load_data(path):


    df = pd.read_csv(path)


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df



# ============================================================
# SIDEBAR
# ============================================================


st.sidebar.header(

    "⚡ Controls"

)



forecast_type = st.sidebar.selectbox(

    "Forecast Type",

    [

        "Intraday",

        "Day Ahead"

    ]

)



if forecast_type == "Intraday":

    DATA_FILE = INTRADAY_FILE

else:

    DATA_FILE = DAY_AHEAD_FILE



if not DATA_FILE.exists():

    st.error(

        f"Missing file:\n{DATA_FILE}"

    )

    st.stop()



df = load_data(DATA_FILE)



countries = sorted(

    df["country"]

    .unique()

)



country = st.sidebar.selectbox(

    "Country",

    countries

)



df = df[

    df["country"]

    ==

    country

].copy()



# ============================================================
# DETECT COLUMNS
# ============================================================


actual_col = None

forecast_col = None



for col in df.columns:


    name = col.lower()



    if "actual" in name:

        actual_col = col



    if "forecast" in name:

        forecast_col = col



if actual_col is None or forecast_col is None:


    st.error(

        "Actual / Forecast columns not found"

    )


    st.write(df.columns)

    st.stop()



# ============================================================
# ERROR CALCULATION
# ============================================================


df["error"] = (

    df[forecast_col]

    -

    df[actual_col]

)



df["absolute_error"] = (

    df["error"]

    .abs()

)



df["percentage_error"] = (

    df["absolute_error"]

    /

    df[actual_col]

    .replace(0,np.nan)

) * 100



# ============================================================
# KPI CARDS
# ============================================================


st.header(

    f"📈 {country.upper()} {forecast_type} Performance"

)



mae = df["absolute_error"].mean()


rmse = np.sqrt(

    (

        df["error"]

        **2

    ).mean()

)


mape = df["percentage_error"].mean()



c1,c2,c3,c4 = st.columns(4)



c1.metric(

    "MAE",

    f"{mae:.2f}"

)


c2.metric(

    "RMSE",

    f"{rmse:.2f}"

)


c3.metric(

    "MAPE",

    f"{mape:.2f}%"

)


c4.metric(

    "Observations",

    f"{len(df):,}"

)



st.divider()



# ============================================================
# ACTUAL VS FORECAST
# ============================================================


st.subheader(

    "📈 Actual vs Forecast"

)



fig = px.line(

    df,

    x="timestamp",

    y=[

        actual_col,

        forecast_col

    ],

    title=(

        f"{country.upper()} Actual vs Forecast"

    )

)



fig.update_layout(

    height=450

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ============================================================
# ERROR OVER TIME
# ============================================================


st.subheader(

    "📉 Forecast Error Over Time"

)



fig_error = px.line(

    df,

    x="timestamp",

    y="error"

)



fig_error.add_hline(

    y=0

)



fig_error.update_layout(

    height=400

)



st.plotly_chart(

    fig_error,

    use_container_width=True

)



# ============================================================
# ERROR DISTRIBUTION
# ============================================================


st.subheader(

    "📊 Error Distribution"

)



fig_hist = px.histogram(

    df,

    x="error",

    nbins=60

)



fig_hist.update_layout(

    height=400

)



st.plotly_chart(

    fig_hist,

    use_container_width=True

)



# ============================================================
# BIGGEST ERRORS
# ============================================================


st.divider()



st.subheader(

    "🚨 Largest Forecast Errors"

)



largest = (

    df

    .sort_values(

        "absolute_error",

        ascending=False

    )

    .head(20)

)



st.dataframe(

    largest,

    use_container_width=True

)



# ============================================================
# FEATURE IMPORTANCE
# ============================================================


st.divider()



st.subheader(

    "🤖 Feature Importance"

)



feature_file = None



for file in FEATURE_DIR.glob("*.csv"):


    if forecast_type.lower() in file.name.lower():

        feature_file = file



if feature_file is None:


    for file in FEATURE_DIR.glob("*.csv"):

        feature_file = file

        break



if feature_file and feature_file.exists():


    importance = pd.read_csv(

        feature_file

    )



    importance = importance.sort_values(

        "Importance",

        ascending=False

    ).head(15)



    fig_imp = px.bar(

        importance,

        x="Importance",

        y="Feature",

        orientation="h",

        title="Top Model Features"

    )



    fig_imp.update_layout(

        height=500

    )



    st.plotly_chart(

        fig_imp,

        use_container_width=True

    )


else:


    st.info(

        "Feature importance demo file not available"

    )



# ============================================================
# SUMMARY TABLE
# ============================================================


st.divider()



st.subheader(

    "📋 Performance Summary"

)



summary = pd.DataFrame(

    {

        "Metric":

        [

            "MAE",

            "RMSE",

            "MAPE",

            "Observations"

        ],


        "Value":

        [

            round(mae,3),

            round(rmse,3),

            round(mape,3),

            len(df)

        ]

    }

)



st.table(summary)



st.success(

    "Model Performance Analysis Completed"

)