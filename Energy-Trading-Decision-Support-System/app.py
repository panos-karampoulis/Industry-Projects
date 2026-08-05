# ==========================================================
# ENERGY TRADING DECISION SUPPORT SYSTEM
# STREAMLIT DASHBOARD v5
# Local + Streamlit Cloud Compatible
# ==========================================================


import streamlit as st
import pandas as pd
import plotly.express as px

import subprocess
import sys
import os

from pathlib import Path
from datetime import datetime



# ==========================================================
# PAGE CONFIG
# ==========================================================


st.set_page_config(
    page_title="Energy Trading DSS",
    page_icon="⚡",
    layout="wide"
)



# ==========================================================
# PATH CONFIGURATION
# ==========================================================


BASE_DIR = Path(__file__).resolve().parent


FEATURE_DIR = (
    BASE_DIR
    /
    "data"
    /
    "features"
)


DEMO_DIR = (
    BASE_DIR
    /
    "data"
    /
    "demo"
)


RESULT_DIR = (
    BASE_DIR
    /
    "results"
)


PRICE_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)



PIPELINE = [

    sys.executable,

    "src/pipeline/run_pipeline.py"

]



COUNTRIES = [

    "germany",

    "france",

    "italy",

    "spain",

    "netherlands"

]



# ==========================================================
# ENVIRONMENT DETECTION
# ==========================================================


def is_streamlit_cloud():

    """
    Detect Streamlit Cloud environment.
    """

    return (

        os.environ.get(
            "STREAMLIT_SHARING_MODE"
        )
        is not None

    )




CLOUD_MODE = is_streamlit_cloud()



# ==========================================================
# DATA LOADERS
# ==========================================================



@st.cache_data
def load_features(country):


    real_file = (
        FEATURE_DIR
        /
        f"{country}_features.csv"
    )


    demo_file = (
        DEMO_DIR
        /
        f"{country}_features_sample.csv"
    )



    if real_file.exists():

        file = real_file

        data_mode = "Local"



    elif demo_file.exists():

        file = demo_file

        data_mode = "Demo"



    else:

        st.error(
            f"No dataset found for {country}"
        )

        st.stop()



    df = pd.read_csv(file)



    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            utc=True
        )



    st.sidebar.caption(
        f"Data source: {data_mode}"
    )


    return df

@st.cache_data
def load_risk(country):

    """
    Load imbalance risk results.

    Priority:
    Local results
    Demo fallback
    """



    real_file = (

        RESULT_DIR

        /

        f"{country}_imbalance_risk.csv"

    )




    demo_file = (

        DEMO_DIR

        /

        "imbalance_risk_sample.csv"

    )




    if real_file.exists():

        file = real_file


    elif demo_file.exists():

        file = demo_file


    else:

        return pd.DataFrame()




    df = pd.read_csv(file)




    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df





@st.cache_data
def load_signals():

    """
    Load trading decisions.
    """



    real_file = (

        RESULT_DIR

        /

        "trading_decisions_all_countries.csv"

    )




    demo_file = (

        DEMO_DIR

        /

        "trading_decisions_sample.csv"

    )




    if real_file.exists():

        file = real_file


    elif demo_file.exists():

        file = demo_file


    else:

        return pd.DataFrame()




    df = pd.read_csv(file)




    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df





# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(

    "⚡ Energy Trading DSS"

)




country = st.sidebar.selectbox(

    "Country",

    COUNTRIES

)





market_type = st.sidebar.selectbox(

    "Market",

    [

        "Day Ahead",

        "Intraday"

    ]

)





st.sidebar.divider()



if CLOUD_MODE:


    st.sidebar.info(

        "☁️ Streamlit Cloud\n\nDemo Dataset Mode"

    )


else:


    st.sidebar.success(

        "💻 Local Dataset Mode"

    )





# ==========================================================
# PIPELINE EXECUTION
# ==========================================================


st.sidebar.divider()



if st.sidebar.button(

    "🔄 Run Pipeline"

):


    with st.spinner(

        "Running energy pipeline..."

    ):


        try:


            result = subprocess.run(

                PIPELINE,

                cwd=BASE_DIR,

                capture_output=True,

                text=True

            )



            if result.returncode == 0:


                st.sidebar.success(

                    "Pipeline completed"

                )


                st.cache_data.clear()

                st.rerun()



            else:


                st.sidebar.error(

                    "Pipeline failed"

                )


                st.sidebar.code(

                    result.stderr

                )



        except Exception as e:


            st.sidebar.error(

                str(e)

            )





# ==========================================================
# LOAD DATA
# ==========================================================


features = load_features(

    country

)



risk = load_risk(

    country

)



signals = load_signals()



# ==========================================================
# CLEAN FEATURES
# ==========================================================


market = features.copy()



# remove duplicate columns if any

market = (

    market

    .loc[:, ~market.columns.duplicated()]

)



# ==========================================================
# MARKET PRICE HANDLING
# ==========================================================


if "day_ahead_price" not in market.columns:


    market["day_ahead_price"] = 0




if "Intraday" not in market.columns:


    market["Intraday"] = (

        market["day_ahead_price"]

    )




if "Day Ahead" not in market.columns:


    market["Day Ahead"] = (

        market["day_ahead_price"]

    )



# ==========================================================
# DATE RANGE
# ==========================================================


min_date = (

    market["timestamp"]

    .min()

    .date()

)



max_date = (

    market["timestamp"]

    .max()

    .date()

)



selected_date = st.sidebar.date_input(

    "Select Date",

    value=max_date,

    min_value=min_date,

    max_value=max_date

)





# ==========================================================
# FILTER DAY
# ==========================================================


market_day = market[

    market["timestamp"]

    .dt.date

    ==

    selected_date

]



if market_day.empty:


    market_day = market.tail(96)


# ==========================================================
# SIGNAL FILTER
# ==========================================================


if not signals.empty:


    signal_day = signals[

        (signals["country"] == country)

        &

        (

            signals["timestamp"]

            .dt.date

            ==

            selected_date

        )

    ]


else:


    signal_day = pd.DataFrame()





# ==========================================================
# LATEST VALUES
# ==========================================================


latest = market_day.iloc[-1]



if not signal_day.empty:


    latest_signal = signal_day.iloc[-1]


else:


    latest_signal = {


        "trading_signal": "N/A",

        "confidence": 0,

        "risk_score": 0


    }





# ==========================================================
# TITLE
# ==========================================================


st.title(

    "⚡ Energy Trading Decision Support System"

)



st.caption(

"""

Day Ahead & Intraday Market Analysis |

Load Forecasting |

Renewable Generation |

Imbalance Risk |

Trading Signals

"""

)





# ==========================================================
# KPI SECTION
# ==========================================================


c1, c2, c3, c4, c5 = st.columns(5)



with c1:


    price = latest.get(

        "day_ahead_price",

        0

    )


    st.metric(

        "Day Ahead Price",

        f"{price:.2f} €/MWh"

    )





with c2:


    market_price = latest.get(

        market_type,

        0

    )


    st.metric(

        market_type,

        f"{market_price:.2f} €/MWh"

    )





with c3:


    load = latest.get(

        "load_mw",

        0

    )


    st.metric(

        "Load",

        f"{load:,.0f} MW"

    )





with c4:


    renewable = latest.get(

        "renewable_share",

        0

    )


    st.metric(

        "Renewable Share",

        f"{renewable:.1%}"

    )





with c5:


    st.metric(

        "Trading Signal",

        latest_signal.get(

            "trading_signal",

            "N/A"

        )

    )





st.divider()





# ==========================================================
# PRICE ANALYSIS
# ==========================================================


st.subheader(

    "📈 Market Price Analysis"

)




price_columns = []



for col in [

    "day_ahead_price",

    "Intraday"

]:


    if col in market_day.columns:


        price_columns.append(col)




if price_columns:


    fig = px.line(

        market_day,

        x="timestamp",

        y=price_columns,

        title="Electricity Market Prices"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


else:


    st.info(

        "Price data unavailable"

    )






# ==========================================================
# SYSTEM FUNDAMENTALS
# ==========================================================


st.subheader(

    "⚡ System Fundamentals"

)



col1, col2 = st.columns(2)




# LOAD


with col1:


    if "load_mw" in market_day.columns:


        fig = px.line(

            market_day,

            x="timestamp",

            y="load_mw",

            title="Electricity Load"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:


        st.info(

            "Load data unavailable"

        )






# RENEWABLES


with col2:


    renewable_columns = []



    for col in [

        "wind_generation",

        "solar_generation",

        "renewable_generation"

    ]:


        if col in market_day.columns:


            renewable_columns.append(col)





    if renewable_columns:


        fig = px.area(

            market_day,

            x="timestamp",

            y=renewable_columns,

            title="Renewable Generation"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:


        st.info(

            "Renewable data unavailable"

        )







# ==========================================================
# RESIDUAL LOAD
# ==========================================================


if "residual_load" in market_day.columns:


    st.subheader(

        "🔋 Residual Load"

    )


    fig = px.line(

        market_day,

        x="timestamp",

        y="residual_load",

        title="Residual Load"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )







# ==========================================================
# IMBALANCE RISK
# ==========================================================


st.subheader(

    "⚠️ Imbalance Risk Analytics"

)




if not risk.empty:


    risk_day = risk[

        risk["timestamp"]

        .dt.date

        ==

        selected_date

    ]



    if not risk_day.empty:


        fig = px.line(

            risk_day,

            x="timestamp",

            y="risk_score",

            title="Risk Score"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


        latest_risk = risk_day.iloc[-1]["risk_score"]


        if latest_risk < 0.33:


            risk_level = "Low Risk"


        elif latest_risk < 0.66:


            risk_level = "Medium Risk"


        else:


            risk_level = "High Risk"




        st.metric(

            "Current Risk Level",

            risk_level,

            f"{latest_risk:.2f}"

        )


    else:


        st.info(

            "No risk data for selected date"

        )



else:


    st.info(

        "Risk analytics available after pipeline execution"

    )







# ==========================================================
# TRADING DECISION ENGINE
# ==========================================================


st.subheader(

    "💹 Trading Decision Engine"

)




if not signals.empty:


    country_signals = signals[

        signals["country"]

        ==

        country

    ]



    if not country_signals.empty:


        fig = px.pie(

            country_signals,

            names="trading_signal",

            title=f"{country} Trading Signals"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


else:


    st.info(

        "Trading decisions unavailable"

    )







# ==========================================================
# AI RECOMMENDATION
# ==========================================================


st.divider()



st.subheader(

    "🤖 AI Trading Recommendation"

)





signal = latest_signal.get(

    "trading_signal",

    "N/A"

)



confidence = latest_signal.get(

    "confidence",

    0

)



risk_score = latest_signal.get(

    "risk_score",

    0

)




if signal == "BUY":


    color = "green"


elif signal == "SELL":


    color = "red"


else:


    color = "orange"





st.markdown(

f"""

<h2 style="color:{color}">

Recommendation: {signal}

</h2>


<b>Confidence:</b>

{confidence:.1f}%


<br><br>


<b>Risk Score:</b>

{risk_score:.2f}

"""

,

unsafe_allow_html=True

)







# ==========================================================
# FOOTER
# ==========================================================


st.divider()



st.caption(

f"""

Dashboard refresh:

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}



Mode:

{"Cloud Demo Data" if CLOUD_MODE else "Local Data"}

"""

)