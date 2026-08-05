# ==========================================================
# PAGE 7
# TRADE ANALYTICS
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path



# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]


RESULT_DIR = (
    BASE_DIR /
    "results"
)


BACKTEST_FILE = (
    RESULT_DIR /
    "backtest_results.csv"
)



# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(

    page_title="Trade Analytics",

    page_icon="📈",

    layout="wide"

)



# ==========================================================
# LOAD
# ==========================================================


@st.cache_data
def load_data():


    df = pd.read_csv(

        BACKTEST_FILE

    )


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df





df = load_data()



# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(
    "📈 Trade Analytics"
)



countries = sorted(

    df["country"]

    .unique()

)



country = st.sidebar.selectbox(

    "Country",

    [
        "All"
    ]
    +
    countries

)



if country != "All":

    data = df[

        df.country == country

    ].copy()


else:

    data = df.copy()





# ==========================================================
# TITLE
# ==========================================================


st.title(

    "📈 Trading Strategy Analytics"

)


st.caption(

"""
Detailed analysis of trading signals,
risk levels and PnL behaviour.
"""

)



# ==========================================================
# KPI
# ==========================================================


c1,c2,c3,c4 = st.columns(4)



with c1:

    st.metric(

        "Total PnL",

        f"{data.hourly_pnl.sum():,.2f} €"

    )



with c2:

    st.metric(

        "Trades",

        int(
            data.position_change.abs().sum()
        )

    )



with c3:

    st.metric(

        "Average Trade PnL",

        f"{data.hourly_pnl.mean():.2f} €"

    )



with c4:

    win_rate = (

        (
            data.hourly_pnl > 0
        )

        .mean()

        *

        100

    )


    st.metric(

        "Win Rate",

        f"{win_rate:.2f}%"

    )





st.divider()



# ==========================================================
# SIGNAL PERFORMANCE
# ==========================================================


st.subheader(

    "🎯 PnL by Trading Signal"

)



signal_pnl = (

    data

    .groupby(

        "trading_signal"

    )

    ["hourly_pnl"]

    .sum()

    .reset_index()

)



fig = px.bar(

    signal_pnl,

    x="trading_signal",

    y="hourly_pnl",

    color="trading_signal",

    title="Profit Contribution by Signal"

)



st.plotly_chart(

    fig,

    use_container_width=True

)





# ==========================================================
# RISK PERFORMANCE
# ==========================================================


st.subheader(

    "⚠️ PnL by Risk Level"

)



if "risk_level" in data.columns:


    risk_pnl = (

        data

        .groupby(

            "risk_level"

        )

        ["hourly_pnl"]

        .sum()

        .reset_index()

    )


    fig = px.bar(

        risk_pnl,

        x="risk_level",

        y="hourly_pnl",

        color="risk_level",

        title="Performance by Risk Category"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )





# ==========================================================
# HOURLY PERFORMANCE
# ==========================================================


st.subheader(

    "⏰ Trading Performance by Hour"

)



data["hour"] = (

    data.timestamp.dt.hour

)



hour_perf = (

    data

    .groupby(

        "hour"

    )

    ["hourly_pnl"]

    .sum()

    .reset_index()

)



fig = px.bar(

    hour_perf,

    x="hour",

    y="hourly_pnl",

    title="PnL Distribution by Hour"

)



st.plotly_chart(

    fig,

    use_container_width=True

)





# ==========================================================
# BEST / WORST HOURS
# ==========================================================


col1,col2 = st.columns(2)



with col1:


    st.subheader(

        "🏆 Best Trading Hours"

    )


    best = (

        hour_perf

        .sort_values(

            "hourly_pnl",

            ascending=False

        )

        .head(5)

    )


    st.dataframe(

        best,

        hide_index=True

    )





with col2:


    st.subheader(

        "📉 Worst Trading Hours"

    )


    worst = (

        hour_perf

        .sort_values(

            "hourly_pnl",

            ascending=True

        )

        .head(5)

    )


    st.dataframe(

        worst,

        hide_index=True

    )





# ==========================================================
# COUNTRY COMPARISON
# ==========================================================


if country == "All":


    st.divider()


    st.subheader(

        "🌍 Country PnL Comparison"

    )


    country_perf = (

        data

        .groupby(

            "country"

        )

        ["hourly_pnl"]

        .sum()

        .reset_index()

    )


    fig = px.bar(

        country_perf,

        x="country",

        y="hourly_pnl",

        color="country",

        title="Total PnL by Country"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )