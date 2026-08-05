# ==========================================================
# MARKET COMPARISON DASHBOARD
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

    page_title="Market Comparison",

    page_icon="🌍",

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
    "sample"
)


FEATURES_DIR = (
    BASE_DIR
    /
    "data"
    /
    "features"
)


RESULTS_DIR = (
    BASE_DIR
    /
    "results"
)



COUNTRIES = [

    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"

]



COUNTRY_NAMES = {

    "germany": "Germany",

    "france": "France",

    "italy": "Italy",

    "spain": "Spain",

    "netherlands": "Netherlands"

}



# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title(
    "⚡ Energy Trading DSS"
)


mode = st.sidebar.radio(

    "Data Mode",

    [
        "Sample",
        "Local"
    ]

)



# ==========================================================
# LOADERS
# ==========================================================


@st.cache_data
def load_features(country, mode):


    if mode == "Sample":

        file = (

            SAMPLE_DIR

            /

            f"{country}_features_sample.csv"

        )


    else:

        file = (

            FEATURES_DIR

            /

            f"{country}_features.csv"

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





@st.cache_data
def load_risk(mode):


    if mode == "Sample":

        file = (

            SAMPLE_DIR

            /

            "imbalance_risk_sample.csv"

        )


    else:

        file = (

            RESULTS_DIR

            /

            "all_countries_imbalance_risk.csv"

        )



    if not file.exists():

        return None



    df = pd.read_csv(

        file

    )


    return df





@st.cache_data
def load_trade(mode):


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



    return pd.read_csv(

        file

    )




# ==========================================================
# BUILD MARKET DATASET
# ==========================================================


market = []



for country in COUNTRIES:


    df = load_features(

        country,

        mode

    )


    if df is not None and len(df) > 0:


        latest = df.iloc[-1]


        market.append(

            {

                "country":

                    COUNTRY_NAMES[country],

                "price":

                    latest["day_ahead_price"],

                "load_gw":

                    latest["load_mw"]/1000,

                "renewable_share":

                    latest["renewable_share"]

            }

        )



market_df = pd.DataFrame(

    market

)



if market_df.empty:

    st.error(
        "No market data found"
    )

    st.stop()



# ==========================================================
# TITLE
# ==========================================================


st.title(

    "🌍 European Energy Market Comparison"

)



st.caption(

    "Cross-country electricity market analytics"

)



# ==========================================================
# KPI TABLE
# ==========================================================


st.subheader(

    "Market Snapshot"

)



st.dataframe(

    market_df,

    use_container_width=True

)



# ==========================================================
# PRICE COMPARISON
# ==========================================================


st.subheader(

    "Day Ahead Price Comparison"

)



fig_price = px.bar(

    market_df,

    x="country",

    y="price",

    title="Current Electricity Prices €/MWh"

)



st.plotly_chart(

    fig_price,

    use_container_width=True

)



# ==========================================================
# LOAD COMPARISON
# ==========================================================


st.subheader(

    "System Load Comparison"

)



fig_load = px.bar(

    market_df,

    x="country",

    y="load_gw",

    title="Current Electricity Demand GW"

)



st.plotly_chart(

    fig_load,

    use_container_width=True

)



# ==========================================================
# RENEWABLE SHARE
# ==========================================================


st.subheader(

    "Renewable Penetration"

)



fig_renew = px.bar(

    market_df,

    x="country",

    y="renewable_share",

    title="Renewable Generation Share %"

)



st.plotly_chart(

    fig_renew,

    use_container_width=True

)



# ==========================================================
# RISK COMPARISON
# ==========================================================


risk = load_risk(

    mode

)



if risk is not None:


    risk_summary = (

        risk

        .groupby("country")

        ["risk_score"]

        .mean()

        .reset_index()

    )


    risk_summary["country"] = (

        risk_summary["country"]

        .map(COUNTRY_NAMES)

    )


    st.subheader(

        "Average Imbalance Risk"

    )


    fig_risk = px.bar(

        risk_summary,

        x="country",

        y="risk_score",

        title="Average Risk Score"

    )


    st.plotly_chart(

        fig_risk,

        use_container_width=True

    )



# ==========================================================
# TRADING SIGNALS
# ==========================================================


trade = load_trade(

    mode

)



if trade is not None:


    signals = (

        trade

        .groupby(

            [

                "country",

                "trading_signal"

            ]

        )

        .size()

        .reset_index(

            name="count"

        )

    )


    signals["country"] = (

        signals["country"]

        .map(COUNTRY_NAMES)

    )



    st.subheader(

        "Trading Signal Distribution"

    )



    fig_signal = px.bar(

        signals,

        x="country",

        y="count",

        color="trading_signal",

        title="BUY / HOLD / SELL Signals"

    )


    st.plotly_chart(

        fig_signal,

        use_container_width=True

    )