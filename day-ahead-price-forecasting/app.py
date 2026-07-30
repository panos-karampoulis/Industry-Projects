import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Day Ahead Price Forecasting",

    page_icon="⚡",

    layout="wide"

)



# ============================================================
# TITLE
# ============================================================

st.title(
    "⚡ Day Ahead Electricity Price Forecasting"
)


st.markdown(
"""
Interactive Energy Market Forecasting Platform

Features:

- Historical forecast exploration
- Actual vs predicted prices
- Model comparison
- Feature importance analysis

Markets:

🇩🇪 Germany  
🇬🇷 Greece
"""
)



# ============================================================
# SIDEBAR
# ============================================================





# ============================================================
# MAIN INFO
# ============================================================

col1, col2, col3 = st.columns(3)



with col1:

    st.metric(

        "Countries",

        "2"

    )


with col2:

    st.metric(

        "Models",

        "4"

    )


with col3:

    st.metric(

        "Forecast Horizon",

        "Hourly"

    )



st.divider()


st.subheader(
    "Project Overview"
)


st.write(
"""
This dashboard presents machine learning based
day-ahead electricity price forecasts using:

- Random Forest
- XGBoost
- LightGBM
- CatBoost

Energy market drivers:

- Demand
- Renewable generation
- Residual load
- Historical prices
"""
)