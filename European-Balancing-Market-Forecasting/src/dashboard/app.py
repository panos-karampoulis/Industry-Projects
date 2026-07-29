from pathlib import Path
from datetime import datetime
import subprocess
import sys

import pandas as pd
import streamlit as st
import plotly.express as px


# ==========================================================
# PROJECT ROOT
# ==========================================================

# ==========================================================
# PROJECT ROOT (LOCAL + STREAMLIT CLOUD SAFE)
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if not (PROJECT_ROOT / "demo_data").exists():

    PROJECT_ROOT = Path.cwd()

st.write("FILE:", __file__)
st.write("ROOT:", PROJECT_ROOT)
st.write("FILES:", list(PROJECT_ROOT.glob("*")))


st.write(
    "FORECAST PATH:",
    PROJECT_ROOT /
    "demo_data" /
    "forecasting" /
    "ml" /
    "germany_ml_forecast.csv"
)

st.write(
    "FORECAST EXISTS:",
    (
        PROJECT_ROOT /
        "demo_data" /
        "forecasting" /
        "ml" /
        "germany_ml_forecast.csv"
    ).exists()
)
# ==========================================================
# DATA PATHS
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"

DEMO_DIR = PROJECT_ROOT / "demo_data"

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

ANALYTICS_DIR = DATA_DIR / "analytics"


# ==========================================================
# PIPELINE PATH
# ==========================================================

REFRESH_SCRIPT = (

    PROJECT_ROOT
    /
    "src"
    /
    "pipeline"
    /
    "refresh_pipeline.py"

)



# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = [

    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"

]


COUNTRY_NAMES = {

    "germany": "Germany 🇩🇪",
    "france": "France 🇫🇷",
    "italy": "Italy 🇮🇹",
    "netherlands": "Netherlands 🇳🇱",
    "spain": "Spain 🇪🇸"

}



# ==========================================================
# STREAMLIT CONFIG
# ==========================================================

st.set_page_config(

    page_title="European Balancing Market Intelligence",

    page_icon="⚡",

    layout="wide"

)



# ==========================================================
# LOADERS
# ==========================================================


@st.cache_data
def load_risk_dataset(country):


    full_file = (

        PROCESSED_DIR
        /
        "risk_dataset"
        /
        f"{country}_risk_features.csv"

    )


    demo_file = (

        DEMO_DIR
        /
        "risk_dataset"
        /
        f"{country}_risk_features.csv"

    )


    if full_file.exists():

        file = full_file


    elif demo_file.exists():

        file = demo_file

        st.info(
            "Running in demo mode"
        )


    else:

        st.error(
            f"No dataset found for {country}"
        )

        return pd.DataFrame()


    df = pd.read_csv(file)


    return df




@st.cache_data
def load_forecast(country):


    possible_files = [

        (
            ANALYTICS_DIR
            /
            "forecasting"
            /
            "ml"
            /
            f"{country}_ml_forecast.csv"
        ),

        (
            PROJECT_ROOT
            /
            "demo_data"
            /
            "forecasting"
            /
            "ml"
            /
            f"{country}_ml_forecast.csv"
        )

    ]


    file = None


    for f in possible_files:

        if f.exists():

            file = f
            break


    if file is None:

        st.warning(
            f"Forecast file not found for {country}"
        )

        return pd.DataFrame()



    df = pd.read_csv(file)



    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            utc=True
        )


    return df



@st.cache_data
def load_analytics(filename):


    possible_files = [

        (
            ANALYTICS_DIR
            /
            filename
        ),

        (
            PROJECT_ROOT
            /
            "demo_data"
            /
            "analytics"
            /
            filename
        )

    ]


    file = None


    for f in possible_files:

        if f.exists():

            file = f
            break



    if file is None:

        return pd.DataFrame()



    return pd.read_csv(file)

# ==========================================================
# REFRESH FUNCTION
# ==========================================================


def run_refresh_pipeline():


    st.info(
        "Running data refresh pipeline..."
    )


    result = subprocess.run(

        [

            sys.executable,

            str(REFRESH_SCRIPT)

        ],

        cwd=PROJECT_ROOT,

        capture_output=True,

        text=True

    )


    if result.returncode == 0:


        st.success(
            "Refresh completed successfully"
        )


        st.cache_data.clear()


    else:


        st.error(
            "Refresh failed"
        )


        st.code(
            result.stderr
        )





def get_last_refresh():


    csv_files = list(

        DATA_DIR.rglob(
            "*.csv"
        )

    )


    if not csv_files:

        return "No refresh available"



    latest = max(

        csv_files,

        key=lambda x: x.stat().st_mtime

    )


    return datetime.fromtimestamp(

        latest.stat().st_mtime

    ).strftime(

        "%Y-%m-%d %H:%M:%S"

    )





# ==========================================================
# HEADER
# ==========================================================


st.title(

    "⚡ European Energy Balancing Market Intelligence Platform"

)



st.markdown(

"""
European electricity market analytics platform combining:

- Load forecasting
- Renewable generation analytics
- Imbalance monitoring
- Day-ahead price analytics
- Market risk indicators
- ML forecasting

Coverage:

Germany 🇩🇪  
France 🇫🇷  
Italy 🇮🇹  
Netherlands 🇳🇱  
Spain 🇪🇸  

Period: 2020 - 2026

"""

)



# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(

    "Market Explorer"

)



if st.sidebar.button(

    "🔄 Refresh Data Pipeline"

):

    run_refresh_pipeline()



st.sidebar.info(

f"""
Last refresh:

{get_last_refresh()}

"""

)



country = st.sidebar.selectbox(

    "Select Country",

    COUNTRIES,

    format_func=lambda x: COUNTRY_NAMES[x]

)



df = load_risk_dataset(

    country

)



if df.empty:

    st.stop()



# ==========================================================
# KPI SECTION
# ==========================================================


st.subheader(

    "Market Overview"

)



col1, col2, col3, col4 = st.columns(4)



with col1:


    avg_price = df[

        "price_eur_mwh"

    ].mean()



    st.metric(

        "Average Price €/MWh",

        f"{avg_price:.2f}"

    )



with col2:


    imbalance = df[

        "imbalance_mw"

    ].std()



    st.metric(

        "Imbalance Volatility MW",

        f"{imbalance:.2f}"

    )



with col3:


    renewable_share = df[

        "renewable_share"

    ].mean()*100



    st.metric(

        "Renewable Share",

        f"{renewable_share:.1f}%"

    )



with col4:


    stress = df[

        "market_stress_index"

    ].mean()



    st.metric(

        "Market Stress Index",

        f"{stress:.3f}"

    )

# ==========================================================
# PRICE EVOLUTION
# ==========================================================


st.subheader(

    "Electricity Price Evolution"

)



daily_price = (

    df

    .copy()

)

daily_price["timestamp"] = pd.to_datetime(
    daily_price["timestamp"],
    errors="coerce"
)


daily_price = (

    daily_price

    .set_index("timestamp")

    ["price_eur_mwh"]

    .resample("D")

    .mean()

    .reset_index()

)



fig = px.line(

    daily_price,

    x="timestamp",

    y="price_eur_mwh",

    title=f"{COUNTRY_NAMES[country]} Daily Average Price"

)



st.plotly_chart(

    fig,

    use_container_width=True,

    key="price_evolution_chart"

)



# ==========================================================
# IMBALANCE ANALYSIS
# ==========================================================


st.subheader(

    "Balancing Market Imbalance"

)



# ==========================================================
# IMBALANCE ANALYSIS
# ==========================================================

st.subheader(
    "Balancing Market Imbalance"
)


daily_imbalance = df.copy()


daily_imbalance["timestamp"] = pd.to_datetime(
    daily_imbalance["timestamp"],
    errors="coerce",
    utc=True
)


daily_imbalance = (

    daily_imbalance

    .dropna(
        subset=["timestamp"]
    )

    .set_index(
        "timestamp"
    )

    ["imbalance_mw"]

    .resample("D")

    .mean()

    .reset_index()

)


fig = px.line(

    daily_imbalance,

    x="timestamp",

    y="imbalance_mw",

    title="Daily Average Imbalance"

)


st.plotly_chart(

    fig,

    use_container_width=True,

    key="imbalance_chart"

)



fig = px.line(

    daily_imbalance,

    x="timestamp",

    y="imbalance_mw",

    title="Daily Average Imbalance"

)



st.plotly_chart(

    fig,

    use_container_width=True

)




# ==========================================================
# RENEWABLE GENERATION MIX
# ==========================================================


st.subheader(

    "Renewable Generation Mix"

)



renewable_columns = [

    "Solar_Actual Aggregated",

    "Wind Onshore_Actual Aggregated",

    "Wind Offshore_Actual Aggregated",

    "Hydro Run-of-river and poundage_Actual Aggregated",

    "Hydro Water Reservoir_Actual Aggregated",

    "Biomass_Actual Aggregated",

    "Other renewable_Actual Aggregated"

]



available_generation = [

    col

    for col in renewable_columns

    if col in df.columns

]



if len(available_generation) > 0:



    renewable_mix = (

        df[available_generation]

        .mean()

        .reset_index()

    )


    renewable_mix.columns = [

        "source",

        "MW"

    ]


    renewable_mix = renewable_mix.sort_values(

        "MW",

        ascending=False

    )


    fig = px.bar(

        renewable_mix,

        x="source",

        y="MW",

        title=f"{COUNTRY_NAMES[country]} Average Renewable Generation"

    )


    st.plotly_chart(

        fig,

        use_container_width=True,

        key="renewable_mix_chart"

    )


else:


    st.warning(

        "Renewable generation columns not available"

    )




# ==========================================================
# FORECAST SECTION
# ==========================================================


st.subheader(

    "ML Next Day Forecast"

)



forecast = load_forecast(

    country

)



if not forecast.empty:


    st.dataframe(

        forecast.tail(24),

        use_container_width=True

    )



    numeric_columns = forecast.select_dtypes(

        include="number"

    ).columns.tolist()



    if len(numeric_columns) > 0:


        selected_column = st.selectbox(

            "Forecast Variable",

            numeric_columns

        )



        fig = px.line(

            forecast,

            x="timestamp",

            y=selected_column,

            title=f"{selected_column} Forecast"

        )


        st.plotly_chart(

            fig,

            use_container_width=True,

            key="forecast_chart"

        )


else:


    st.warning(

        "Forecast file not available"

    )





# ==========================================================
# RISK RANKINGS
# ==========================================================


st.subheader(

    "European Risk Rankings"

)



tab1, tab2, tab3 = st.tabs(

    [

        "Balancing Risk",

        "Price Risk",

        "Renewable Risk"

    ]

)




with tab1:


    balancing = load_analytics(

        "balancing_risk_ranking.csv"

    )


    if not balancing.empty:


        fig = px.bar(

            balancing,

            x="country",

            y="balancing_risk_score",

            title="Balancing Risk Ranking"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


        st.dataframe(

            balancing,

            use_container_width=True

        )




with tab2:


    price = load_analytics(

        "price_risk_ranking.csv"

    )


    if not price.empty:


        fig = px.bar(

            price,

            x="country",

            y="price_risk_score",

            title="Price Risk Ranking"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


        st.dataframe(

            price,

            use_container_width=True

        )





with tab3:


    renewable = load_analytics(

        "renewable_risk_ranking.csv"

    )


    if not renewable.empty:


        fig = px.bar(

            renewable,

            x="country",

            y="renewable_risk_score",

            title="Renewable Risk Ranking"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


        st.dataframe(

            renewable,

            use_container_width=True

        )





# ==========================================================
# FOOTER
# ==========================================================


st.markdown(

"""
---

Built with:

🐍 Python  
📊 Pandas  
🤖 Scikit-learn  
⚡ XGBoost  
📈 Plotly  
🚀 Streamlit  


European Balancing Market Forecasting & Risk Intelligence Platform

"""

)