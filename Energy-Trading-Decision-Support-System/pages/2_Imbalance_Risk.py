# ==========================================================
# IMBALANCE RISK ANALYTICS
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

    page_title="Imbalance Risk",

    page_icon="⚠️",

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
def load_risk_data(mode):


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



    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )



    return df





risk = load_risk_data(

    mode

)



if risk is None:


    st.error(

        "Risk dataset not found"

    )


    st.stop()



# ==========================================================
# FILTER COUNTRY
# ==========================================================


risk_country = risk[

    risk["country"] == country

].copy()



if risk_country.empty:


    st.warning(

        f"No risk data available for {country_display}"

    )


    st.stop()



risk_country = risk_country.sort_values(

    "timestamp"

)



# ==========================================================
# TITLE
# ==========================================================


st.title(

    "⚠️ Imbalance Risk Analysis"

)



st.caption(

    f"{country_display} imbalance exposure and risk monitoring"

)



# ==========================================================
# KPI
# ==========================================================


latest = risk_country.iloc[-1]



col1,col2,col3,col4 = st.columns(4)



with col1:

    st.metric(

        "Risk Score",

        f"{latest['risk_score']:.2f}"

    )



with col2:

    st.metric(

        "Risk Level",

        latest["risk_level"]

    )



with col3:

    st.metric(

        "Imbalance MW",

        f"{latest['imbalance_mw']:.2f}"

    )



with col4:

    st.metric(

        "Imbalance Cost",

        f"{latest['imbalance_cost_eur']:.2f} €"

    )



st.divider()



# ==========================================================
# RISK DISTRIBUTION
# ==========================================================


st.subheader(

    "Risk Level Distribution"

)



fig_distribution = px.histogram(

    risk_country,

    x="risk_level",

    category_orders={

        "risk_level":

        [

            "LOW",

            "MEDIUM",

            "HIGH"

        ]

    },

    title="Risk Categories"

)



st.plotly_chart(

    fig_distribution,

    use_container_width=True

)



# ==========================================================
# RISK SCORE EVOLUTION
# ==========================================================


st.subheader(

    "Risk Score Evolution"

)



fig_score = px.line(

    risk_country.tail(1000),

    x="timestamp",

    y="risk_score",

    title="Risk Score Over Time"

)



st.plotly_chart(

    fig_score,

    use_container_width=True

)



# ==========================================================
# IMBALANCE COST
# ==========================================================


st.subheader(

    "Imbalance Cost Evolution"

)



fig_cost = px.line(

    risk_country.tail(1000),

    x="timestamp",

    y="imbalance_cost_eur",

    title="Financial Exposure"

)



st.plotly_chart(

    fig_cost,

    use_container_width=True

)



# ==========================================================
# COUNTRY COMPARISON
# ==========================================================


st.subheader(

    "Country Risk Comparison"

)



if mode == "Sample":


    comparison = (

        risk

        .groupby("country")

        ["risk_score"]

        .mean()

        .reset_index()

    )


    fig_compare = px.bar(

        comparison,

        x="country",

        y="risk_score",

        title="Average Risk Score by Country"

    )


    st.plotly_chart(

        fig_compare,

        use_container_width=True

    )



else:


    st.info(

        "Country comparison available from all_countries_imbalance_risk.csv"

    )
