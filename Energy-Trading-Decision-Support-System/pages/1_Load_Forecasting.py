# ==========================================================
# LOAD FORECASTING ANALYTICS
# Energy Trading Decision Support System
# Cloud + Local Compatible
# ==========================================================


import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
import numpy as np



# ==========================================================
# PAGE CONFIG
# ==========================================================


st.set_page_config(

    page_title="Load Forecasting",

    page_icon="⚡",

    layout="wide"

)



# ==========================================================
# PATHS
# ==========================================================


BASE_DIR = Path(__file__).resolve().parents[1]


DEMO_DIR = (
    BASE_DIR
    /
    "data"
    /
    "demo"
)


FEATURE_DIR = (
    BASE_DIR
    /
    "data"
    /
    "features"
)


RESULT_DIR = (
    BASE_DIR
    /
    "results"
)



COUNTRIES = {

    "Germany":"germany",
    "France":"france",
    "Italy":"italy",
    "Spain":"spain",
    "Netherlands":"netherlands"

}



# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(
    "⚡ Energy Trading DSS"
)


country_display = st.sidebar.selectbox(

    "Country",

    list(COUNTRIES.keys())

)


country = COUNTRIES[country_display]



mode = st.sidebar.radio(

    "Data Mode",

    [
        "Demo",
        "Local"
    ]

)



# ==========================================================
# LOAD FEATURES
# ==========================================================


@st.cache_data
def load_features(country, mode):


    if mode=="Demo":


        file = (

            DEMO_DIR

            /

            f"{country}_features_sample.csv"

        )


    else:


        file = (

            FEATURE_DIR

            /

            f"{country}_features.csv"

        )



    if not file.exists():

        return pd.DataFrame()



    df = pd.read_csv(file)



    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df




features = load_features(

    country,

    mode

)



if features.empty:


    st.error(

        "Dataset not found"

    )

    st.stop()



# ==========================================================
# CREATE DEMO FORECAST
# ==========================================================


def create_demo_forecast(df):


    forecast = df[

        [

            "timestamp",

            "load_mw"

        ]

    ].copy()



    forecast["forecast_load_mw"] = (

        forecast["load_mw"]

        *

        np.random.normal(

            1,

            0.015,

            len(forecast)

        )

    )


    return forecast





# ==========================================================
# FORECAST LOADING
# ==========================================================


forecast_file = (

    RESULT_DIR

    /

    f"{country}_load_forecast_results.csv"

)



if forecast_file.exists():


    forecast = pd.read_csv(

        forecast_file

    )


    forecast["timestamp"] = pd.to_datetime(

        forecast["timestamp"],

        utc=True

    )


else:


    forecast = create_demo_forecast(

        features

    )





# ==========================================================
# TITLE
# ==========================================================


st.title(

    "⚡ Load Forecasting"

)



st.caption(

    f"{country_display} electricity demand forecasting"

)



# ==========================================================
# KPI
# ==========================================================


latest = features.iloc[-1]


c1,c2,c3,c4 = st.columns(4)



with c1:


    st.metric(

        "Current Load",

        f"{latest['load_mw']/1000:.2f} GW"

    )



with c2:


    st.metric(

        "Price",

        f"{latest['day_ahead_price']:.2f} €/MWh"

    )



with c3:


    st.metric(

        "Renewable Share",

        f"{latest['renewable_share']:.1%}"

    )



with c4:


    st.metric(

        "Mode",

        mode

    )




st.divider()



# ==========================================================
# LOAD HISTORY
# ==========================================================


st.subheader(

    "⚡ Electricity Load History"

)



fig = px.line(

    features.tail(500),

    x="timestamp",

    y="load_mw",

    title="Historical Load"

)


st.plotly_chart(

    fig,

    use_container_width=True

)




# ==========================================================
# FORECAST GRAPH
# ==========================================================


st.subheader(

    "🔮 Load Forecast"

)



fig = px.line(

    forecast.tail(500),

    x="timestamp",

    y=[

        "load_mw",

        "forecast_load_mw"

    ],

    title="Actual vs Forecast Load"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================


st.subheader(

    "🤖 Model Feature Importance"

)



importance_file = (

    RESULT_DIR

    /

    f"{country}_load_feature_importance.csv"

)



if importance_file.exists():


    importance = pd.read_csv(

        importance_file

    )


else:


    importance = pd.DataFrame({

        "feature":[

            "load_lag_1",

            "load_lag_24",

            "load_lag_168",

            "renewable_generation",

            "day_ahead_price"

        ],

        "importance":[

            0.91,

            0.04,

            0.02,

            0.02,

            0.01

        ]

    })




fig = px.bar(

    importance.head(10),

    x="importance",

    y="feature",

    orientation="h",

    title="Top Predictive Features"

)


st.plotly_chart(

    fig,

    use_container_width=True

)