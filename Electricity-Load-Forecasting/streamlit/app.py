import streamlit as st
import pandas as pd
import joblib
import json
from pathlib import Path
import sys

import plotly.graph_objects as go


# -----------------------
# Project path
# -----------------------

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(BASE_DIR)
)


# -----------------------
# Imports from src
# -----------------------

from src.loader import load_processed_data
from src.features import create_features
from src.predict import recursive_forecast



# -----------------------
# Page config
# -----------------------

st.set_page_config(
    page_title="European Energy Forecasting",
    layout="wide"
)



# -----------------------
# Sidebar
# -----------------------

with st.sidebar:

    st.title(
        "⚡ Energy Forecasting"
    )

    st.write(
        "Multi-country electricity demand forecasting"
    )

    st.divider()


    country = st.selectbox(
        "Select Country",
        [
            "Germany",
            "France",
            "Spain",
            "Netherlands"
        ]
    )


    st.divider()


    st.subheader(
        "Model"
    )

    st.write(
        "XGBoost Regressor"
    )


    st.subheader(
        "Forecast Horizon"
    )

    st.write(
        "24 hours"
    )


    st.subheader(
        "Training Period"
    )

    st.write(
        "2015 - 2020"
    )



# -----------------------
# Tabs
# -----------------------

tab1, tab2 = st.tabs(
    [
        "⚡ Forecast Dashboard",
        "🌍 Model Comparison"
    ]
)



# ==================================================
# TAB 1 - FORECAST DASHBOARD
# ==================================================

with tab1:


    st.title(
        "⚡ European Electricity Load Forecasting"
    )


    st.write(
        f"Machine Learning forecast for **{country}**"
    )



    # -----------------------
    # Load Model
    # -----------------------


    MODEL_PATH = (
        BASE_DIR
        / "models"
        / country
        / "xgboost_load_forecasting.pkl"
    )


    FEATURES_PATH = (
        BASE_DIR
        / "models"
        / country
        / "features.json"
    )


    model = joblib.load(
        MODEL_PATH
    )


    with open(
        FEATURES_PATH,
        "r"
    ) as f:

        features = json.load(f)



    st.success(
        f"{country} model loaded"
    )



    # -----------------------
    # Load Data
    # -----------------------


    df = load_processed_data(
        country
    )


    features_df = create_features(
        df
    )


    st.success(
        "Dataset loaded"
    )



    # -----------------------
    # Historical Load
    # -----------------------


    st.subheader(
        "📈 Historical Electricity Load"
    )


    last_week = df.tail(
        24*7
    )


    st.line_chart(
        last_week.set_index(
            "datetime"
        )["load"]
    )



    # -----------------------
    # KPIs
    # -----------------------


    st.subheader(
        "📊 Energy KPIs"
    )


    current_load = df["load"].iloc[-1]

    average_load = df["load"].mean()

    peak_load = df["load"].max()


    peak_hour = features_df.loc[
        features_df["load"].idxmax(),
        "hour"
    ]


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Current Load",
        f"{current_load:,.0f} MW"
    )


    c2.metric(
        "Average Load",
        f"{average_load:,.0f} MW"
    )


    c3.metric(
        "Peak Load",
        f"{peak_load:,.0f} MW"
    )


    c4.metric(
        "Peak Hour",
        f"{peak_hour}:00"
    )



    # -----------------------
    # Model Performance
    # -----------------------


    st.subheader(
        "🤖 Model Performance"
    )


    metrics_path = (
        BASE_DIR
        / "results"
        / "country_model_metrics.csv"
    )


    metrics = pd.read_csv(
        metrics_path,
        index_col=0
    )


    country_metrics = metrics.loc[country]


    m1,m2,m3 = st.columns(3)


    m1.metric(
        "MAE",
        f"{country_metrics['MAE']:.2f} MW"
    )


    m2.metric(
        "RMSE",
        f"{country_metrics['RMSE']:.2f} MW"
    )


    m3.metric(
        "MAPE",
        f"{country_metrics['MAPE']*100:.2f}%"
    )



    # -----------------------
    # Forecast
    # -----------------------


    st.subheader(
        "⚡ 24 Hour Forecast"
    )


    if st.button(
        "Generate Forecast"
    ):


        forecast = recursive_forecast(
            model,
            features_df,
            features
        )


        history = df.tail(
            24
        )


        fig = go.Figure()


        fig.add_trace(
            go.Scatter(
                x=history["datetime"],
                y=history["load"],
                name="Actual Load"
            )
        )


        fig.add_trace(
            go.Scatter(
                x=forecast["datetime"],
                y=forecast["forecast"],
                name="Forecast"
            )
        )


        fig.update_layout(
            height=500,
            yaxis_title="MW",
            xaxis_title="Datetime"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            forecast.style.format(
                {
                    "forecast": "{:,.0f} MW"
                }
            )
        )


        f1,f2,f3 = st.columns(3)


        f1.metric(
            "Forecast Average",
            f"{forecast['forecast'].mean():,.0f} MW"
        )


        f2.metric(
            "Forecast Peak",
            f"{forecast['forecast'].max():,.0f} MW"
        )


        f3.metric(
            "Forecast Minimum",
            f"{forecast['forecast'].min():,.0f} MW"
        )




# ==================================================
# TAB 2 - MODEL COMPARISON
# ==================================================

with tab2:


    st.title(
        "🌍 European Model Comparison"
    )


    comparison_path = (
        BASE_DIR
        / "results"
        / "country_model_metrics.csv"
    )


    comparison_df = pd.read_csv(
        comparison_path,
        index_col=0
    )



    st.subheader(
        "📊 Model Metrics"
    )


    st.dataframe(
        comparison_df.style.format(
            {
                "MAE":"{:.2f}",
                "RMSE":"{:.2f}",
                "MAPE":"{:.4f}"
            }
        )
    )



    st.subheader(
        "🏆 MAE Comparison"
    )


    st.bar_chart(
        comparison_df["MAE"]
    )



    st.subheader(
        "📉 RMSE Comparison"
    )


    st.bar_chart(
        comparison_df["RMSE"]
    )