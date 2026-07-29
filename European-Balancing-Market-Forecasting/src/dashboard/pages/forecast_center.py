import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

ROOT = Path(
    r"D:\Portfolio\European-Balancing-Market-Forecasting"
)


FORECAST_DIR = (
    ROOT
    /
    "data"
    /
    "analytics"
    /
    "forecasting"
    /
    "ml"
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Forecast Center",
    page_icon="🔮",
    layout="wide"
)


st.title(
    "🔮 Next Day Balancing Forecast Center"
)


st.markdown(
    """
    Machine Learning based 24-hour imbalance forecasting
    using XGBoost models and uncertainty estimation.
    """
)


# ============================================================
# COUNTRY SELECTOR
# ============================================================

country = st.selectbox(
    "Select Country",
    COUNTRIES,
    format_func=lambda x: x.capitalize()
)



# ============================================================
# LOAD FORECAST
# ============================================================

file = (

    FORECAST_DIR

    /

    f"{country}_ml_forecast.csv"

)


if not file.exists():

    st.error(
        "Forecast file not found."
    )

    st.stop()



df = pd.read_csv(
    file
)


df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)



# ============================================================
# KPI SECTION
# ============================================================

latest = df.iloc[0]


mean_forecast = (
    df["forecast_imbalance"]
    .mean()
)


max_forecast = (
    df["forecast_imbalance"]
    .max()
)


uncertainty = (

    df["upper_bound"]
    -
    df["lower_bound"]

).mean()



risk = (

    df["risk_level"]
    .value_counts()
    .idxmax()

)



c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Average imbalance forecast",
        f"{mean_forecast:.0f} MW"
    )


with c2:

    st.metric(
        "Peak imbalance",
        f"{max_forecast:.0f} MW"
    )


with c3:

    st.metric(
        "Average uncertainty",
        f"±{uncertainty/2:.0f} MW"
    )


with c4:

    st.metric(
        "Risk Level",
        risk
    )



# ============================================================
# FORECAST CHART
# ============================================================


st.subheader(
    "24 Hour Imbalance Forecast"
)


fig = go.Figure()



# Confidence area

fig.add_trace(

    go.Scatter(

        x=df["timestamp"],

        y=df["upper_bound"],

        mode="lines",

        line=dict(
            width=0
        ),

        showlegend=False

    )

)



fig.add_trace(

    go.Scatter(

        x=df["timestamp"],

        y=df["lower_bound"],

        mode="lines",

        fill="tonexty",

        name="Confidence Interval",

        line=dict(
            width=0
        )

    )

)



# Forecast line

fig.add_trace(

    go.Scatter(

        x=df["timestamp"],

        y=df["forecast_imbalance"],

        mode="lines+markers",

        name="XGBoost Forecast"

    )

)



fig.update_layout(

    height=500,

    xaxis_title="Time",

    yaxis_title="Imbalance MW",

    hovermode="x unified"

)



st.plotly_chart(
    fig,
    use_container_width=True
)



# ============================================================
# TABLE
# ============================================================


st.subheader(
    "Forecast Details"
)



display = df.copy()


display["timestamp"] = (

    display["timestamp"]

    .dt.strftime(
        "%Y-%m-%d %H:%M"
    )

)


st.dataframe(

    display,

    use_container_width=True,

    height=400

)