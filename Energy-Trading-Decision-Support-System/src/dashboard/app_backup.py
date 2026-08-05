# ==========================================================
# ENERGY TRADING DECISION SUPPORT SYSTEM
# Streamlit Dashboard
# ==========================================================

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

print("="*60)
print("RUNNING FILE:")
print(__file__)
print("="*60)
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="European Energy Trading Decision Support System",
    page_icon="⚡",
    layout="wide"
)


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "features"
)


RESULTS_DIR = os.path.join(
    BASE_DIR,
    "results"
)


MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)


# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = {
    "Germany": "germany",
    "France": "france",
    "Italy": "italy",
    "Spain": "spain",
    "Netherlands": "netherlands"
}


# ==========================================================
# LOAD DATA FUNCTIONS
# ==========================================================

@st.cache_data
def load_country_data(country):

    feature_path = os.path.join(
        DATA_DIR,
        f"{country}_features.csv"
    )


    if not os.path.exists(feature_path):
        return None


    df = pd.read_csv(
        feature_path
    )


    # -------------------------------
    # Timestamp UTC FIX
    # -------------------------------

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="coerce"
    )


    df = df.sort_values(
        "timestamp"
    )


    # -------------------------------
    # Merge risk results
    # -------------------------------

    risk_path = os.path.join(
        RESULTS_DIR,
        f"{country}_imbalance_risk.csv"
    )


    if os.path.exists(risk_path):

        risk = pd.read_csv(
            risk_path
        )


        risk["timestamp"] = pd.to_datetime(
            risk["timestamp"],
            utc=True,
            errors="coerce"
        )


        df = df.merge(
            risk[
                [
                    "timestamp",
                    "risk_score",
                    "risk_level"
                ]
            ],
            on="timestamp",
            how="left"
        )


    else:

        df["risk_score"] = np.nan

        df["risk_level"] = "N/A"



    # -------------------------------
    # Merge trading decisions
    # -------------------------------


    trading_path = os.path.join(
        RESULTS_DIR,
        "trading_decisions_all_countries.csv"
    )


    if os.path.exists(trading_path):


        trading = pd.read_csv(
            trading_path
        )


        trading["timestamp"] = pd.to_datetime(
            trading["timestamp"],
            utc=True,
            errors="coerce"
        )


        trading = trading[
            trading["country"]
            .str.lower()
            ==
            country
        ]


        df = df.merge(
            trading[
                [
                    "timestamp",
                    "trading_signal"
                ]
            ],
            on="timestamp",
            how="left"
        )


    else:

        df["trading_signal"] = "N/A"



    return df



# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title(
    "⚡ Energy Trading DSS"
)


selected_country = st.sidebar.selectbox(
    "Select Country",
    list(COUNTRIES.keys())
)


country_code = COUNTRIES[
    selected_country
]


refresh = st.sidebar.button(
    "🔄 Refresh Full System"
)


if refresh:

    with st.spinner(
        "Updating Energy Trading Decision Support System..."
    ):

        from src.pipeline.run_pipeline import run_pipeline

        run_pipeline()


    st.cache_data.clear()


    st.success(
        "System refreshed successfully"
    )


    st.rerun()



# ==========================================================
# LOAD SELECTED COUNTRY
# ==========================================================


df = load_country_data(
    country_code
)


if df is None:

    st.error(
        "Dataset not found"
    )

    st.stop()



# ==========================================================
# HEADER
# ==========================================================


st.title(
    "⚡ European Energy Trading Decision Support System"
)


st.write(
    """
Machine Learning based electricity market analytics platform.

Coverage:

🇩🇪 Germany  
🇫🇷 France  
🇮🇹 Italy  
🇳🇱 Netherlands  
🇪🇸 Spain
"""
)



st.write(
    f"""
Historical coverage:

{df.timestamp.min().date()}
-
{df.timestamp.max().date()}
"""
)



# ==========================================================
# DATE FILTER
# ==========================================================


st.subheader(
    "📅 Select Analysis Date"
)



min_date = (
    df["timestamp"]
    .min()
    .date()
)


max_date = (
    df["timestamp"]
    .max()
    .date()
)



selected_date = st.date_input(
    "Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)



# ==========================================================
# SINGLE DATE UTC FILTER
# ==========================================================


filtered = df[
    df["timestamp"]
    .dt.date
    ==
    selected_date
].copy()



if filtered.empty:

    st.warning(
        "No data available for selected date"
    )

    st.stop()

if filtered.empty:

    st.warning(
        "No data available for selected period"
    )

    st.stop()



# ==========================================================
# KPI CALCULATIONS
# ==========================================================


latest = filtered.iloc[-1]



avg_price = filtered[
    "day_ahead_price"
].mean()



avg_load = filtered[
    "load_mw"
].mean()



renewable_share = filtered[
    "renewable_share"
].mean()*100



risk_score = filtered[
    "risk_score"
].mean()



signal = latest.get(
    "trading_signal",
    "N/A"
)



risk_level = latest.get(
    "risk_level",
    "N/A"
)



# ==========================================================
# KPI DISPLAY
# ==========================================================


st.subheader(
    f"🌍 {selected_country} Market Overview"
)



k1,k2,k3,k4,k5 = st.columns(5)


k1.metric(
    "Average Price",
    f"{avg_price:.2f} €/MWh"
)


k2.metric(
    "Average Load",
    f"{avg_load:,.0f} MW"
)


k3.metric(
    "Renewable Share",
    f"{renewable_share:.2f}%"
)


k4.metric(
    "Risk Score",
    f"{risk_score:.2f}"
)


k5.metric(
    "Trading Signal",
    signal
)