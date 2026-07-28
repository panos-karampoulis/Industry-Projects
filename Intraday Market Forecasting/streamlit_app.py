# ============================================================
# Intraday Electricity Market Forecasting Dashboard
# Part 1/3
# ============================================================

import os
import warnings

import pandas as pd
import numpy as np

import streamlit as st

import matplotlib.pyplot as plt


warnings.filterwarnings("ignore")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Intraday Electricity Market Forecasting",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# BASE PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


FEATURE_DIR = os.path.join(
    DATA_DIR,
    "features"
)


RESULTS_DIR = os.path.join(
    DATA_DIR,
    "results"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


IMAGE_DIR = os.path.join(
    BASE_DIR,
    "images"
)


SHAP_DIR = os.path.join(
    IMAGE_DIR,
    "shap"
)


IMPORTANCE_DIR = os.path.join(
    IMAGE_DIR,
    "feature_importance"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "⚡ Intraday Electricity Market Forecasting"
)


st.markdown(
    """
Machine Learning based intraday electricity price forecasting.

**Models**
- Linear Regression
- Random Forest
- XGBoost


**Markets**
- France
- Germany
- Italy
- Netherlands
- Spain


Forecast resolution:

**15 minutes (96 intervals/day)**
"""
)


# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = {
    "France": "france",
    "Germany": "germany",
    "Italy": "italy",
    "Netherlands": "netherlands",
    "Spain": "spain"
}



# ============================================================
# TIMESTAMP DETECTION
# ============================================================

def detect_timestamp(df):

    possible_columns = [
        "timestamp",
        "local_timestamp",
        "datetime",
        "date",
        "Unnamed: 0"
    ]


    for col in possible_columns:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            return col


    raise Exception(
        f"No timestamp column found. Available columns: {list(df.columns)}"
    )



# ============================================================
# LOAD HISTORICAL FEATURES
# ============================================================

@st.cache_data(show_spinner=False)
def load_historical_data(country):


    file_path = os.path.join(
        FEATURE_DIR,
        f"{country}_features.csv"
    )


    if not os.path.exists(file_path):

        raise FileNotFoundError(
            file_path
        )


    df = pd.read_csv(
        file_path
    )


    timestamp_col = detect_timestamp(df)


    df = df.rename(
        columns={
            timestamp_col:"timestamp"
        }
    )


    df = df.sort_values(
        "timestamp"
    )


    return df



# ============================================================
# LOAD FORECAST RESULTS
# ============================================================

@st.cache_data(show_spinner=False)
def load_prediction_results(country):


    file_path = os.path.join(
        RESULTS_DIR,
        f"{country}_Linear_Regression_predictions.csv"
    )


    if not os.path.exists(file_path):

        return None


    df = pd.read_csv(
        file_path
    )


    timestamp_col = detect_timestamp(df)


    df = df.rename(
        columns={
            timestamp_col:"timestamp"
        }
    )


    # normalize columns

    if "actual" in df.columns:

        df["actual_price"] = df["actual"]


    if "prediction" in df.columns:

        df["predicted_price"] = df["prediction"]


    return df



# ============================================================
# LOAD NEXT DAY FORECAST
# ============================================================

@st.cache_data(show_spinner=False)
def load_next_day_forecast(country):


    file_path = os.path.join(
        RESULTS_DIR,
        "next_day_forecasts",
        f"{country}_next_day_forecast.csv"
    )


    if not os.path.exists(file_path):

        return None


    df = pd.read_csv(
        file_path
    )


    timestamp_col = detect_timestamp(df)


    df = df.rename(
        columns={
            timestamp_col:"timestamp"
        }
    )


    return df



# ============================================================
# LOAD IMAGE
# ============================================================

def load_image(folder, country):

    possible_files = [

        os.path.join(
            folder,
            f"{country}_shap_summary.png"
        ),

        os.path.join(
            folder,
            f"{country}_feature_importance.png"
        ),

        os.path.join(
            folder,
            f"{country}_shap.png"
        ),

        os.path.join(
            folder,
            f"{country}.png"
        )

    ]

    for file in possible_files:

        if os.path.exists(file):

            return file

    # fallback:
    # βρίσκει οποιοδήποτε png που ξεκινάει με το όνομα της χώρας

    for file in os.listdir(folder):

        if file.lower().startswith(country.lower()) and file.lower().endswith(".png"):

            return os.path.join(folder, file)

    return None



# ============================================================
# SIDEBAR
# ============================================================


st.sidebar.header(
    "⚙️ Controls"
)


selected_country = st.sidebar.selectbox(

    "Select Country",

    list(COUNTRIES.keys())

)


country_code = COUNTRIES[selected_country]


st.sidebar.info(

    f"""
Selected Market:

{selected_country}

Resolution:

15 minutes

96 points/day
"""
)



# ============================================================
# TABS
# ============================================================


tab1, tab2, tab3, tab4 = st.tabs(

    [
        "📈 Historical Intraday Analysis",
        "🔮 Intraday Forecast",
        "📊 Model Performance",
        "🧠 Explainability"
    ]

)

# ============================================================
# TAB 1
# HISTORICAL INTRADAY ANALYSIS
# ============================================================


with tab1:


    st.header(
        f"📈 Historical Intraday Analysis - {selected_country}"
    )


    try:

        hist_df = load_historical_data(
            country_code
        )


        st.success(
            f"Loaded dataset: {hist_df.shape[0]:,} rows"
        )


        # --------------------------------------------
        # Date selector
        # --------------------------------------------

        min_date = hist_df["timestamp"].min().date()

        max_date = hist_df["timestamp"].max().date()


        selected_date = st.date_input(

            "Select Historical Date",

            value=max_date,

            min_value=min_date,

            max_value=max_date

        )


        daily = hist_df[
            hist_df["timestamp"].dt.date
            ==
            selected_date
        ].copy()



        if len(daily) == 0:

            st.warning(
                "No data available for selected date"
            )

        else:


            st.subheader(
                "📌 Market Summary"
            )


            col1, col2, col3, col4 = st.columns(4)


            # Price column detection

            price_col = None


            possible_price = [

                "day_ahead_price",
                "price",
                "actual_price"

            ]


            for c in possible_price:

                if c in daily.columns:

                    price_col = c
                    break



            if price_col:


                col1.metric(

                    "Average Price",

                    f"{daily[price_col].mean():.2f} €/MWh"

                )


                col2.metric(

                    "Maximum Price",

                    f"{daily[price_col].max():.2f} €/MWh"

                )


                col3.metric(

                    "Minimum Price",

                    f"{daily[price_col].min():.2f} €/MWh"

                )


                col4.metric(

                    "Volatility",

                    f"{daily[price_col].std():.2f}"

                )



            # =====================================================
            # PRICE CHART
            # =====================================================


            st.subheader(
                "⚡ Intraday Electricity Price"
            )


            if price_col:


                fig, ax = plt.subplots(
                    figsize=(12,4)
                )


                ax.plot(

                    daily["timestamp"],

                    daily[price_col]

                )


                ax.set_ylabel(
                    "€/MWh"
                )


                ax.set_xlabel(
                    "Time"
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



            # =====================================================
            # LOAD
            # =====================================================


            if "load_mw" in daily.columns:


                st.subheader(
                    "🔌 Electricity Load"
                )


                fig, ax = plt.subplots(
                    figsize=(12,4)
                )


                ax.plot(

                    daily["timestamp"],

                    daily["load_mw"]

                )


                ax.set_ylabel(
                    "MW"
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



            # =====================================================
            # RENEWABLES
            # =====================================================


            renewable_cols = []


            for c in [

                "wind_generation",

                "solar_generation",

                "renewable_generation"

            ]:


                if c in daily.columns:

                    renewable_cols.append(c)



            if renewable_cols:


                st.subheader(
                    "🌱 Renewable Generation"
                )


                fig, ax = plt.subplots(
                    figsize=(12,4)
                )


                for c in renewable_cols:


                    ax.plot(

                        daily["timestamp"],

                        daily[c],

                        label=c

                    )


                ax.legend()


                ax.set_ylabel(
                    "MW"
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



            # =====================================================
            # WEATHER
            # =====================================================


            weather_cols = []


            for c in [

                "temperature_2m",

                "wind_speed_10m",

                "shortwave_radiation",

                "cloud_cover",

                "precipitation"

            ]:


                if c in daily.columns:

                    weather_cols.append(c)



            if weather_cols:


                st.subheader(
                    "🌤 Weather Conditions"
                )


                selected_weather = st.multiselect(

                    "Select Weather Variables",

                    weather_cols,

                    default=weather_cols[:2]

                )


                if selected_weather:


                    fig, ax = plt.subplots(
                        figsize=(12,4)
                    )


                    for c in selected_weather:


                        ax.plot(

                            daily["timestamp"],

                            daily[c],

                            label=c

                        )


                    ax.legend()


                    ax.grid(
                        True
                    )


                    plt.xticks(
                        rotation=45
                    )


                    st.pyplot(
                        fig
                    )



            # =====================================================
            # TABLE
            # =====================================================


            with st.expander(
                "View Intraday Data"
            ):


                st.dataframe(

                    daily,

                    use_container_width=True

                )


    except Exception as e:


        st.error(
            str(e)
        )

# ============================================================
# TAB 2
# INTRADAY FORECAST
# ============================================================


with tab2:


    st.header(
        f"🔮 Intraday Forecast - {selected_country}"
    )


    forecast_df = load_next_day_forecast(
        country_code
    )


    if forecast_df is None:


        st.warning(
            "No forecast file available."
        )


    else:


        min_date = forecast_df["timestamp"].min().date()

        max_date = forecast_df["timestamp"].max().date()


        selected_forecast_date = st.date_input(

            "Select Forecast Date",

            value=max_date,

            min_value=min_date,

            max_value=max_date,

            key="forecast_date"

        )


        forecast_day = forecast_df[

            forecast_df["timestamp"].dt.date
            ==
            selected_forecast_date

        ].copy()



        if len(forecast_day)==0:


            st.warning(
                "No forecast available for selected date."
            )


        else:


            st.subheader(
                "Prediction Curve"
            )


            fig, ax = plt.subplots(
                figsize=(12,4)
            )


            ax.plot(

                forecast_day["timestamp"],

                forecast_day["predicted_price"],

                label="Prediction"

            )


            if "actual_price" in forecast_day.columns:


                ax.plot(

                    forecast_day["timestamp"],

                    forecast_day["actual_price"],

                    label="Actual"

                )


            ax.legend()


            ax.set_ylabel(
                "€/MWh"
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



            st.subheader(
                "Forecast Table"
            )


            st.dataframe(

                forecast_day,

                use_container_width=True

            )



# ============================================================
# TAB 3
# MODEL PERFORMANCE
# ============================================================


with tab3:


    st.header(
        f"📊 Model Performance - {selected_country}"
    )


    predictions = load_prediction_results(
        country_code
    )


    if predictions is None:


        st.warning(
            "Prediction results not found."
        )


    else:


        if (

            "actual_price" in predictions.columns

            and

            "predicted_price" in predictions.columns

        ):


            actual = predictions["actual_price"]

            pred = predictions["predicted_price"]


            mae = np.mean(
                np.abs(actual-pred)
            )


            rmse = np.sqrt(
                np.mean(
                    (actual-pred)**2
                )
            )


            mape = np.mean(

                np.abs(
                    (actual-pred)/actual
                )

            )*100



            col1,col2,col3,col4 = st.columns(4)


            col1.metric(

                "MAE",

                f"{mae:.2f}"

            )


            col2.metric(

                "RMSE",

                f"{rmse:.2f}"

            )


            col3.metric(

                "MAPE",

                f"{mape:.2f}%"

            )


            col4.metric(

                "Mean Actual Price",

                f"{actual.mean():.2f} €/MWh"

            )



            st.subheader(
                "Actual vs Prediction"
            )


            sample = predictions.tail(500)


            fig, ax = plt.subplots(

                figsize=(12,4)

            )


            ax.plot(

                sample["timestamp"],

                sample["actual_price"],

                label="Actual"

            )


            ax.plot(

                sample["timestamp"],

                sample["predicted_price"],

                label="Prediction"

            )


            ax.legend()

            ax.grid(True)


            plt.xticks(

                rotation=45

            )


            st.pyplot(
                fig
            )



# ============================================================
# TAB 4
# EXPLAINABILITY
# ============================================================


with tab4:


    st.header(
        f"🧠 Explainability - {selected_country}"
    )


    country_lower = country_code



    # ----------------------------
    # SHAP
    # ----------------------------


    st.subheader(
        "SHAP Analysis"
    )


    shap_file = load_image(

        SHAP_DIR,

        country_lower

    )


    if shap_file:


        st.image(

            shap_file,

            use_container_width=True

        )


    else:


        st.warning(
            "SHAP image not found."
        )



    # ----------------------------
    # Feature Importance
    # ----------------------------


    st.subheader(
        "Feature Importance"
    )


    importance_file = load_image(

        IMPORTANCE_DIR,

        country_lower

    )


    if importance_file:


        st.image(

            importance_file,

            use_container_width=True

        )


    else:


        st.warning(
            "Feature importance image not found."
        )



# ============================================================
# FOOTER
# ============================================================


st.divider()


st.caption(

    """
Energy Analytics Portfolio Project

Intraday Electricity Price Forecasting

Machine Learning + Explainability

96 intervals/day

"""
)
