# ==========================================================
# LOAD FORECASTING ANALYTICS
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
    page_title="Load Forecasting",
    page_icon="⚡",
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

    list(
        COUNTRIES.keys()
    )

)


country = COUNTRIES[
    country_display
]



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
def load_data(
    country,
    mode
):


    # ------------------------------
    # FEATURES
    # ------------------------------

    if mode == "Sample":

        feature_file = (
            SAMPLE_DIR
            /
            f"{country}_features_sample.csv"
        )

    else:

        feature_file = (
            FEATURES_DIR
            /
            f"{country}_features.csv"
        )



    if not feature_file.exists():

        return None, None



    features = pd.read_csv(
        feature_file
    )



    features["timestamp"] = pd.to_datetime(

        features["timestamp"],

        utc=True

    )



    # ------------------------------
    # FORECAST RESULTS
    # ------------------------------


    forecast_file = (
        RESULTS_DIR
        /
        f"{country}_load_forecast_results.csv"
    )



    forecast = None


    if forecast_file.exists():

        forecast = pd.read_csv(
            forecast_file
        )



        if "timestamp" in forecast.columns:


            forecast["timestamp"] = pd.to_datetime(

                forecast["timestamp"],

                utc=True

            )



    return features, forecast





features, forecast = load_data(

    country,

    mode

)



if features is None:


    st.error(
        "Dataset not found"
    )


    st.stop()



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


col1,col2,col3,col4 = st.columns(4)



with col1:

    st.metric(

        "Current Load",

        f"{latest['load_mw']/1000:.2f} GW"

    )



with col2:

    st.metric(

        "Day Ahead Price",

        f"{latest['day_ahead_price']:.2f} €/MWh"

    )



with col3:

    st.metric(

        "Renewable Share",

        f"{latest['renewable_share']:.1f}%"

    )



with col4:

    st.metric(

        "Data Mode",

        mode

    )



st.divider()



# ==========================================================
# LOAD HISTORY
# ==========================================================


st.subheader(

    "Electricity Load History"

)



fig = px.line(

    features.tail(500),

    x="timestamp",

    y="load_mw",

    title="Recent Load Evolution"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ==========================================================
# FORECAST
# ==========================================================


st.subheader(

    "Load Forecast"

)



if forecast is not None and len(forecast) > 0:


    st.dataframe(

        forecast.tail(20),

        use_container_width=True

    )


else:


    st.info(

        "Forecast results available only in Local mode after running pipeline."

    )



# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================


st.subheader(

    "Model Feature Importance"

)



importance_file = (

    RESULTS_DIR

    /

    f"{country}_load_feature_importance.csv"

)



if importance_file.exists():


    importance = pd.read_csv(

        importance_file

    )


    fig_imp = px.bar(

        importance.head(15),

        x="importance",

        y="feature",

        orientation="h",

        title="Top Features"

    )


    st.plotly_chart(

        fig_imp,

        use_container_width=True

    )


else:


    st.info(

        "Feature importance available in Local mode."

    )