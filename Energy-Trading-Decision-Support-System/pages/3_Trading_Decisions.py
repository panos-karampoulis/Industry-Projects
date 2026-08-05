# ==========================================================
# TRADING DECISIONS ANALYTICS
# Energy Trading Decision Support System
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Trading Decisions",

    page_icon="📈",

    layout="wide"

)



# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]


SAMPLE_DIR = (

    BASE_DIR
    /
    "data"
    /
    "demo"

)


RESULTS_DIR = (

    BASE_DIR
    /
    "results"

)



# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = {

    "Germany": "germany",

    "France": "france",

    "Italy": "italy",

    "Spain": "spain",

    "Netherlands": "netherlands"

}



# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title(

    "⚡ Energy Trading DSS"

)



country_display = st.sidebar.selectbox(

    "Select Country",

    list(COUNTRIES.keys())

)



country = COUNTRIES[country_display]



mode = st.sidebar.radio(

    "Data Mode",

    [

        "Sample",

        "Local"

    ]

)



# ==========================================================
# LOAD DATA
# ==========================================================


@st.cache_data
def load_trading_data(mode):


    if mode == "Sample":


        file = (

            SAMPLE_DIR

            /

            "trading_decisions_sample.csv"

        )


    else:


        file = (

            RESULTS_DIR

            /

            "trading_decisions_all_countries.csv"

        )



    if not file.exists():

        return None



    df = pd.read_csv(

        file

    )


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df





trade = load_trading_data(

    mode

)



if trade is None:


    st.error(

        "Trading decision dataset not found"

    )


    st.stop()



# ==========================================================
# FILTER COUNTRY
# ==========================================================


trade_country = trade[

    trade["country"] == country

].copy()



if trade_country.empty:


    st.warning(

        f"No trading data available for {country_display}"

    )


    st.stop()



trade_country = trade_country.sort_values(

    "timestamp"

)



# ==========================================================
# TITLE
# ==========================================================


st.title(

    "📈 Trading Decision Engine"

)



st.caption(

    f"{country_display} automated market decision signals"

)



# ==========================================================
# KPI
# ==========================================================


latest = trade_country.iloc[-1]



col1,col2,col3,col4,col5 = st.columns(5)



with col1:

    st.metric(

        "Trading Signal",

        latest["trading_signal"]

    )



with col2:

    st.metric(

        "Confidence",

        f"{latest['confidence']:.2f}%"

    )



with col3:

    st.metric(

        "Risk Level",

        latest["risk_level"]

    )



with col4:

    st.metric(

        "Risk Score",

        f"{latest['risk_score']:.2f}"

    )



with col5:

    st.metric(

        "Day Ahead Price",

        f"{latest['day_ahead_price']:.2f} €/MWh"

    )



st.divider()



# ==========================================================
# SIGNAL DISTRIBUTION
# ==========================================================


st.subheader(

    "Trading Signal Distribution"

)



fig_signal = px.histogram(

    trade_country,

    x="trading_signal",

    category_orders={

        "trading_signal":

        [

            "BUY",

            "HOLD",

            "SELL"

        ]

    },

    title="BUY / HOLD / SELL Signals"

)



st.plotly_chart(

    fig_signal,

    use_container_width=True

)



# ==========================================================
# SIGNAL EVOLUTION
# ==========================================================


st.subheader(

    "Trading Signal Evolution"

)



signal_map = {

    "SELL": -1,

    "HOLD": 0,

    "BUY": 1

}



trade_country["signal_numeric"] = (

    trade_country["trading_signal"]

    .map(signal_map)

)



fig_evolution = px.line(

    trade_country.tail(1000),

    x="timestamp",

    y="signal_numeric",

    title="Signal Movement Over Time"

)



st.plotly_chart(

    fig_evolution,

    use_container_width=True

)



# ==========================================================
# CONFIDENCE
# ==========================================================


st.subheader(

    "Decision Confidence"

)



fig_conf = px.line(

    trade_country.tail(1000),

    x="timestamp",

    y="confidence",

    title="Model Confidence"

)



st.plotly_chart(

    fig_conf,

    use_container_width=True

)



# ==========================================================
# PRICE VS SIGNAL
# ==========================================================


st.subheader(

    "Price vs Trading Signal"

)



fig_price = px.scatter(

    trade_country.tail(2000),

    x="day_ahead_price",

    y="confidence",

    color="trading_signal",

    title="Market Price and Decision Confidence"

)



st.plotly_chart(

    fig_price,

    use_container_width=True

)



# ==========================================================
# RECOMMENDATION
# ==========================================================


signal = latest["trading_signal"]



if signal == "BUY":

    color = "green"


elif signal == "SELL":

    color = "red"


else:

    color = "orange"



st.markdown(

f"""

<h2 style='color:{color}'>

Recommendation: {signal}

</h2>


Confidence:

<b>{latest['confidence']:.2f}%</b>


<br><br>


Risk Level:

<b>{latest['risk_level']}</b>

""",

unsafe_allow_html=True

)
