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

    page_title="Backtesting Analytics",

    page_icon="📉",

    layout="wide"

)



# ============================================================
# PATHS
# ============================================================


BASE_DIR = Path(

    r"D:\Portfolio\Intraday Market Forecasting - updated"

)



BACKTEST_DIR = (

    BASE_DIR

    /

    "data"

    /

    "backtesting"

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

    "📉 Forecast Backtesting Analytics"

)



st.markdown(
"""
Model validation dashboard.

Evaluates:

- Forecast accuracy
- Model stability
- Forecast bias
- Market performance
"""
)



# ============================================================
# LOAD DATA
# ============================================================


@st.cache_data

def load_file(path):


    df = pd.read_csv(

        path

    )


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df





# ============================================================
# SELECT ENGINE
# ============================================================


st.sidebar.header(

    "Backtesting Settings"

)



engine = st.sidebar.selectbox(

    "Forecast Engine",

    [

        "Intraday",

        "Day Ahead"

    ]

)



if engine == "Intraday":


    FILE = INTRADAY_FILE


else:


    FILE = DAY_AHEAD_FILE





if not FILE.exists():


    st.error(

        f"Missing file:\n{FILE}"

    )


    st.stop()



df = load_file(

    FILE

)



# ============================================================
# COUNTRY FILTER
# ============================================================


countries = sorted(

    df["country"]

    .unique()

)



country = st.sidebar.selectbox(

    "Country",

    countries

)



df_country = df[

    df["country"]

    ==

    country

].copy()



# ============================================================
# ERROR METRICS
# ============================================================


actual = [

    c for c in df.columns

    if "actual" in c.lower()

][0]



forecast = [

    c for c in df.columns

    if "forecast" in c.lower()

][0]




df_country["error"] = (

    df_country[forecast]

    -

    df_country[actual]

)



df_country["abs_error"] = (

    df_country["error"]

    .abs()

)



df_country["squared_error"] = (

    df_country["error"]

    **2

)



mae = df_country["abs_error"].mean()


rmse = np.sqrt(

    df_country["squared_error"]

    .mean()

)


bias = df_country["error"].mean()



mape = (

    (

        df_country["abs_error"]

        /

        df_country[actual]

        .replace(0,np.nan)

    )

    .mean()

    *

    100

)



# ============================================================
# KPI
# ============================================================


st.header(

    f"📊 {country.upper()} Backtest Results"

)



c1,c2,c3,c4 = st.columns(4)



with c1:

    st.metric(

        "MAE",

        f"{mae:.2f}"

    )


with c2:

    st.metric(

        "RMSE",

        f"{rmse:.2f}"

    )


with c3:

    st.metric(

        "MAPE",

        f"{mape:.2f}%"

    )


with c4:

    st.metric(

        "Bias",

        f"{bias:.2f}"

    )



# ============================================================
# ERROR TREND
# ============================================================


st.divider()


st.subheader(

    "📉 Forecast Error Trend"

)



fig = px.line(

    df_country,

    x="timestamp",

    y="error",

    title="Forecast Error Over Time"

)



fig.add_hline(

    y=0

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ============================================================
# ROLLING PERFORMANCE
# ============================================================


st.subheader(

    "📈 Rolling MAE"

)



df_country["rolling_mae"] = (

    df_country["abs_error"]

    .rolling(

        96

    )

    .mean()

)



fig_roll = px.line(

    df_country,

    x="timestamp",

    y="rolling_mae",

    title="24 Hour Rolling MAE"

)



st.plotly_chart(

    fig_roll,

    use_container_width=True

)



# ============================================================
# COUNTRY RANKING
# ============================================================


st.divider()


st.subheader(

    "🌍 European Forecast Accuracy Ranking"

)



ranking = (

    df

    .copy()

)



ranking["error"] = (

    ranking[forecast]

    -

    ranking[actual]

)



ranking["absolute_error"] = (

    ranking["error"]

    .abs()

)



ranking_table = (

    ranking

    .groupby(

        "country"

    )

    .agg(

        MAE=(

            "absolute_error",

            "mean"

        ),

        RMSE=(

            "error",

            lambda x:

            np.sqrt(

                (x**2).mean()

            )

        )

    )

    .reset_index()

    .sort_values(

        "MAE"

    )

)



st.dataframe(

    ranking_table.round(3),

    use_container_width=True

)



fig_rank = px.bar(

    ranking_table,

    x="country",

    y="MAE",

    title="Forecast Accuracy Ranking (Lower is Better)"

)



st.plotly_chart(

    fig_rank,

    use_container_width=True

)



# ============================================================
# WORST PERIODS
# ============================================================


st.divider()


st.subheader(

    "🚨 Worst Forecast Periods"

)



worst = (

    df_country

    .sort_values(

        "abs_error",

        ascending=False

    )

    .head(20)

)



st.dataframe(

    worst,

    use_container_width=True

)



st.success(

    "Backtesting Analytics Completed"

)