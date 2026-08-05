# ==========================================================
# ENERGY TRADING DECISION SUPPORT SYSTEM
# STREAMLIT DASHBOARD v3
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

import subprocess
import sys

from pathlib import Path
from datetime import datetime



# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent


FEATURE_DIR = (
    BASE_DIR
    /
    "data"
    /
    "features"
)


PRICE_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


RESULT_DIR = (
    BASE_DIR
    /
    "results"
)



PIPELINE = [
    sys.executable,
    "src/pipeline/run_pipeline.py"
]



COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]



# ==========================================================
# PAGE
# ==========================================================

st.set_page_config(
    page_title="Energy Trading DSS",
    page_icon="⚡",
    layout="wide"
)



# ==========================================================
# LOAD FUNCTIONS
# ==========================================================


@st.cache_data
def load_features(country):

    file = (
        FEATURE_DIR
        /
        f"{country}_features.csv"
    )


    df = pd.read_csv(file)


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    return df




@st.cache_data
def load_prices(country, market):


    if market == "Day Ahead":

        file = (
            PRICE_DIR
            /
            f"{country}_day_ahead_prices.csv"
        )

    else:

        file = (
            PRICE_DIR
            /
            f"{country}_intraday_prices.csv"
        )


    df = pd.read_csv(file)


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.rename(
        columns={
            "price_eur_mwh": market
        }
    )


    return df[
        [
            "timestamp",
            market
        ]
    ]





@st.cache_data
def load_risk(country):

    file = (
        RESULT_DIR
        /
        f"{country}_imbalance_risk.csv"
    )


    if not file.exists():

        return pd.DataFrame()


    df = pd.read_csv(file)


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    return df





@st.cache_data
def load_signals():


    file = (
        RESULT_DIR
        /
        "trading_decisions_all_countries.csv"
    )


    df = pd.read_csv(file)


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    return df





# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(
    "⚡ Energy Trading DSS"
)



country = st.sidebar.selectbox(

    "Country",

    COUNTRIES

)



market_type = st.sidebar.selectbox(

    "Price Market",

    [
        "Day Ahead",
        "Intraday"
    ]

)



st.sidebar.divider()



if st.sidebar.button(
    "🔄 Refresh Pipeline"
):


    with st.spinner(
        "Running complete pipeline..."
    ):


        result = subprocess.run(

            PIPELINE,

            cwd=BASE_DIR

        )


        if result.returncode == 0:


            st.success(
                "Pipeline completed"
            )

            st.cache_data.clear()

            st.rerun()


        else:

            st.error(
                "Pipeline failed"
            )




# ==========================================================
# LOAD DATA
# ==========================================================


features = load_features(
    country
)



prices = load_prices(
    country,
    market_type
)



risk = load_risk(
    country
)



signals = load_signals()



# ==========================================================
# MERGE
# ==========================================================


market = features.copy()



# keep historical day ahead from features

market = market.merge(

    prices,

    on="timestamp",

    how="left"

)



# ==========================================================
# DATE SELECTOR
# ==========================================================


min_date = (
    market["timestamp"]
    .min()
    .date()
)



max_date = (
    market["timestamp"]
    .max()
    .date()
)



selected_date = st.sidebar.date_input(

    "Select Date",

    value=max_date,

    min_value=min_date,

    max_value=max_date

)



market_day = market[

    market["timestamp"]
    .dt.date
    ==
    selected_date

]



if market_day.empty:

    market_day = market.tail(96)



signal_day = signals[

    (signals["country"]==country)
    &
    (signals["timestamp"].dt.date==selected_date)

]



latest = market_day.iloc[-1]



if not signal_day.empty:

    latest_signal = signal_day.iloc[-1]

else:

    latest_signal = {

        "trading_signal":"N/A",

        "confidence":0,

        "risk_score":0

    }



# ==========================================================
# TITLE
# ==========================================================


st.title(
    "⚡ Energy Trading Decision Support System"
)


st.caption(
"""
Day Ahead & Intraday Market Analysis |
Load Forecasting |
Renewable Generation |
Imbalance Risk |
Trading Signals
"""
)



# ==========================================================
# KPI
# ==========================================================


c1,c2,c3,c4,c5 = st.columns(5)



with c1:

    st.metric(

        "Day Ahead Price",

        f"{latest['day_ahead_price']:.2f} €/MWh"

    )



with c2:

    st.metric(

        market_type,

        f"{latest.get(market_type,0):.2f} €/MWh"

    )



with c3:

    st.metric(

        "Load",

        f"{latest['load_mw']:.0f} MW"

    )



with c4:

    st.metric(

        "Renewable Share",

        f"{latest['renewable_share']:.1%}"

    )



with c5:

    st.metric(

        "Trading Signal",

        latest_signal["trading_signal"]

    )



st.divider()



# ==========================================================
# PRICE
# ==========================================================


st.subheader(
"📈 Market Price"
)



fig = px.line(

    market_day,

    x="timestamp",

    y=[
        "day_ahead_price",
        market_type
    ],

    title="Energy Prices"

)



st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================================================
# LOAD
# ==========================================================


st.subheader(
"⚡ System Fundamentals"
)



c1,c2 = st.columns(2)



with c1:


    fig = px.line(

        market_day,

        x="timestamp",

        y="load_mw",

        title="Electricity Load"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )




with c2:


    fig = px.area(

        market_day,

        x="timestamp",

        y=[
            "wind_generation",
            "solar_generation",
            "renewable_generation"
        ],

        title="Renewable Generation"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ==========================================================
# RISK
# ==========================================================


st.subheader(
"⚠️ Imbalance Risk"
)



if not risk.empty:


    risk_day = risk[

        risk["timestamp"].dt.date
        ==
        selected_date

    ]


    fig = px.line(

        risk_day,

        x="timestamp",

        y="risk_score",

        title="Risk Score"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# ==========================================================
# SIGNALS
# ==========================================================


st.subheader(
"💹 Trading Decision Engine"
)



if not signals.empty:


    country_signals = signals[

        signals["country"]
        ==
        country

    ]


    fig = px.pie(

        country_signals,

        names="trading_signal",

        title="Signal Distribution"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )




# ==========================================================
# FINAL
# ==========================================================


st.divider()



signal = latest_signal["trading_signal"]



if signal=="BUY":

    color="green"

elif signal=="SELL":

    color="red"

else:

    color="orange"



st.markdown(

f"""

<h2 style="color:{color}">

Recommendation: {signal}

</h2>


Confidence:

{latest_signal.get("confidence",0):.1f}%


<br><br>


Risk Score:

{latest_signal.get("risk_score",0):.2f}


""",

unsafe_allow_html=True

)



st.caption(

f"""

Dashboard refresh:

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

"""

)