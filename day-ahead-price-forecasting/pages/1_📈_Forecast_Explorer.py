import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

from pathlib import Path
# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]


DEMO_DIR = PROJECT_ROOT / "demo_data"

PREDICTIONS_DIR = DEMO_DIR / "predictions"

st.write("PROJECT ROOT:", PROJECT_ROOT)
st.write("PREDICTIONS DIR:", PREDICTIONS_DIR)
st.write("FILES:", list(PREDICTIONS_DIR.glob("*")))
# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Forecast Explorer",

    page_icon="📈",

    layout="wide"

)


# ============================================================
# TITLE
# ============================================================

st.title(
    "📈 Forecast Explorer"
)


st.markdown(
"""
Compare actual electricity prices against machine learning forecasts.
"""
)



# ============================================================
# LOAD FUNCTION
# ============================================================

@st.cache_data
def load_predictions(country, model):


   

    file = (
        PREDICTIONS_DIR
        /
        f"{model}_predictions.csv"
    )


    if not file.exists():

        return None


    df = pd.read_csv(

        file,

        index_col=0,

        parse_dates=True

    )


    df.index = pd.to_datetime(

        df.index,

        utc=True

    )


    df = df.sort_index()


    return df


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚙️ Forecast Settings"
)



country = st.sidebar.selectbox(

    "Country",

    [

        "germany",

        "greece"

    ]

)



available_models = [

    f.stem.replace("_predictions","")
    for f in PREDICTIONS_DIR.glob("*_predictions.csv")

]


model = st.sidebar.selectbox(

    "Model",

    available_models

)



# ============================================================
# LOAD DATA
# ============================================================


df = load_predictions(

    country,

    model

)



if df is None:

    st.error(
        "Prediction file not found"
    )

    st.stop()



# ============================================================
# FIND FORECAST COLUMN
# ============================================================

forecast_col = (

    [
        c for c in df.columns
        if c != "actual"
    ][0]

)



# ============================================================
# AVAILABLE DATES
# ============================================================


available_dates = (

    pd.Series(

        df.index.date

    )

    .unique()

    .tolist()

)



selected_date = st.sidebar.date_input(

    "📅 Select date",

    value=available_dates[-1],

    min_value=min(available_dates),

    max_value=max(available_dates)

)



# ============================================================
# FILTER
# ============================================================


daily = df[

    df.index.date == selected_date

]



if daily.empty:

    st.warning(
        "No data available"
    )

    st.stop()



# ============================================================
# METRICS
# ============================================================


mae = mean_absolute_error(

    daily["actual"],

    daily[forecast_col]

)



rmse = np.sqrt(

    mean_squared_error(

        daily["actual"],

        daily[forecast_col]

    )

)


avg_actual = daily["actual"].mean()

avg_forecast = daily[forecast_col].mean()

peak = daily["actual"].max()



col1,col2,col3,col4 = st.columns(4)



col1.metric(

    "Average Actual",

    f"{avg_actual:.2f} €/MWh"

)


col2.metric(

    "Average Forecast",

    f"{avg_forecast:.2f} €/MWh"

)


col3.metric(

    "MAE",

    f"{mae:.2f}"

)


col4.metric(

    "RMSE",

    f"{rmse:.2f}"

)




# ============================================================
# CHART
# ============================================================


st.subheader(

    f"{country.upper()} | {model.upper()} | {selected_date}"

)



fig = go.Figure()



fig.add_trace(

    go.Scatter(

        x=daily.index,

        y=daily["actual"],

        mode="lines+markers",

        name="Actual Price"

    )

)



fig.add_trace(

    go.Scatter(

        x=daily.index,

        y=daily[forecast_col],

        mode="lines+markers",

        name="Forecast"

    )

)



fig.update_layout(

    height=500,

    hovermode="x unified",

    xaxis_title="Hour",

    yaxis_title="€/MWh"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ============================================================
# TABLE
# ============================================================


st.subheader(
    "Hourly Forecast Table"
)


table = daily.copy()


table["error"] = (

    table["actual"]

    -

    table[forecast_col]

)


st.dataframe(

    table,

    use_container_width=True

)