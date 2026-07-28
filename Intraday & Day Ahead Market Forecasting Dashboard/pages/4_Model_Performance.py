import os
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import joblib



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Model Performance",

    page_icon="📊",

    layout="wide"

)



# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(
    r"D:\Portfolio\Intraday Market Forecasting - updated"
)


BACKTEST_DIR = (

    BASE_DIR

    /

    "data"

    /

    "backtesting"

)



MODEL_DIR = (

    BASE_DIR

    /

    "models"

)



INTRADAY_FILE = (

    BACKTEST_DIR

    /

    "intraday_backtest_results.csv"

)



DAY_AHEAD_FILE = (

    BACKTEST_DIR

    /

    "day_ahead_backtest_results.csv"

)



# ============================================================
# TITLE
# ============================================================


st.title(

    "📊 Electricity Forecast Model Performance"

)



st.markdown(
"""
Machine Learning model monitoring dashboard.

Includes:

- Forecast accuracy
- Error analysis
- Model explainability
- Feature importance
"""
)



# ============================================================
# LOAD DATA
# ============================================================


@st.cache_data

def load_data(path):


    df = pd.read_csv(path)


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df





# ============================================================
# SIDEBAR
# ============================================================


st.sidebar.header(

    "Settings"

)



forecast_type = st.sidebar.selectbox(

    "Forecast Type",

    [

        "Intraday",

        "Day Ahead"

    ]

)



if forecast_type == "Intraday":


    DATA_FILE = INTRADAY_FILE


else:


    DATA_FILE = DAY_AHEAD_FILE





if not DATA_FILE.exists():

    st.error(

        f"Missing file:\n{DATA_FILE}"

    )

    st.stop()



df = load_data(

    DATA_FILE

)



countries = sorted(

    df["country"]

    .unique()

)



country = st.sidebar.selectbox(

    "Country",

    countries

)



df = df[

    df["country"]

    ==

    country

].copy()



# ============================================================
# DETECT COLUMNS
# ============================================================


actual_col = None

forecast_col = None



for col in df.columns:


    name = col.lower()


    if "actual" in name:

        actual_col = col


    if "forecast" in name:

        forecast_col = col





if actual_col is None or forecast_col is None:


    st.error(

        "Could not detect actual / forecast columns"

    )


    st.write(

        df.columns

    )

    st.stop()




# ============================================================
# CALCULATE ERRORS
# ============================================================


df["error"] = (

    df[forecast_col]

    -

    df[actual_col]

)



df["absolute_error"] = (

    df["error"]

    .abs()

)



df["percentage_error"] = (

    (

        df["absolute_error"]

        /

        df[actual_col]

        .replace(0,np.nan)

    )

    *

    100

)



# ============================================================
# KPI
# ============================================================


st.header(

    f"📈 {country.upper()} Performance"

)



mae = df["absolute_error"].mean()


rmse = np.sqrt(

    (

        df["error"]

        **2

    )

    .mean()

)



mape = df["percentage_error"].mean()



c1,c2,c3,c4 = st.columns(4)



with c1:

    st.metric(

        "MAE",

        f"{mae:.2f}"

    )


with c2:

    st.metric(

        "RMSE",

        f"{rmse:.2f}"

    )


with c3:

    st.metric(

        "MAPE",

        f"{mape:.2f}%"

    )


with c4:

    st.metric(

        "Rows",

        f"{len(df):,}"

    )



# ============================================================
# ACTUAL VS FORECAST
# ============================================================


st.divider()


st.subheader(

    "📈 Actual vs Forecast"

)



fig = px.line(

    df,

    x="timestamp",

    y=[

        actual_col,

        forecast_col

    ]

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ============================================================
# ERROR OVER TIME
# ============================================================


st.subheader(

    "📉 Forecast Error"

)



fig_error = px.line(

    df,

    x="timestamp",

    y="error"

)



fig_error.add_hline(

    y=0

)



st.plotly_chart(

    fig_error,

    use_container_width=True

)



# ============================================================
# ERROR DISTRIBUTION
# ============================================================


st.subheader(

    "📊 Error Distribution"

)



fig_hist = px.histogram(

    df,

    x="error",

    nbins=80

)



st.plotly_chart(

    fig_hist,

    use_container_width=True

)



# ============================================================
# BIGGEST ERRORS
# ============================================================


st.divider()



st.subheader(

    "🚨 Largest Forecast Errors"

)



largest = (

    df

    .sort_values(

        "absolute_error",

        ascending=False

    )

    .head(20)

)



st.dataframe(

    largest,

    use_container_width=True

)



# ============================================================
# FIND MODEL AUTOMATICALLY
# ============================================================


st.divider()



st.subheader(

    "🤖 XGBoost Feature Importance"

)



model_file = None



for root, dirs, files in os.walk(

    MODEL_DIR

):


    for file in files:


        if file.endswith(

            (

                ".pkl",

                ".joblib"

            )

        ):


            if country.lower() in file.lower():


                model_file = (

                    Path(root)

                    /

                    file

                )

                break



    if model_file:

        break





if model_file:


    st.info(

        f"Loaded model: {model_file.name}"

    )


    try:


        model = joblib.load(

            model_file

        )


        if hasattr(

            model,

            "feature_importances_"

        ):


            if hasattr(

                model,

                "feature_names_in_"

            ):


                features = model.feature_names_in_


            else:


                features = [

                    f"feature_{i}"

                    for i in range(

                        len(

                            model.feature_importances_

                        )

                    )

                ]



            importance = pd.DataFrame(

                {

                    "Feature":

                        features,

                    "Importance":

                        model.feature_importances_

                }

            )



            importance = importance.sort_values(

                "Importance",

                ascending=False

            ).head(15)



            fig_imp = px.bar(

                importance,

                x="Importance",

                y="Feature",

                orientation="h"

            )



            st.plotly_chart(

                fig_imp,

                use_container_width=True

            )



        else:


            st.warning(

                "Model has no feature importance"

            )


    except Exception as e:


        st.warning(

            str(e)

        )


else:


    st.warning(

        f"No model found for {country}"

    )



# ============================================================
# SUMMARY
# ============================================================


st.divider()



st.subheader(

    "📋 Performance Summary"

)



summary = pd.DataFrame(

    {

        "Metric":

        [

            "MAE",

            "RMSE",

            "MAPE",

            "Observations"

        ],


        "Value":

        [

            round(mae,3),

            round(rmse,3),

            round(mape,3),

            len(df)

        ]

    }

)



st.table(

    summary

)


st.success(

    "Model Performance Analysis Completed"

)