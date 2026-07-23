import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# Streamlit Config
# ==========================================

st.set_page_config(
    page_title="Electricity Demand Forecast",
    page_icon="⚡",
    layout="wide"
)


# ==========================================
# Sidebar
# ==========================================

st.sidebar.title(
    "⚡ Energy Forecasting"
)


countries = [
    "germany",
    "france",
    "netherlands",
    "austria"
]


country = st.sidebar.selectbox(
    "Select Country",
    countries
)


# ==========================================
# Directories
# ==========================================

report_dir = (
    BASE_DIR
    /
    "reports"
    /
    country
)


forecast_dir = (
    report_dir
    /
    "forecasts"
)


backtest_file = (
    report_dir
    /
    "rolling_backtest_results.csv"
)


# ==========================================
# Load Forecast
# ==========================================

if not forecast_dir.exists():

    st.warning(
        f"No forecast folder found for {country}"
    )

    st.stop()



forecast_files = list(
    forecast_dir.glob(
        "*forecast*.csv"
    )
)


if len(forecast_files) == 0:

    st.warning(
        f"No forecast files found for {country}"
    )

    st.stop()



forecast_file = forecast_files[-1]


forecast = pd.read_csv(
    forecast_file,
    parse_dates=["datetime"]
)



# Detect forecast column

forecast_column = None


for col in forecast.columns:

    if "forecast" in col.lower():

        forecast_column = col

        break



if forecast_column is None:

    st.error(
        "Forecast column not found"
    )

    st.stop()



# ==========================================
# Header
# ==========================================

st.title(
    "⚡ Electricity Demand Forecast"
)


st.subheader(
    f"Country: {country.upper()}"
)


st.caption(
    f"Forecast file: {forecast_file.name}"
)



# ==========================================
# KPIs
# ==========================================


average_load = (
    forecast[forecast_column]
    .mean()
)


peak_load = (
    forecast[forecast_column]
    .max()
)


peak_hour = (
    forecast.loc[
        forecast[forecast_column].idxmax(),
        "datetime"
    ]
)


daily_energy = (
    forecast[forecast_column]
    .sum()
    /
    1000
)



col1, col2, col3, col4 = st.columns(4)



col1.metric(
    "Average Load",
    f"{average_load/1000:.2f} GW"
)


col2.metric(
    "Peak Load",
    f"{peak_load/1000:.2f} GW"
)


col3.metric(
    "Peak Hour",
    peak_hour.strftime("%H:%M")
)


col4.metric(
    "Daily Energy",
    f"{daily_energy:.2f} GWh"
)



st.divider()



# ==========================================
# Forecast Chart
# ==========================================


st.subheader(
    "Hourly Demand Forecast"
)



fig, ax = plt.subplots(
    figsize=(12,4)
)



ax.plot(
    forecast["datetime"],
    forecast[forecast_column]
)



ax.set_xlabel(
    "Datetime"
)


ax.set_ylabel(
    "Load (MW)"
)


ax.grid(
    True
)


plt.xticks(
    rotation=45
)



st.pyplot(
    fig
)



# ==========================================
# Backtest Metrics
# ==========================================


st.subheader(
    "Model Performance"
)



if backtest_file.exists():


    backtest = pd.read_csv(
        backtest_file
    )


    metrics = (
        backtest
        .mean(numeric_only=True)
    )



    c1,c2,c3,c4 = st.columns(4)



    if "MAPE" in metrics:

        c1.metric(
            "MAPE",
            f"{metrics['MAPE']:.2f}%"
        )


    if "MAE" in metrics:

        c2.metric(
            "MAE",
            f"{metrics['MAE']:.0f} MW"
        )


    if "RMSE" in metrics:

        c3.metric(
            "RMSE",
            f"{metrics['RMSE']:.0f} MW"
        )


    if "R2" in metrics:

        c4.metric(
            "R²",
            f"{metrics['R2']:.3f}"
        )


else:

    st.info(
        "No backtest results available yet."
    )



# ==========================================
# Forecast Table
# ==========================================


with st.expander(
    "View Forecast Data"
):

    st.dataframe(
        forecast,
        use_container_width=True
    )