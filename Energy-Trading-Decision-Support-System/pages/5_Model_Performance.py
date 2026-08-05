# ==========================================================
# MODEL PERFORMANCE DASHBOARD
# Energy Trading Decision Support System
# Cloud + Local Compatible
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


DEMO_DIR = (
    BASE_DIR
    /
    "data"
    /
    "demo"
)



# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(

    "⚡ Energy Trading DSS"

)



country_display = st.sidebar.selectbox(

    "Country",

    [

        "Germany",
        "France",
        "Italy",
        "Spain",
        "Netherlands"

    ]

)


country = country_display.lower()



mode = st.sidebar.radio(

    "Data Mode",

    [

        "Demo",
        "Local"

    ]

)



# ==========================================================
# TITLE
# ==========================================================


st.title(

    "🤖 Forecasting Model Performance"

)



st.caption(

    "Machine Learning evaluation, metrics and explainability"

)



# ==========================================================
# LOAD MODEL METRICS
# ==========================================================


@st.cache_data
def load_metrics():



    file = (

        RESULTS_DIR

        /

        "load_forecast_metrics.csv"

    )


    if file.exists():


        return pd.read_csv(file)



    # ------------------------------
    # DEMO RESULTS
    # ------------------------------


    return pd.DataFrame(

        {


            "model":

            [

                "Linear Regression",

                "Random Forest",

                "XGBoost",

                "Prophet"

            ],


            "MAE":

            [

                1109.31,

                537.23,

                490.64,

                2820.25

            ],


            "RMSE":

            [

                1422.28,

                739.01,

                650.90,

                3719.09

            ],


            "MAPE":

            [

                0.0214,

                0.0104,

                0.0095,

                0.0563

            ]

        }

    )




metrics = load_metrics()



# ==========================================================
# METRICS TABLE
# ==========================================================


st.subheader(

    "Forecast Metrics"

)



st.dataframe(

    metrics,

    use_container_width=True

)



# ==========================================================
# MODEL COMPARISON
# ==========================================================


st.subheader(

    "Model Accuracy Comparison"

)



fig = px.bar(

    metrics,

    x="model",

    y="RMSE",

    title="RMSE Comparison (Lower is Better)"

)



st.plotly_chart(

    fig,

    use_container_width=True

)




fig2 = px.bar(

    metrics,

    x="model",

    y="MAE",

    title="MAE Comparison"

)



st.plotly_chart(

    fig2,

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


else:


    importance = pd.DataFrame(

        {

        "feature":

        [

            "load_lag_1",

            "load_lag_24",

            "load_lag_168",

            "renewable_generation",

            "day_ahead_price"

        ],


        "importance":

        [

            0.916,

            0.035,

            0.020,

            0.018,

            0.011

        ]

        }

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



# ==========================================================
# PRICE FORECASTING
# ==========================================================


st.subheader(

    "📈 Price Forecasting Performance"

)



price_file = (

    RESULTS_DIR

    /

    "statistical_models_results.csv"

)



if price_file.exists():


    price_metrics = pd.read_csv(

        price_file

    )


else:


    price_metrics = pd.DataFrame(

        {

        "Model":

        [

            "SARIMAX"

        ],


        "MAE":

        [

            12.71

        ],


        "RMSE":

        [

            15.83

        ]

        }

    )




st.dataframe(

    price_metrics,

    use_container_width=True

)



# ==========================================================
# FOOTER
# ==========================================================


st.divider()


st.caption(

f"""

Mode: {mode}

Country: {country_display}

"""

)