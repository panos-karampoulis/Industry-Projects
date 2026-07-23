import streamlit as st
import pandas as pd
import yaml
import plotly.express as px

from pathlib import Path
import sys


# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


sys.path.append(
    str(BASE_DIR / "src")
)


from forecast_engine import generate_forecast



# ---------------------------------------
# Load configs
# ---------------------------------------

COUNTRY_CONFIG = (
    BASE_DIR
    /
    "configs"
    /
    "countries.yaml"
)


MODEL_CONFIG = (
    BASE_DIR
    /
    "configs"
    /
    "models.yaml"
)



with open(COUNTRY_CONFIG, "r") as f:

    countries = yaml.safe_load(f)



with open(MODEL_CONFIG, "r") as f:

    models = yaml.safe_load(f)



available_countries = list(
    countries.keys()
)



# ---------------------------------------
# Page config
# ---------------------------------------

st.set_page_config(

    page_title="Electricity Demand Forecast",

    page_icon="⚡",

    layout="wide"

)



# ---------------------------------------
# Title
# ---------------------------------------

st.title(
    "⚡ Electricity Demand Forecast Platform"
)


st.write(
    "Multi-country electricity demand forecasting using XGBoost and weather data"
)



# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.header(
    "Forecast Configuration"
)



country = st.sidebar.selectbox(

    "Select Country",

    available_countries

)



forecast_date = st.sidebar.date_input(

    "Forecast Date"

)



generate = st.sidebar.button(

    "🚀 Generate Forecast"

)



# ---------------------------------------
# Run Forecast
# ---------------------------------------

if generate:


    with st.spinner(
        "Generating forecast..."
    ):


        forecast, summary = generate_forecast(

            country=country,

            forecast_date=forecast_date

        )


        # ---------------------------------------
    # Save Forecast History
    # ---------------------------------------

    forecast_dir = (

        BASE_DIR
        /
        "reports"
        /
        "forecasts"
        /
        country

    )


    forecast_dir.mkdir(

        parents=True,

        exist_ok=True

    )



    forecast_file = (

        forecast_dir

        /

        f"{country}_forecast_{forecast_date}.csv"

    )



    forecast.to_csv(

        forecast_file,

        index=False

    )


    st.success(

    f"""
    Forecast generated successfully

    Saved:
    {forecast_file}
    """

    )


    # -----------------------------------
    # KPI Cards
    # -----------------------------------

    col1, col2, col3, col4 = st.columns(4)



    col1.metric(

        "Average Load",

        f"{summary['average_load_mw']/1000:.2f} GW"

    )


    col2.metric(

        "Peak Load",

        f"{summary['peak_load_mw']/1000:.2f} GW"

    )


    col3.metric(

        "Peak Hour",

        summary["peak_hour"]

    )


    col4.metric(

        "Daily Energy",

        f"{summary['daily_energy_gwh']:.2f} GWh"

    )



    st.divider()



    # -----------------------------------
    # Forecast Chart
    # -----------------------------------

    st.subheader(
        "Hourly Demand Forecast"
    )


    fig = px.line(

        forecast,

        x="datetime",

        y="forecast_load_mw",

        markers=True,

        title=f"{country.upper()} Demand Forecast"

    )


    fig.update_layout(

        xaxis_title="Time",

        yaxis_title="Load (MW)",

        height=450

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



    st.divider()



    # -----------------------------------
    # Model Performance
    # -----------------------------------

    st.subheader(
        "🤖 Model Performance"
    )


    model_info = models[country]

    metrics = model_info["metrics"]



    c1, c2, c3 = st.columns(3)



    c1.metric(

        "MAE",

        f"{metrics['MAE_MW']:.2f} MW"

    )


    c2.metric(

        "RMSE",

        f"{metrics['RMSE_MW']:.2f} MW"

    )


    c3.metric(

        "R²",

        f"{metrics['R2']:.4f}"

    )



    st.caption(

        f"""
        Model: {model_info['model_name']}
        
        Version: {model_info['model_version']}
        """

    )



    st.divider()



    # -----------------------------------
    # Data Preview
    # -----------------------------------

    with st.expander(
        "View Forecast Data"
    ):

        st.dataframe(
            forecast
        )



    # -----------------------------------
    # Download
    # -----------------------------------

    csv = forecast.to_csv(
        index=False
    )


    st.download_button(

        label="⬇ Download Forecast CSV",

        data=csv,

        file_name=(

            f"{country}_forecast_{forecast_date}.csv"

        ),

        mime="text/csv"

    )



else:


    st.info(

        "Select country and click Generate Forecast"

    )