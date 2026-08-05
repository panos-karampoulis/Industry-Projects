# ==========================================================
# MODEL PERFORMANCE DASHBOARD
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

    page_title="Model Performance",

    page_icon="🤖",

    layout="wide"

)



# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]


RESULTS_DIR = (

    BASE_DIR
    /
    "results"

)



# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title(

    "⚡ Energy Trading DSS"

)



country_display = st.sidebar.selectbox(

    "Select Country",

    [

        "Germany",

        "France",

        "Italy",

        "Spain",

        "Netherlands"

    ]

)



country = country_display.lower()



# ==========================================================
# TITLE
# ==========================================================

st.title(

    "🤖 Forecasting Model Performance"

)


st.caption(

    "Machine Learning model evaluation and explainability"

)



# ==========================================================
# LOAD METRICS
# ==========================================================


@st.cache_data
def load_metrics():


    file = (

        RESULTS_DIR

        /

        "load_forecast_metrics.csv"

    )


    if not file.exists():

        return None



    df = pd.read_csv(

        file

    )


    return df





metrics = load_metrics()



if metrics is None:


    st.warning(

        "Model metrics not found. Run forecasting pipeline first."

    )

    st.stop()



# ==========================================================
# COUNTRY FILTER (OPTIONAL)
# ==========================================================


if "country" in metrics.columns:


    country_metrics = metrics[

        metrics["country"]

        .str.lower()

        == country

    ]


    if country_metrics.empty:

        country_metrics = metrics.copy()


else:


    country_metrics = metrics.copy()
# ==========================================================
# METRICS TABLE
# ==========================================================


st.subheader(

    "Forecast Metrics"

)



st.dataframe(

    country_metrics,

    use_container_width=True

)



# ==========================================================
# MODEL COMPARISON
# ==========================================================


st.subheader(

    "Model Accuracy Comparison"

)
country_metrics.columns = [

    c.lower()

    for c in country_metrics.columns

]


if "model" in country_metrics.columns:


    fig = px.bar(

        country_metrics,

        x="model",

        y="rmse",

        title="RMSE Comparison (Lower is Better)"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



# ==========================================================
# MAE
# ==========================================================


if "MAE" in country_metrics.columns:


    fig_mae = px.bar(

        country_metrics,

        x="model",

        y="mae",

        title="MAE Comparison"

    )


    st.plotly_chart(

        fig_mae,

        use_container_width=True

    )



# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================


st.subheader(

    "Feature Importance"

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


    importance = importance.sort_values(

        "importance",

        ascending=False

    )



    fig_imp = px.bar(

        importance.head(15),

        x="importance",

        y="feature",

        orientation="h",

        title="Top Predictive Features"

    )



    st.plotly_chart(

        fig_imp,

        use_container_width=True

    )



else:


    st.info(

        "Feature importance file not available for this country."

    )



# ==========================================================
# PRICE MODEL PERFORMANCE
# ==========================================================


st.subheader(

    "Price Forecasting Performance"

)



price_metrics_file = (

    RESULTS_DIR

    /

    "statistical_models_results.csv"

)



if price_metrics_file.exists():


    price_metrics = pd.read_csv(

        price_metrics_file

    )


    st.dataframe(

        price_metrics,

        use_container_width=True

    )


else:


    st.info(

        "Price forecasting metrics not available."

    )